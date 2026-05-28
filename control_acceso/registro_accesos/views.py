from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta

from .models import RegistroAcceso
from usuarios.decorators import rol_requerido


@login_required
@rol_requerido('admin', 'supervisor', 'vigilante')
def historial_accesos(request):
    accesos = RegistroAcceso.objects.select_related('usuario', 'zona')

    q = request.GET.get('q', '')
    zona = request.GET.get('zona', '')
    autorizado = request.GET.get('autorizado', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    if q:
        accesos = accesos.filter(
            Q(usuario__first_name__icontains=q) |
            Q(usuario__last_name__icontains=q) |
            Q(usuario__cedula__icontains=q)
        )
    if zona:
        accesos = accesos.filter(zona_id=zona)
    if autorizado:
        accesos = accesos.filter(autorizado=autorizado == 'true')
    if fecha_desde:
        accesos = accesos.filter(fecha_hora__date__gte=fecha_desde)
    if fecha_hasta:
        accesos = accesos.filter(fecha_hora__date__lte=fecha_hasta)

    from usuarios.models import Zona
    context = {
        'accesos': accesos[:100],
        'zonas': Zona.objects.filter(activa=True),
        'query': q,
        'zona_filtro': zona,
        'autorizado_filtro': autorizado,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    }
    return render(request, 'registro_accesos/historial.html', context)


@login_required
@rol_requerido('admin', 'supervisor')
def reportes(request):
    hoy = timezone.now().date()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    inicio_mes = hoy.replace(day=1)

    accesos_semana = RegistroAcceso.objects.filter(fecha_hora__date__gte=inicio_semana)
    accesos_mes = RegistroAcceso.objects.filter(fecha_hora__date__gte=inicio_mes)

    por_zona = (
        RegistroAcceso.objects
        .filter(fecha_hora__date__gte=inicio_mes)
        .values('zona__nombre')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    context = {
        'accesos_semana': accesos_semana.count(),
        'permitidos_semana': accesos_semana.filter(autorizado=True).count(),
        'denegados_semana': accesos_semana.filter(autorizado=False).count(),
        'accesos_mes': accesos_mes.count(),
        'permitidos_mes': accesos_mes.filter(autorizado=True).count(),
        'denegados_mes': accesos_mes.filter(autorizado=False).count(),
        'por_zona': por_zona,
    }
    return render(request, 'registro_accesos/reportes.html', context)
