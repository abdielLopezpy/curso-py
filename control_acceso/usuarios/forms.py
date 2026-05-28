from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Zona


class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'email',
            'cedula', 'telefono', 'rol', 'foto', 'zonas_permitidas',
        ]
        widgets = {
            'zonas_permitidas': forms.CheckboxSelectMultiple,
        }


class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'first_name', 'last_name', 'email',
            'cedula', 'telefono', 'rol', 'foto', 'zonas_permitidas', 'activo',
        ]
        widgets = {
            'zonas_permitidas': forms.CheckboxSelectMultiple,
        }


class ZonaForm(forms.ModelForm):
    class Meta:
        model = Zona
        fields = ['nombre', 'descripcion', 'activa']
