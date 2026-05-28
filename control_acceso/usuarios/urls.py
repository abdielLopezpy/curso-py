from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/<int:pk>/', views.detalle_usuario, name='detalle_usuario'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('zonas/', views.lista_zonas, name='lista_zonas'),
    path('zonas/crear/', views.crear_zona, name='crear_zona'),
    path('zonas/<int:pk>/editar/', views.editar_zona, name='editar_zona'),
]
