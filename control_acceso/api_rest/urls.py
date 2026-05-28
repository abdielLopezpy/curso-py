from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'usuarios', views.UsuarioViewSet)
router.register(r'zonas', views.ZonaViewSet)
router.register(r'accesos', views.RegistroAccesoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
