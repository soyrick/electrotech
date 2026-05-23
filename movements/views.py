"""
Vistas de la aplicación 'movements'.
Formularios de ingreso y egreso, generación de planillas PDF.
Implementación mínima con CBV para ingreso y egreso (CreateView).
"""

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import FormView, TemplateView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.shortcuts import redirect
from urllib.parse import urlencode
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test

from .forms import IngresoForm, EgresoForm
from .models import Movimiento
from .utils import generar_comprobante_pdf


@method_decorator(login_required, name='dispatch')
class IngresoCreateView(FormView):
    """Vista para registrar ingresos de componentes (FormView para forms.Form)."""
    form_class = IngresoForm
    template_name = 'movements/ingreso.html'
    success_url = reverse_lazy('movements:ingreso')

    def form_valid(self, form):
        # No crear todavía: mostrar resumen con los datos enviados y pedir confirmación
        cleaned = form.cleaned_data
        # Preparar datos para la vista de confirmación
        pending = {
            'tipo': Movimiento.Tipo.INGRESO,
            'componente': cleaned.get('componente'),
            'cantidad': cleaned.get('cantidad'),
            'nombre_persona': cleaned.get('nombre_persona'),
            'cedula': cleaned.get('cedula'),
            'cargo': cleaned.get('cargo'),
            'departamento': cleaned.get('departamento'),
            'fecha_hora': cleaned.get('fecha_hora') if cleaned.get('usar_fecha_hora') else None,
        }
        return render(self.request, 'movements/confirm_comprobante.html', {
            'pending': pending,
            'action_url': reverse_lazy('movements:confirm_create'),
        })

    def get_initial(self):
        # Permitir prefilling desde query params al volver a editar
        initial = super().get_initial()
        params = self.request.GET
        for key in ['componente', 'cantidad', 'nombre_persona', 'cedula_prefijo', 'cedula', 'cargo', 'departamento', 'fecha_personalizada', 'hora_personalizada', 'usar_fecha_hora']:
            if params.get(key) is not None:
                val = params.get(key)
                # Normalizar checkbox
                if key == 'usar_fecha_hora':
                    initial[key] = val.lower() in ['1', 'true', 'on']
                else:
                    initial[key] = val
        return initial


@method_decorator(login_required, name='dispatch')
class EgresoCreateView(FormView):
    """Vista para registrar egresos de componentes (FormView para forms.Form)."""
    form_class = EgresoForm
    template_name = 'movements/egreso.html'
    success_url = reverse_lazy('movements:egreso')

    def form_valid(self, form):
        cleaned = form.cleaned_data
        pending = {
            'tipo': Movimiento.Tipo.EGRESO,
            'componente': cleaned.get('componente'),
            'cantidad': cleaned.get('cantidad'),
            'nombre_persona': cleaned.get('nombre_persona'),
            'cedula': cleaned.get('cedula'),
            'cargo': cleaned.get('cargo'),
            'departamento': cleaned.get('departamento'),
            'motivo': cleaned.get('motivo'),
            'fecha_hora': cleaned.get('fecha_hora') if cleaned.get('usar_fecha_hora') else None,
        }
        return render(self.request, 'movements/confirm_comprobante.html', {
            'pending': pending,
            'action_url': reverse_lazy('movements:confirm_create'),
        })

    def get_initial(self):
        initial = super().get_initial()
        params = self.request.GET
        for key in ['componente', 'cantidad', 'nombre_persona', 'cedula_prefijo', 'cedula', 'cargo', 'departamento', 'fecha_personalizada', 'hora_personalizada', 'usar_fecha_hora', 'motivo']:
            if params.get(key) is not None:
                val = params.get(key)
                if key == 'usar_fecha_hora':
                    initial[key] = val.lower() in ['1', 'true', 'on']
                else:
                    initial[key] = val
        return initial


@login_required
def volver_y_editar(request, pk):
    """Reconstruye los parámetros del formulario desde un Movimiento, elimina el movimiento temporal y redirige al formulario con query params."""
    mov = get_object_or_404(Movimiento, pk=pk)
    # Extraer cedula en prefijo/número si tiene formato PREFIJO-NUM
    cedula_prefijo = ''
    cedula_num = ''
    if mov.cedula:
        parts = mov.cedula.split('-', 1)
        if len(parts) == 2:
            cedula_prefijo, cedula_num = parts[0], parts[1]
        else:
            cedula_num = mov.cedula

    params = {
        'componente': mov.detalles.first().componente.pk if mov.detalles.exists() and mov.detalles.first().componente else '',
        'cantidad': mov.detalles.first().cantidad if mov.detalles.exists() else '',
        'nombre_persona': mov.nombre_persona or '',
        'cedula_prefijo': cedula_prefijo,
        'cedula': cedula_num,
        'cargo': mov.cargo or '',
        'departamento': mov.departamento or '',
        'usar_fecha_hora': '1',
        'fecha_personalizada': mov.fecha_hora.date().isoformat(),
        'hora_personalizada': mov.fecha_hora.time().strftime('%H:%M') if mov.fecha_hora else '',
    }

    # Elegir ruta de destino según tipo
    destino = 'movements:ingreso' if mov.es_ingreso else 'movements:egreso'
    # Borrar movimiento temporal
    mov.delete()
    qs = urlencode({k: v for k, v in params.items() if v is not None and v != ''})
    return redirect(f"{reverse_lazy(destino)}?{qs}")


