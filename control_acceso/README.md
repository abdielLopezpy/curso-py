# Sistema de Control de Acceso con Reconocimiento Facial

Proyecto final del curso de Desarrollo Backend con Python y Django.

## Descripción

Sistema web que controla el acceso a zonas restringidas mediante reconocimiento facial. Permite registrar usuarios, asignar permisos por zona, verificar identidad por cámara y mantener un historial detallado de accesos.

## Funcionalidades

- Autenticación y roles (admin, supervisor, vigilante, empleado)
- Gestión de usuarios y zonas con permisología
- Registro de rostros vía cámara web
- Punto de acceso con verificación facial en tiempo real
- Historial de accesos con filtros (usuario, zona, fecha, estado)
- Dashboard con estadísticas
- Reportes semanales y mensuales por zona
- API REST con DRF

## Stack

- Python 3.12
- Django 6.0
- Django REST Framework
- OpenCV + face_recognition
- SQLite (desarrollo)
- Bootstrap 5

## Instalación

```bash
python -m venv venv_acceso
venv_acceso\Scripts\activate
pip install -r requirements.txt
pip install "setuptools<81"
pip install "git+https://github.com/ageitgey/face_recognition_models"
python manage.py migrate
python cargar_datos.py
python manage.py runserver
```

## Credenciales de prueba

- `admin / admin123` - Administrador
- `mlopez / demo1234` - Supervisor
- `jperez / demo1234` - Empleado

## Estructura

- `usuarios/` - Modelo de Usuario, Zonas y permisología
- `registro_accesos/` - Registro e historial de accesos
- `facial/` - Reconocimiento facial (registro y verificación)
- `api_rest/` - API REST con DRF
