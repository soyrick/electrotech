from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Categoria


class CategoriaGestionTests(TestCase):
    def setUp(self):
        self.UserModel = get_user_model()
        self.admin = self.UserModel.objects.create_user(
            email='admin@example.com',
            username='admin',
            password='adminpass',
            rol='admin'
        )
        self.client.login(email='admin@example.com', password='adminpass')

    def test_categorias_page_renders(self):
        response = self.client.get(reverse('inventory:categorias'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/categorias.html')
        self.assertContains(response, 'Gestión de categorías')

    def test_create_categoria(self):
        response = self.client.post(reverse('inventory:categorias'), {'nombre': 'Sensores'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Categoria.objects.filter(nombre='Sensores').exists())

    def test_initial_categories_created_if_empty(self):
        Categoria.objects.all().delete()
        response = self.client.get(reverse('inventory:categorias'))
        self.assertEqual(response.status_code, 200)
        self.assertGreater(Categoria.objects.count(), 0)