# Mantener vistas auxiliares (planilla/pdf) como placeholders

def planilla_ingreso(request, pk):
    """Vista previa de planilla de ingreso para impresión."""
    return render(request, 'movements/planilla_ingreso.html')


def pdf_ingreso(request, pk):
    """Genera y descarga el PDF de una planilla de ingreso."""
    movimiento = get_object_or_404(Movimiento, pk=pk)
    return generar_comprobante_pdf(movimiento)


def planilla_egreso(request, pk):
    """Vista previa de planilla de egreso para impresión."""
    return render(request, 'movements/planilla_egreso.html')


def pdf_egreso(request, pk):
    """Genera y descarga el PDF de una planilla de egreso."""
    movimiento = get_object_or_404(Movimiento, pk=pk)
    return generar_comprobante_pdf(movimiento)


def buscar_componente(request):
    """API: busca componentes por nombre para autocompletar."""
    # Implementación pendiente (devolver JSON)
    pass


@login_required
@require_POST
def confirm_create_movimiento(request):
    """Crea el Movimiento y Detalle a partir de los datos POST después de confirmación."""
    # Leer datos desde POST
    tipo = request.POST.get('tipo')
    componente_id = request.POST.get('componente')
    cantidad = int(request.POST.get('cantidad') or 0)
    nombre_persona = request.POST.get('nombre_persona') or ''
    cedula = request.POST.get('cedula') or ''
    cargo = request.POST.get('cargo') or ''
    departamento = request.POST.get('departamento') or ''
    fecha_hora = request.POST.get('fecha_hora') or None

    # Crear movimiento
    movimiento = Movimiento.objects.create(
        tipo=tipo,
        numero_planilla='',
        usuario=request.user,
        nombre_persona=nombre_persona,
        cedula=cedula,
        cargo=cargo,
        departamento=departamento,
    )
    movimiento.generar_numero_planilla()

    # Aplicar fecha/hora personalizada si viene
    if fecha_hora:
        try:
            from django.utils.dateparse import parse_datetime
            dt = parse_datetime(fecha_hora)
            if dt:
                movimiento.fecha_hora = dt
                movimiento.save(update_fields=['fecha_hora'])
        except Exception:
            pass

    # Crear detalle
    try:
        comp = None
        from inventory.models import Componente
        if componente_id:
            comp = Componente.objects.get(pk=int(componente_id))
        detalle = movimiento.detalles.model(
            movimiento=movimiento,
            componente=comp,
            cantidad=cantidad,
        )
        detalle.guardar_snapshot()
        detalle.save()
        if comp:
            # Ajustar stock según tipo
            if movimiento.es_ingreso:
                comp.cantidad = (comp.cantidad or 0) + cantidad
            else:
                comp.cantidad = (comp.cantidad or 0) - cantidad
                if comp.cantidad < 0:
                    comp.cantidad = 0
            comp.save(update_fields=['cantidad'])
    except Exception:
        pass

    # Generar y devolver PDF directamente
    return generar_comprobante_pdf(movimiento)


@login_required
@require_POST
@user_passes_test(lambda u: u.is_superuser)
def eliminar_movimiento(request, pk):
    """Marca un movimiento como eliminado (soft-delete). Solo superusuarios."""
    mov = get_object_or_404(Movimiento, pk=pk)
    mov.eliminado = True
    mov.eliminado_por = request.user
    mov.eliminado_en = timezone.now()
    mov.save(update_fields=['eliminado', 'eliminado_por', 'eliminado_en'])
    messages.success(request, f'Movimiento {mov.numero_planilla} marcado como eliminado.')
    return redirect('metrics:historial')


# Function wrappers for compatibility with existing urls.py
def ingreso_componentes(request):
    """Compatibilidad: interfaz basada en funciones para ingreso."""
    view = IngresoCreateView.as_view()
    return view(request)


def egreso_componentes(request):
    """Compatibilidad: interfaz basada en funciones para egreso."""
    view = EgresoCreateView.as_view()
    return view(request)
