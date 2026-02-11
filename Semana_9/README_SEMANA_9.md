# Semana 9: Autenticación en Flask

## Objetivo
Agregar un sistema completo de autenticación a nuestra aplicación Flask, incluyendo registro, login, protección de rutas y gestión de usuarios.

## Contenido

### Archivos Educativos (ejecutar en orden)

| # | Archivo | Tema |
|---|---------|------|
| 1 | `01_intro_autenticacion.py` | Conceptos de autenticación, hashing de contraseñas con `werkzeug.security` |
| 2 | `02_sesiones_flask.py` | Cómo funcionan las sesiones en Flask, cookies, `session` |
| 3 | `03_decoradores_proteccion.py` | Decoradores `@login_required` y `@admin_required`, protección de rutas |

### Aplicación Principal

| Archivo | Descripción |
|---------|-------------|
| `app_flask.py` | Aplicación completa con autenticación |

## Cómo Ejecutar

```bash
# 1. Ejecutar los ejemplos educativos
python 01_intro_autenticacion.py
python 02_sesiones_flask.py
python 03_decoradores_proteccion.py

# 2. Ejecutar la aplicación principal
python app_flask.py
# Abrir: http://localhost:5003
```

## Credenciales por Defecto

| Campo | Valor |
|-------|-------|
| Email | `admin@ejemplo.com` |
| Password | `admin123` |

## Conceptos Nuevos en Semana 9

### 1. Modelo de Usuario
```python
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    rol = Column(String(20), default='usuario')
    activo = Column(Boolean, default=True)
```

### 2. Hashing de Contraseñas
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Guardar contraseña (al registrar)
usuario.password_hash = generate_password_hash("mi_password")

# Verificar contraseña (al hacer login)
if check_password_hash(usuario.password_hash, "mi_password"):
    print("Contraseña correcta")
```

### 3. Sesiones de Flask
```python
from flask import session

# Guardar datos en la sesión (al hacer login)
session['usuario_id'] = usuario.id
session['usuario_nombre'] = usuario.nombre

# Leer datos de la sesión
nombre = session.get('usuario_nombre')

# Cerrar sesión
session.clear()
```

### 4. Decorador login_required
```python
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesión', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Uso:
@app.route('/ruta-protegida')
@login_required
def mi_ruta():
    # Solo accesible si el usuario está logueado
    ...
```

### 5. Context Processor
```python
@app.context_processor
def inject_user():
    """Inyecta datos del usuario en TODAS las plantillas."""
    if 'usuario_id' in session:
        return {'usuario_actual': usuario, 'esta_logueado': True}
    return {'usuario_actual': None, 'esta_logueado': False}

# En cualquier template:
# {{ usuario_actual.nombre }}
# {% if esta_logueado %}...{% endif %}
```

## Rutas de la Aplicación

### Rutas Públicas
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/login` | GET, POST | Iniciar sesión |
| `/registro` | GET, POST | Crear cuenta |
| `/logout` | GET | Cerrar sesión |

### Rutas Protegidas (requieren login)
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Página principal con estadísticas |
| `/perfil` | GET | Ver perfil del usuario |
| `/perfil/editar` | GET, POST | Editar nombre y email |
| `/perfil/cambiar-password` | GET, POST | Cambiar contraseña |
| `/categorias` | GET | Lista de categorías |
| `/categorias/nueva` | GET, POST | Crear categoría |
| `/categorias/<id>` | GET | Detalle de categoría |
| `/categorias/<id>/editar` | GET, POST | Editar categoría |
| `/categorias/<id>/eliminar` | POST | Eliminar categoría |
| `/productos` | GET | Lista de productos |
| `/productos/nuevo` | GET, POST | Crear producto |
| `/productos/<id>` | GET | Detalle de producto |
| `/productos/<id>/editar` | GET, POST | Editar producto |
| `/productos/<id>/eliminar` | POST | Eliminar producto |

### Rutas de Admin (requieren rol admin)
| Ruta | Método | Descripción |
|------|--------|-------------|
| `/admin/usuarios` | GET | Gestionar usuarios |
| `/admin/usuarios/<id>/toggle` | POST | Activar/desactivar usuario |
| `/admin/usuarios/<id>/cambiar-rol` | POST | Cambiar rol de usuario |

## Estructura de Archivos

```
Semana_9/
├── app_flask.py                    # Aplicación principal
├── 01_intro_autenticacion.py       # Tutorial: hashing
├── 02_sesiones_flask.py            # Tutorial: sesiones
├── 03_decoradores_proteccion.py    # Tutorial: decoradores
├── README_SEMANA_9.md              # Este archivo
├── static/
│   └── css/
│       └── styles.css              # Estilos (con auth)
└── templates/
    ├── base.html                   # Base con navbar de auth
    ├── index.html                  # Dashboard
    ├── error.html                  # Página de error
    ├── macros.html                 # Componentes reutilizables
    ├── auth/
    │   ├── login.html              # Formulario de login
    │   ├── registro.html           # Formulario de registro
    │   ├── perfil.html             # Perfil de usuario
    │   ├── editar_perfil.html      # Editar perfil
    │   ├── cambiar_password.html   # Cambiar contraseña
    │   └── lista_usuarios.html     # Admin: gestión de usuarios
    ├── categorias/
    │   ├── lista.html
    │   ├── formulario.html
    │   └── detalle.html
    └── productos/
        ├── lista.html
        ├── formulario.html
        └── detalle.html
```

## Buenas Prácticas de Seguridad

1. **NUNCA** guardar contraseñas en texto plano
2. Usar mensajes genéricos: "Email o contraseña incorrectos" (no revelar cuál falló)
3. Cambiar `secret_key` en producción
4. Validar datos tanto en frontend como en backend
5. Usar HTTPS en producción
6. Limitar intentos de login (no implementado en este ejemplo básico)
