from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Zona


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'created_at']
    list_filter = ['activa']
    search_fields = ['nombre']


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'cedula', 'nombre_completo', 'rol', 'activo']
    list_filter = ['rol', 'activo']
    search_fields = ['username', 'cedula', 'first_name', 'last_name']
    fieldsets = UserAdmin.fieldsets + (
        ('Información adicional', {
            'fields': ('rol', 'cedula', 'telefono', 'foto', 'zonas_permitidas', 'activo'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información adicional', {
            'fields': ('rol', 'cedula', 'telefono', 'foto'),
        }),
    )
    filter_horizontal = ['zonas_permitidas', 'groups', 'user_permissions']
