from rest_framework import serializers
from usuarios.models import Usuario, Zona
from registro_accesos.models import RegistroAcceso


class ZonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zona
        fields = ['id', 'nombre', 'descripcion', 'activa', 'created_at']


class UsuarioSerializer(serializers.ModelSerializer):
    zonas_permitidas = ZonaSerializer(many=True, read_only=True)
    tiene_encoding_facial = serializers.BooleanField(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'cedula', 'telefono', 'rol', 'activo',
            'zonas_permitidas', 'tiene_encoding_facial',
            'created_at', 'updated_at',
        ]


class RegistroAccesoSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.nombre_completo', read_only=True, default='Desconocido')
    zona_nombre = serializers.CharField(source='zona.nombre', read_only=True, default='')

    class Meta:
        model = RegistroAcceso
        fields = [
            'id', 'usuario', 'usuario_nombre', 'zona', 'zona_nombre',
            'tipo', 'autorizado', 'metodo', 'confianza',
            'observacion', 'fecha_hora',
        ]
