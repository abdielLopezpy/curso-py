from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

from usuarios.models import Usuario, Zona
from registro_accesos.models import RegistroAcceso
from .serializers import UsuarioSerializer, ZonaSerializer, RegistroAccesoSerializer


class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'cedula', 'username']


class ZonaViewSet(viewsets.ModelViewSet):
    queryset = Zona.objects.all()
    serializer_class = ZonaSerializer


class RegistroAccesoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegistroAcceso.objects.select_related('usuario', 'zona').all()
    serializer_class = RegistroAccesoSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['usuario__first_name', 'usuario__last_name', 'usuario__cedula']

    @action(detail=False, methods=['get'])
    def resumen_hoy(self, request):
        hoy = timezone.now().date()
        accesos = RegistroAcceso.objects.filter(fecha_hora__date=hoy)
        return Response({
            'fecha': str(hoy),
            'total': accesos.count(),
            'permitidos': accesos.filter(autorizado=True).count(),
            'denegados': accesos.filter(autorizado=False).count(),
        })
