from django.contrib.auth.models import AbstractUser
from django.db import models


class Zona(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        SUPERVISOR = 'supervisor', 'Supervisor'
        VIGILANTE = 'vigilante', 'Vigilante'
        EMPLEADO = 'empleado', 'Empleado'

    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.EMPLEADO)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    zonas_permitidas = models.ManyToManyField(Zona, blank=True, related_name='usuarios')
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.cedula})"

    @property
    def nombre_completo(self):
        return self.get_full_name() or self.username

    @property
    def tiene_encoding_facial(self):
        return self.encodings_faciales.exists()
