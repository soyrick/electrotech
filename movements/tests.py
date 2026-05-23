from django.test import TestCase
from django.contrib.auth import get_user_model

from inventory.models import Categoria, Componente
from movements.models import Movimiento, DetalleMovimiento
from movements.utils import generar_comprobante_pdf
from movements.forms import IngresoForm


class ComprobantePdfTests(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.user = self.UserModel.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='adminpass',
            rol='admin'
        )
        self.categoria = Categoria.objects.create(nombre='Tarjetas gráficas')
        self.componente = Componente.objects.create(
            nombre='RTX 4080',
            categoria=self.categoria,
            marca='NVIDIA',
            modelo='RTX 4080',
            serial='SN12345',
            detalles='GPU de alto rendimiento',
            cantidad=2,
            ubicacion='Estante A1',
        )

    def test_generar_comprobante_pdf(self):
        movimiento = Movimiento.objects.create(
            tipo=Movimiento.Tipo.INGRESO,
            numero_planilla='ING-0001',
            usuario=self.user,
            nombre_persona='Ana Pérez',
            cedula='T1234567',
            cargo='Técnico de Almacén',
            departamento='Mantenimiento',
        )

        detalle = DetalleMovimiento.objects.create(
            movimiento=movimiento,
            componente=self.componente,
            cantidad=2,
            snapshot_nombre=self.componente.nombre,
            snapshot_categoria=self.componente.categoria.nombre,
            snapshot_marca=self.componente.marca,
            snapshot_modelo=self.componente.modelo,
            snapshot_serial=self.componente.serial,
            snapshot_detalles=self.componente.detalles,
            snapshot_ubicacion=self.componente.ubicacion,
        )

        response = generar_comprobante_pdf(movimiento)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

        content = b''.join(response.streaming_content)
        self.assertTrue(content.startswith(b'%PDF'))
        self.assertGreater(len(content), 1000)
        self.assertIn(b'/Producer', content)

    def test_ingreso_form_cedula_prefix_and_numeric_validation(self):
        form = IngresoForm(data={
            'componente': self.componente.pk,
            'cantidad': 1,
            'nombre_persona': 'Juan Pérez',
            'cedula_prefijo': 'V',
            'cedula': '12345678',
            'cargo': 'Técnico',
            'departamento': 'Almacén',
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['cedula'], 'V-12345678')

        invalid_form = IngresoForm(data={
            'componente': self.componente.pk,
            'cantidad': 1,
            'nombre_persona': 'Juan Pérez',
            'cedula_prefijo': 'V',
            'cedula': '12A45678',
            'cargo': 'Técnico',
            'departamento': 'Almacén',
        })
        self.assertFalse(invalid_form.is_valid())
        self.assertIn('cedula', invalid_form.errors)
