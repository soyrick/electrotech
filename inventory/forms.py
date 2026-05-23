from django import forms
from django.core.exceptions import ValidationError
from .models import Componente, Categoria


class ComponenteForm(forms.ModelForm):
    """Form para crear/editar Componente.

    - aplica clases del sistema de diseño (dark-input, dark-select)
    - valida que serial sea único (excluye la instancia actual)
    - valida que cantidad sea >= 0
    - muestra fecha_ingreso como campo de solo lectura (no editable)
    """

    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'class': 'dark-select'}),
        empty_label='-- Seleccionar categoría --',
        label='Categoría'
    )

    imagen = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'dark-input'}),
        label='Imagen (opcional)'
    )

    fecha_ingreso = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'class': 'dark-input', 'readonly': 'readonly'}),
        label='Fecha de ingreso'
    )

    class Meta:
        model = Componente
        fields = [
            'nombre', 'categoria', 'marca', 'modelo', 'serial',
            'detalles', 'cantidad', 'ubicacion', 'imagen'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'dark-input', 'placeholder': 'Nombre del componente'}),
            'marca': forms.TextInput(attrs={'class': 'dark-input', 'placeholder': 'Marca'}),
            'modelo': forms.TextInput(attrs={'class': 'dark-input', 'placeholder': 'Modelo'}),
            'serial': forms.TextInput(attrs={'class': 'dark-input', 'placeholder': 'Serial único'}),
            'detalles': forms.Textarea(attrs={'class': 'dark-textarea', 'placeholder': 'Detalles o especificaciones'}),
            'cantidad': forms.NumberInput(attrs={'class': 'dark-input', 'min': 0}),
            'ubicacion': forms.TextInput(attrs={'class': 'dark-input', 'placeholder': 'Ubicación en el almacén'}),
        }
        labels = {
            'nombre': 'Nombre',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'serial': 'Serial',
            'detalles': 'Detalles',
            'cantidad': 'Cantidad',
            'ubicacion': 'Ubicación',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si la instancia existe, mostrar fecha_ingreso en el campo (read-only)
        if self.instance and getattr(self.instance, 'fecha_ingreso', None):
            self.fields['fecha_ingreso'].initial = self.instance.fecha_ingreso
            # deshabilitar edición en formularios
            self.fields['fecha_ingreso'].disabled = True

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is None:
            return 0
        if cantidad < 0:
            raise ValidationError('La cantidad no puede ser negativa.')
        return cantidad

    def clean_serial(self):
        serial = self.cleaned_data.get('serial')
        if not serial:
            return serial
        qs = Componente.objects.filter(serial__iexact=serial)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('El número de serie ya existe para otro componente.')
        return serial


class CategoriaForm(forms.ModelForm):
    """Form para crear nuevas categorías de inventario."""

    class Meta:
        model = Categoria
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'dark-input',
                    'placeholder': 'Nombre de la categoría'
                }
            )
        }
        labels = {
            'nombre': 'Nombre de categoría'
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise ValidationError('Debe ingresar un nombre para la categoría.')
        if Categoria.objects.filter(nombre__iexact=nombre).exists():
            raise ValidationError('Ya existe una categoría con ese nombre.')
        return nombre
