from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from .models import Usuario, Zona
from .forms import UsuarioForm, UsuarioEditForm, ZonaForm
from .decorators import rol_requerido
from registro_accesos.models import RegistroAcceso


@login_required
def dashboard(request):
    hoy = timezone.now().date()
    accesos_hoy = RegistroAcceso.objects.filter(fecha_hora__date=hoy)

    context = {
        'total_usuarios': Usuario.objects.filter(activo=True).count(),
        'total_zonas': Zona.objects.filter(activa=True).count(),
        'accesos_hoy': accesos_hoy.count(),
        'accesos_permitidos_hoy': accesos_hoy.filter(autorizado=True).count(),
        'accesos_denegados_hoy': accesos_hoy.filter(autorizado=False).count(),
        'ultimos_accesos': RegistroAcceso.objects.select_related('usuario', 'zona').order_by('-fecha_hora')[:10],
    }
    return render(request, 'usuarios/dashboard.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'usuarios/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@rol_requerido('admin', 'supervisor')
def lista_usuarios(request):
    q = request.GET.get('q', '')
    rol = request.GET.get('rol', '')
    usuarios = Usuario.objects.all()
    if q:
        usuarios = usuarios.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(cedula__icontains=q) |
            Q(username__icontains=q)
        )
    if rol:
        usuarios = usuarios.filter(rol=rol)
    context = {
        'usuarios': usuarios,
        'query': q,
        'rol_filtro': rol,
        'roles': Usuario.Rol.choices,
    }
    return render(request, 'usuarios/lista_usuarios.html', context)


@login_required
@rol_requerido('admin')
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/form_usuario.html', {'form': form, 'titulo': 'Crear Usuario'})


@login_required
@rol_requerido('admin')
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioEditForm(instance=usuario)
    return render(request, 'usuarios/form_usuario.html', {'form': form, 'titulo': 'Editar Usuario', 'usuario': usuario})


@login_required
@rol_requerido('admin')
def detalle_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    accesos = RegistroAcceso.objects.filter(usuario=usuario).order_by('-fecha_hora')[:20]
    context = {
        'usuario': usuario,
        'accesos': accesos,
    }
    return render(request, 'usuarios/detalle_usuario.html', context)


@login_required
@rol_requerido('admin', 'supervisor')
def lista_zonas(request):
    zonas = Zona.objects.annotate(num_usuarios=Count('usuarios'))
    return render(request, 'usuarios/lista_zonas.html', {'zonas': zonas})


@login_required
@rol_requerido('admin')
def crear_zona(request):
    if request.method == 'POST':
        form = ZonaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zona creada exitosamente.')
            return redirect('lista_zonas')
    else:
        form = ZonaForm()
    return render(request, 'usuarios/form_zona.html', {'form': form, 'titulo': 'Crear Zona'})


@login_required
@rol_requerido('admin')
def editar_zona(request, pk):
    zona = get_object_or_404(Zona, pk=pk)
    if request.method == 'POST':
        form = ZonaForm(request.POST, instance=zona)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zona actualizada exitosamente.')
            return redirect('lista_zonas')
    else:
        form = ZonaForm(instance=zona)
    return render(request, 'usuarios/form_zona.html', {'form': form, 'titulo': 'Editar Zona'})
