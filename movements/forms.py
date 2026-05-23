from django import forms
from django.core.exceptions import ValidationError

from inventory.models import Componente
from .models import Movimiento, DetalleMovimiento


class BaseMovimientoForm(forms.Form):
    componente = forms.ModelChoiceField(
        queryset=Componente.objects.all(),
        label='Componente',
        widget=forms.Select(attrs={'class': 'dark-select'})
    )
    cantidad = forms.IntegerField(
        min_value=1,
        label='Cantidad',
        widget=forms.NumberInput(attrs={'class': 'dark-input', 'min': 1})
    )
    nombre_persona = forms.CharField(
        label='Nombre de la persona',
        widget=forms.TextInput(attrs={'class': 'dark-input'})
    )
    cedula_prefijo = forms.ChoiceField(
        choices=[
            ('', 'Seleccione'),
            ('V', 'V - Venezolano'),
            ('E', 'E - Extranjero'),
            ('J', 'J - Jurídico'),
        ],
        label='Tipo de documento',
        required=False,
        widget=forms.Select(attrs={'class': 'dark-select'})
    )
    cedula = forms.CharField(
        label='Número de cédula',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'dark-input',
            'inputmode': 'numeric',
            'pattern': '[0-9]*',
            'placeholder': 'Solo dígitos',
        })
    )
    usar_fecha_hora = forms.BooleanField(
        label='Usar fecha/hora personalizada',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'dark-checkbox', 'id': 'id_usar_fecha_hora'})
    )
    fecha_personalizada = forms.DateField(
        label='Fecha (DD/MM/AAAA)',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'dark-input custom-datetime'})
    )
    hora_personalizada = forms.TimeField(
        label='Hora (HH:MM)',
        required=False,
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'dark-input custom-datetime'})
    )
    cargo = forms.CharField(
        label='Cargo',
        required=False,
        widget=forms.TextInput(attrs={'class': 'dark-input'})
    )

    def clean(self):
        cleaned = super().clean()
        cedula_prefijo = cleaned.get('cedula_prefijo', '')
        cedula_numero = cleaned.get('cedula', '')

        if cedula_prefijo or cedula_numero:
            if not cedula_prefijo:
                self.add_error('cedula_prefijo', 'Seleccione el tipo de documento.')
            if not cedula_numero:
                self.add_error('cedula', 'Ingrese el número de documento.')
            elif not cedula_numero.isdigit():
                self.add_error('cedula', 'La cédula solo debe contener números.')
            else:
                cleaned['cedula'] = f"{cedula_prefijo}-{cedula_numero}"

        # Manejo de fecha/hora personalizada
        usar_fecha = cleaned.get('usar_fecha_hora')
        fecha_personalizada = cleaned.get('fecha_personalizada')
        hora_personalizada = cleaned.get('hora_personalizada')
        if usar_fecha:
            if not fecha_personalizada:
                self.add_error('fecha_personalizada', 'Seleccione la fecha.')
            if not hora_personalizada:
                self.add_error('hora_personalizada', 'Seleccione la hora.')
            if fecha_personalizada and hora_personalizada:
                # Construir objeto datetime y colocar en cleaned
                from datetime import datetime
                dt = datetime.combine(fecha_personalizada, hora_personalizada)
                cleaned['fecha_hora'] = dt

        return cleaned
    departamento = forms.CharField(
        label='Departamento',
        required=False,
        widget=forms.TextInput(attrs={'class': 'dark-input'})
    )


class IngresoForm(BaseMovimientoForm):
    """Formulario para registrar ingresos.

    El método save(user) crea Movimiento y DetalleMovimiento, actualiza el stock
    del componente y devuelve la instancia de Movimiento creada.
    """

    def save(self, user):
        data = self.cleaned_data
        componente = data['componente']
        cantidad = data['cantidad']
        cedula_text = data.get('cedula', '')

        # Crear movimiento
        movimiento = Movimiento.objects.create(
            tipo=Movimiento.Tipo.INGRESO,
            numero_planilla='',
            usuario=user,
            nombre_persona=data.get('nombre_persona', ''),
            cedula=cedula_text,
            cargo=data.get('cargo', ''),
            departamento=data.get('departamento', ''),
        )
        # Generar número de planilla (usa pk)
        movimiento.generar_numero_planilla()

        # Si se proporcionó fecha/hora personalizada, actualizarla
        fecha_hora_custom = data.get('fecha_hora') or data.get('fecha_hora')
        if data.get('fecha_hora'):
            movimiento.fecha_hora = data.get('fecha_hora')
            movimiento.save(update_fields=['fecha_hora'])

        # Crear detalle y snapshot
        detalle = DetalleMovimiento(
            movimiento=movimiento,
            componente=componente,
            cantidad=cantidad,
        )
        detalle.guardar_snapshot()
        detalle.save()

        # Actualizar stock (campo 'cantidad' en Componente)
        componente.cantidad = (componente.cantidad or 0) + cantidad
        componente.save(update_fields=['cantidad'])

        return movimiento


class EgresoForm(BaseMovimientoForm):
    motivo = forms.CharField(
        label='Motivo',
        required=False,
        widget=forms.Textarea(attrs={'class': 'dark-textarea'})
    )

    def clean(self):
        cleaned = super().clean()
        componente = cleaned.get('componente')
        cantidad = cleaned.get('cantidad')
        if componente and cantidad is not None:
            if cantidad > (componente.cantidad or 0):
                raise ValidationError({'cantidad': 'La cantidad solicitada excede el stock disponible.'})
        return cleaned

    def save(self, user):
        data = self.cleaned_data
        componente = data['componente']
        cantidad = data['cantidad']
        cedula_text = data.get('cedula', '')

        # Crear movimiento de egreso
        movimiento = Movimiento.objects.create(
            tipo=Movimiento.Tipo.EGRESO,
            numero_planilla='',
            usuario=user,
            nombre_persona=data.get('nombre_persona', ''),
            cedula=cedula_text,
            cargo=data.get('cargo', ''),
            departamento=data.get('departamento', ''),
        )
        movimiento.generar_numero_planilla()

        # Aplicar fecha/hora personalizada si se indicó
        if data.get('fecha_hora'):
            movimiento.fecha_hora = data.get('fecha_hora')
            movimiento.save(update_fields=['fecha_hora'])

        # Crear detalle y snapshot
        detalle = DetalleMovimiento(
            movimiento=movimiento,
            componente=componente,
            cantidad=cantidad,
        )
        detalle.guardar_snapshot()
        detalle.save()

        # Restar del stock
        componente.cantidad = (componente.cantidad or 0) - cantidad
        if componente.cantidad < 0:
            componente.cantidad = 0
        componente.save(update_fields=['cantidad'])

        return movimiento
