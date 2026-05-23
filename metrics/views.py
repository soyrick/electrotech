"""
Vistas de la aplicación 'metrics'.
Dashboard principal, métricas con gráficas e historial de movimientos.
"""

import calendar

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.db.models.functions import Coalesce, ExtractMonth, TruncDay
from django.utils import timezone

from accounts.decorators import admin_required
from inventory.models import Componente
from movements.models import Movimiento, DetalleMovimiento


@login_required
def dashboard(request):
    """Dashboard principal con accesos a todos los módulos."""
    return render(request, 'metrics/dashboard.html')


def _parse_int(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _filtrar_detalles(year, month=None, componente_id=None):
    detalles = DetalleMovimiento.objects.filter(movimiento__fecha_hora__year=year)
    if month:
        detalles = detalles.filter(movimiento__fecha_hora__month=month)
    if componente_id:
        detalles = detalles.filter(componente_id=componente_id)
    return detalles


def _obtener_resumen(detalles, month=None):
    total_ingresos = detalles.filter(movimiento__tipo=Movimiento.Tipo.INGRESO).aggregate(
        total=Coalesce(Sum('cantidad'), 0)
    )['total']
    total_egresos = detalles.filter(movimiento__tipo=Movimiento.Tipo.EGRESO).aggregate(
        total=Coalesce(Sum('cantidad'), 0)
    )['total']

    if month:
        pico = detalles.annotate(dia=TruncDay('movimiento__fecha_hora')).values('dia').annotate(
            total=Sum('cantidad')
        ).order_by('-total').first()
        dia_pico = pico['dia'].strftime('%d/%m/%Y') if pico else '—'
    else:
        pico = detalles.annotate(mes=ExtractMonth('movimiento__fecha_hora')).values('mes').annotate(
            total=Sum('cantidad')
        ).order_by('-total').first()
        dia_pico = calendar.month_name[pico['mes']] if pico else '—'

    componente_top = detalles.filter(movimiento__tipo=Movimiento.Tipo.EGRESO).values('snapshot_nombre').annotate(
        total=Sum('cantidad')
    ).order_by('-total').first()
    componente_mas_retirado = componente_top['snapshot_nombre'] if componente_top else '—'

    return {
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'dia_pico': dia_pico,
        'componente_mas_retirado': componente_mas_retirado,
    }


@login_required
@admin_required
def metricas_graficas(request):
    """Página de métricas con gráfica de ingresos/egresos por mes."""
    current_year = timezone.now().year
    selected_year = _parse_int(request.GET.get('year'), current_year)
    selected_month = _parse_int(request.GET.get('month'))
    selected_componente_id = _parse_int(request.GET.get('componente'))

    componentes = Componente.objects.order_by('nombre')
    componentes = componentes.select_related('categoria')

    if selected_componente_id and not componentes.filter(pk=selected_componente_id).exists():
        selected_componente_id = None

    detalles = _filtrar_detalles(
        year=selected_year,
        month=selected_month,
        componente_id=selected_componente_id,
    )

    resumen = _obtener_resumen(detalles, month=selected_month)

    meses = [
        {'valor': i, 'texto': f'{calendar.month_name[i]} {selected_year}'}
        for i in range(1, 13)
    ]

    context = {
        'componentes': componentes,
        'meses': meses,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'selected_componente_id': selected_componente_id,
        'resumen': resumen,
    }
    return render(request, 'metrics/graficas.html', context)


@login_required
@admin_required
def api_datos_grafica(request):
    """API: retorna datos JSON para la gráfica Chart.js."""
    selected_year = _parse_int(request.GET.get('year'), timezone.now().year)
    selected_month = _parse_int(request.GET.get('month'))
    selected_componente_id = _parse_int(request.GET.get('componente'))

    detalles = _filtrar_detalles(
        year=selected_year,
        month=selected_month,
        componente_id=selected_componente_id,
    )

    if selected_month:
        days_in_month = calendar.monthrange(selected_year, selected_month)[1]
        labels = [str(day) for day in range(1, days_in_month + 1)]
        ingresos = detalles.filter(movimiento__tipo=Movimiento.Tipo.INGRESO).annotate(
            dia=TruncDay('movimiento__fecha_hora')
        ).values('dia').annotate(total=Sum('cantidad')).order_by('dia')
        egresos = detalles.filter(movimiento__tipo=Movimiento.Tipo.EGRESO).annotate(
            dia=TruncDay('movimiento__fecha_hora')
        ).values('dia').annotate(total=Sum('cantidad')).order_by('dia')

        ingresos_data = [0] * days_in_month
        egresos_data = [0] * days_in_month
        for item in ingresos:
            ingresos_data[item['dia'].day - 1] = item['total']
        for item in egresos:
            egresos_data[item['dia'].day - 1] = item['total']
    else:
        labels = [calendar.month_name[i] for i in range(1, 13)]
        ingresos = detalles.filter(movimiento__tipo=Movimiento.Tipo.INGRESO).annotate(
            mes=ExtractMonth('movimiento__fecha_hora')
        ).values('mes').annotate(total=Sum('cantidad')).order_by('mes')
        egresos = detalles.filter(movimiento__tipo=Movimiento.Tipo.EGRESO).annotate(
            mes=ExtractMonth('movimiento__fecha_hora')
        ).values('mes').annotate(total=Sum('cantidad')).order_by('mes')

        ingresos_data = [0] * 12
        egresos_data = [0] * 12
        for item in ingresos:
            ingresos_data[item['mes'] - 1] = item['total']
        for item in egresos:
            egresos_data[item['mes'] - 1] = item['total']

    resumen = _obtener_resumen(detalles, month=selected_month)

    return JsonResponse({
        'labels': labels,
        'ingresos': ingresos_data,
        'egresos': egresos_data,
        'resumen': resumen,
    })


@login_required
@admin_required
def historial(request):
    """Historial completo de movimientos (ingresos y egresos)."""
    tipo = request.GET.get('tipo')
    componente_id = _parse_int(request.GET.get('componente'))
    search = request.GET.get('search', '').strip()

    movimientos = Movimiento.objects.select_related('usuario').prefetch_related('detalles__componente')

    if tipo in (Movimiento.Tipo.INGRESO, Movimiento.Tipo.EGRESO):
        movimientos = movimientos.filter(tipo=tipo)

    if componente_id:
        movimientos = movimientos.filter(detalles__componente_id=componente_id)

    if search:
        movimientos = movimientos.filter(
            Q(numero_planilla__icontains=search) |
            Q(nombre_persona__icontains=search) |
            Q(usuario__email__icontains=search)
        )

    movimientos = movimientos.annotate(total_unidades=Coalesce(Sum('detalles__cantidad'), 0)).order_by('-fecha_hora').distinct()
    componentes = Componente.objects.order_by('nombre')
    componente_seleccionado = None
    if componente_id:
        componente_seleccionado = componentes.filter(pk=componente_id).first()

    cantidad_total = movimientos.aggregate(total=Coalesce(Sum('total_unidades'), 0))['total'] or 0

    context = {
        'movimientos': movimientos,
        'componentes': componentes,
        'tipo': tipo,
        'componente_id': componente_id,
        'componente_seleccionado': componente_seleccionado,
        'search': search,
        'cantidad_total': cantidad_total,
    }
    return render(request, 'metrics/historial.html', context)


@login_required
@admin_required
def ver_planilla_historica(request, pk):
    """Vista de una planilla histórica (re-generada desde snapshot)."""
    movimiento = get_object_or_404(Movimiento, pk=pk)
    return render(request, 'metrics/ver_planilla.html', {
        'movimiento': movimiento,
    })
