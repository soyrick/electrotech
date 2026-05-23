from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from inventory.models import Categoria, Componente
from movements.models import Movimiento, DetalleMovimiento


class MetricsViewsTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='testpass123',
            rol=User.Rol.SUPER_ADMIN,
        )

        categoria = Categoria.objects.create(nombre='Tarjetas madre')
        componente = Componente.objects.create(
            nombre='Placa base ASUS',
            categoria=categoria,
            marca='ASUS',
            modelo='Prime B650',
            serial='ASUS-12345',
            cantidad=5,
            ubicacion='Estante A1',
        )

        ingreso = Movimiento.objects.create(
            tipo=Movimiento.Tipo.INGRESO,
            numero_planilla='',
            usuario=self.user,
            nombre_persona='Julio Martínez',
            cedula='10203040',
            cargo='Técnico',
            departamento='Almacén',
        )
        ingreso.generar_numero_planilla()
        detalle_ingreso = DetalleMovimiento(
            movimiento=ingreso,
            componente=componente,
            cantidad=3,
        )
        detalle_ingreso.guardar_snapshot()
        detalle_ingreso.save()

        egreso = Movimiento.objects.create(
            tipo=Movimiento.Tipo.EGRESO,
            numero_planilla='',
            usuario=self.user,
            nombre_persona='Ana Pérez',
            cedula='50506070',
            cargo='Operadora',
            departamento='Producción',
        )
        egreso.generar_numero_planilla()
        detalle_egreso = DetalleMovimiento(
            movimiento=egreso,
            componente=componente,
            cantidad=1,
        )
        detalle_egreso.guardar_snapshot()
        detalle_egreso.save()

        self.client.force_login(self.user)

    def test_dashboard_view_accessible(self):
        response = self.client.get(reverse('metrics:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard — ElectroTech')

    def test_metricas_graficas_view_renders(self):
        response = self.client.get(reverse('metrics:graficas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Métricas de Inventario')

    def test_api_datos_grafica_returns_json(self):
        response = self.client.get(reverse('metrics:api_datos_grafica'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = response.json()
        self.assertIn('labels', data)
        self.assertIn('ingresos', data)
        self.assertIn('egresos', data)
        self.assertIn('resumen', data)

    def test_historial_view_renders(self):
        response = self.client.get(reverse('metrics:historial'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Historial de Movimientos')

    def test_ver_planilla_historica_renders(self):
        movimiento = Movimiento.objects.first()
        response = self.client.get(reverse('metrics:ver_planilla', kwargs={'pk': movimiento.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, movimiento.numero_planilla)
