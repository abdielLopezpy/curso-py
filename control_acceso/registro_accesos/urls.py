from django.urls import path
from . import views

urlpatterns = [
    path('historial/', views.historial_accesos, name='historial_accesos'),
    path('reportes/', views.reportes, name='reportes'),
]
