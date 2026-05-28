"""Script para cargar datos iniciales de prueba."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'control_acceso.settings')
django.setup()

from usuarios.models import Usuario, Zona


def crear_superusuario():
    if not Usuario.objects.filter(username='admin').exists():
        admin = Usuario.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@control.com',
            first_name='Administrador',
            last_name='Sistema',
            cedula='V-00000000',
            rol='admin',
        )
        print(f'[OK] Superusuario creado: admin / admin123')
    else:
        print('[INFO] Superusuario ya existe.')


def crear_zonas():
    zonas = [
        ('Entrada Principal', 'Acceso principal al edificio'),
        ('Oficinas Administrativas', 'Área de oficinas y administración'),
        ('Almacén', 'Bodega de inventario'),
        ('Sala de Servidores', 'Zona restringida - solo IT'),
        ('Estacionamiento', 'Área de estacionamiento de empleados'),
    ]
    for nombre, desc in zonas:
        zona, creada = Zona.objects.get_or_create(nombre=nombre, defaults={'descripcion': desc})
        if creada:
            print(f'[OK] Zona creada: {nombre}')
        else:
            print(f'[INFO] Zona ya existe: {nombre}')


def crear_usuarios_ejemplo():
    usuarios_data = [
        {'username': 'jperez', 'password': 'demo1234', 'first_name': 'Juan', 'last_name': 'Pérez',
         'cedula': 'V-12345678', 'rol': 'empleado', 'email': 'jperez@empresa.com'},
        {'username': 'mlopez', 'password': 'demo1234', 'first_name': 'María', 'last_name': 'López',
         'cedula': 'V-23456789', 'rol': 'supervisor', 'email': 'mlopez@empresa.com'},
        {'username': 'crodriguez', 'password': 'demo1234', 'first_name': 'Carlos', 'last_name': 'Rodríguez',
         'cedula': 'V-34567890', 'rol': 'vigilante', 'email': 'crodriguez@empresa.com'},
    ]
    todas_zonas = Zona.objects.all()
    for data in usuarios_data:
        if not Usuario.objects.filter(username=data['username']).exists():
            usuario = Usuario.objects.create_user(**data)
            if usuario.rol in ('supervisor', 'vigilante'):
                usuario.zonas_permitidas.set(todas_zonas)
            else:
                usuario.zonas_permitidas.set(todas_zonas[:2])
            print(f'[OK] Usuario creado: {data["username"]} / demo1234 ({data["rol"]})')
        else:
            print(f'[INFO] Usuario ya existe: {data["username"]}')


if __name__ == '__main__':
    print('\n=== Cargando datos iniciales ===\n')
    crear_superusuario()
    crear_zonas()
    crear_usuarios_ejemplo()
    print('\n=== Listo! Accede en http://127.0.0.1:8000 ===')
    print('   Login admin: admin / admin123')
    print('   Login supervisor: mlopez / demo1234\n')
