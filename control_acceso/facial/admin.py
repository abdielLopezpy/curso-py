from django.contrib import admin
from .models import EncodingFacial


@admin.register(EncodingFacial)
class EncodingFacialAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'created_at']
    list_filter = ['created_at']
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__cedula']
    readonly_fields = ['encoding', 'created_at']
