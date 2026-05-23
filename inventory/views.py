"""
Vistas de la aplicación 'inventory' — Implementación de CRUD con CBV.
"""

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from accounts.decorators import admin_required
from .models import Categoria, Componente
from .forms import CategoriaForm, ComponenteForm


@method_decorator(login_required, name='dispatch')
class ComponenteListView(ListView):
    """Lista paginada de componentes (10 por página), ordenada por nombre."""
    model = Componente
    template_name = 'inventory/lista.html'
    context_object_name = 'componentes'
    paginate_by = 10
    ordering = ['nombre']

    def get_queryset(self):
        return super().get_queryset().select_related('categoria')


@method_decorator(login_required, name='dispatch')
class ComponenteDetailView(DetailView):
    """Detalle de un componente."""
    model = Componente
    template_name = 'inventory/detalle.html'
    context_object_name = 'componente'

    def get_queryset(self):
        return super().get_queryset().select_related('categoria')


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ComponenteCreateView(CreateView):
    """Crear un nuevo componente. Requiere permiso admin."""
    model = Componente
    form_class = ComponenteForm
    template_name = 'inventory/form.html'
    success_url = reverse_lazy('inventory:listado')

    def form_valid(self, form):
        # El manejo de archivos lo gestiona Django si el template usa enctype multipart/form-data
        response = super().form_valid(form)
        messages.success(self.request, 'Componente creado correctamente.')
        return response


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ComponenteUpdateView(UpdateView):
    """Editar un componente existente. Requiere permiso admin."""
    model = Componente
    form_class = ComponenteForm
    template_name = 'inventory/form.html'
    success_url = reverse_lazy('inventory:listado')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Componente actualizado correctamente.')
        return response


@method_decorator(login_required, name='dispatch')
@method_decorator(admin_required, name='dispatch')
class ComponenteDeleteView(DeleteView):
    """Eliminar un componente (confirmación). Requiere permiso admin."""
    model = Componente
    template_name = 'inventory/confirmar_eliminar.html'
    success_url = reverse_lazy('inventory:listado')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Componente eliminado correctamente.')
        return super().delete(request, *args, **kwargs)


# Atajos compatibles con vistas basadas en funciones antiguas (opcional)
# Si el proyecto usa nombres de vista anteriores en templates, se pueden exponer funciones wrapper.

def listado_inventario(request):
    """Compatibilidad: redirige a la vista basada en clases."""
    view = ComponenteListView.as_view()
    return view(request)


def detalle_componente(request, pk):
    """Compatibilidad: detalle vía CBV."""
    view = ComponenteDetailView.as_view()
    return view(request, pk=pk)


def crear_componente(request):
    """Compatibilidad: crear vía CBV."""
    view = ComponenteCreateView.as_view()
    return view(request)


def editar_componente(request, pk):
    """Compatibilidad: editar vía CBV."""
    view = ComponenteUpdateView.as_view()
    return view(request, pk=pk)


def eliminar_componente(request, pk):
    """Compatibilidad: eliminar vía CBV."""
    view = ComponenteDeleteView.as_view()
    return view(request, pk=pk)


# Gestión de categorías (compatibilidad con inventory/urls.py)

@login_required
@admin_required
def gestionar_categorias(request):
    """Gestión de categorías con creación simple desde formulario."""
    initial_categories = []
    if not Categoria.objects.exists():
        initial_names = [
            'Procesadores',
            'Tarjetas madre',
            'Memorias RAM',
            'Discos duros',
            'Tarjetas gráficas',
        ]
        initial_categories = [Categoria(nombre=name) for name in initial_names]
        Categoria.objects.bulk_create(initial_categories)
        messages.info(request, 'Se han creado categorías iniciales para comenzar a registrar componentes.')

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            messages.success(request, f'Categoría "{categoria.nombre}" creada correctamente.')
            return redirect('inventory:categorias')
    else:
        form = CategoriaForm()

    categorias = Categoria.objects.order_by('nombre')
    return render(
        request,
        'inventory/categorias.html',
        {
            'form': form,
            'categorias': categorias,
        }
    )
