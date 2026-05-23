"""
Modelos de la aplicación 'movements'.
Gestiona los ingresos, egresos y el historial de movimientos del inventario.
Cada movimiento tiene un detalle que guarda una "foto" (snapshot) del componente al momento del movimiento.
"""

from django.db import models
from django.conf import settings
from inventory.models import Componente


class Movimiento(models.Model):
    """
    Registro de un movimiento de inventario (ingreso o egreso).
    Puede contener uno o varios componentes mediante DetalleMovimiento.
    """
    
    class Tipo(models.TextChoices):
        """Tipos de movimiento posibles."""
        INGRESO = 'ING', 'Ingreso'
        EGRESO = 'EGR', 'Egreso'
    
    tipo = models.CharField(
        max_length=3,
        choices=Tipo.choices,
        verbose_name='Tipo de movimiento'
    )
    numero_planilla = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de planilla',
        help_text='Numeración automática: ING-0001, EGR-0001, etc.'
    )
    fecha_hora = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y hora del movimiento'
    )
    
    # Usuario del sistema que realizó el movimiento
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='movimientos',
        verbose_name='Usuario que registró el movimiento'
    )
    
    # Datos de la persona externa (encargado que ingresa o persona que retira)
    nombre_persona = models.CharField(
        max_length=200,
        verbose_name='Nombre de la persona',
        help_text='Encargado que entrega el componente o persona que lo retira.'
    )
    cedula = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Cédula / ID',
        help_text='Documento de identidad de la persona. Requerido en egresos.'
    )
    cargo = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Cargo',
        help_text='Cargo o puesto de la persona.'
    )
    departamento = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Departamento',
        help_text='Departamento al que pertenece (solo para egresos).'
    )
    # Soft-delete fields
    eliminado = models.BooleanField(default=False, verbose_name='Eliminado')
    eliminado_en = models.DateTimeField(null=True, blank=True, verbose_name='Eliminado en')
    eliminado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='movimientos_eliminados',
        verbose_name='Eliminado por'
    )
    
    def __str__(self):
        return f"{self.numero_planilla} - {self.get_tipo_display()} ({self.fecha_hora.strftime('%d/%m/%Y %H:%M')})"
    
    @property
    def es_ingreso(self):
        return self.tipo == self.Tipo.INGRESO
    
    @property
    def es_egreso(self):
        return self.tipo == self.Tipo.EGRESO
    
    def generar_numero_planilla(self):
        """
        Genera el número de planilla automáticamente basado en el tipo y el ID.
        Formato: ING-XXXX o EGR-XXXX (relleno con ceros a 4 dígitos).
        Se llama después de guardar el movimiento por primera vez.
        """
        if not self.numero_planilla:
            prefijo = 'ING' if self.tipo == self.Tipo.INGRESO else 'EGR'
            # El ID existe después del primer save()
            self.numero_planilla = f"{prefijo}-{self.pk:04d}"
            self.save(update_fields=['numero_planilla'])
    
    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['tipo']),
            models.Index(fields=['fecha_hora']),
        ]


class DetalleMovimiento(models.Model):
    """
    Detalle de cada componente involucrado en un movimiento.
    Guarda un 'snapshot' de los datos del componente al momento del movimiento
    para mantener integridad histórica aunque el componente sea editado después.
    """
    movimiento = models.ForeignKey(
        Movimiento,
        on_delete=models.CASCADE,
        related_name='detalles',
        verbose_name='Movimiento'
    )
    componente = models.ForeignKey(
        Componente,
        on_delete=models.PROTECT,
        related_name='detalles_movimiento',
        verbose_name='Componente'
    )
    cantidad = models.PositiveIntegerField(
        verbose_name='Cantidad',
        help_text='Cantidad de unidades involucradas en este movimiento.'
    )
    
    # Snapshot: copia de los datos del componente en el momento del movimiento
    snapshot_nombre = models.CharField(max_length=200, verbose_name='Nombre (histórico)')
    snapshot_categoria = models.CharField(max_length=100, verbose_name='Categoría (histórico)')
    snapshot_marca = models.CharField(max_length=100, verbose_name='Marca (histórico)')
    snapshot_modelo = models.CharField(max_length=100, verbose_name='Modelo (histórico)')
    snapshot_serial = models.CharField(max_length=100, verbose_name='Serial (histórico)')
    snapshot_detalles = models.TextField(blank=True, verbose_name='Detalles (histórico)')
    snapshot_ubicacion = models.CharField(max_length=100, verbose_name='Ubicación (histórico)')
    
    def __str__(self):
        return f"{self.componente.nombre} x{self.cantidad} en {self.movimiento.numero_planilla}"
    
    def guardar_snapshot(self):
        """
        Guarda una copia de los datos actuales del componente
        para mantener el registro histórico exacto.
        """
        comp = self.componente
        self.snapshot_nombre = comp.nombre
        self.snapshot_categoria = comp.categoria.nombre
        self.snapshot_marca = comp.marca
        self.snapshot_modelo = comp.modelo
        self.snapshot_serial = comp.serial
        self.snapshot_detalles = comp.detalles
        self.snapshot_ubicacion = comp.ubicacion
    
    class Meta:
        verbose_name = 'Detalle de movimiento'
        verbose_name_plural = 'Detalles de movimientos'
        ordering = ['movimiento', 'id']
