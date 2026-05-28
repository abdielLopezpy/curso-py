from django.urls import path
from . import views

urlpatterns = [
    path('registrar/<int:usuario_id>/', views.registrar_rostro, name='registrar_rostro'),
    path('punto-acceso/', views.punto_acceso, name='punto_acceso'),
    path('verificar/', views.verificar_rostro, name='verificar_rostro'),
]
