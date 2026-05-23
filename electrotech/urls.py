"""
Configuración de rutas URL principales para el proyecto ElectroTech.
Incluye las rutas de las apps: accounts, inventory, movements, metrics.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import RegistrarUsuarioView

urlpatterns = [
    # Panel de administración de Django (acceso opcional)
    path('admin/', admin.site.urls),
    
    # Ruta pública de registro directa
    path('register/', RegistrarUsuarioView.as_view(), name='register'),

    # Autenticación y gestión de usuarios (accounts)
    path('cuentas/', include('accounts.urls')),
    
    # Inventario: catálogo, componentes, categorías (inventory)
    path('inventario/', include('inventory.urls')),
    
    # Movimientos: ingresos, egresos, planillas (movements)
    path('movimientos/', include('movements.urls')),
    
    # Métricas, dashboard e historial (metrics)
    path('metricas/', include('metrics.urls')),
    
    # Dashboard principal (redirige a metrics que lo contiene)
    path('', include('metrics.urls_dashboard')),
]

# Servir archivos multimedia en modo DEBUG (desarrollo)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
