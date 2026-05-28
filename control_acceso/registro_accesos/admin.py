from django.contrib import admin
from .models import RegistroAcceso


@admin.register(RegistroAcceso)
class RegistroAccesoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'zona', 'tipo', 'autorizado', 'metodo', 'confianza', 'fecha_hora']
    list_filter = ['autorizado', 'tipo', 'metodo', 'zona', 'fecha_hora']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__cedula']
    readonly_fields = ['fecha_hora']
    date_hierarchy = 'fecha_hora'
