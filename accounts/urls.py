"""
Rutas de la aplicación 'accounts'.
Gestión de autenticación (login, logout) y administración de usuarios.
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.RegistrarUsuarioView.as_view(), name='registro'),
    
    # Gestión de administradores (solo super-admin)
    path('crear-admin/', views.crear_admin, name='crear_admin'),
    path('cambiar-password/', views.cambiar_password, name='cambiar_password'),
    
    # Página de error de permisos
    path('permiso-denegado/', views.permiso_denegado, name='permiso_denegado'),
]
