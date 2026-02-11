# ============================================================================
# SEMANA 9 - PARTE 3: Decoradores y Protección de Rutas
# ============================================================================
#
# Un DECORADOR es una función que "envuelve" a otra función para
# agregarle funcionalidad sin modificar su código original.
#
# En autenticación, usamos decoradores para PROTEGER rutas:
# - @login_required → solo usuarios logueados
# - @admin_required → solo administradores
#
# ============================================================================

# ============================================================================
# 1. ¿QUÉ ES UN DECORADOR?
# ============================================================================

print("=" * 60)
print("PARTE 1: Decoradores en Python")
print("=" * 60)

# Un decorador es simplemente una función que recibe otra función
# y retorna una nueva función "mejorada".

# ── Ejemplo básico: decorador que saluda ─────────────────────────────────

def saludar_antes(funcion):
    """Decorador que imprime un saludo antes de ejecutar la función."""
    def wrapper(*args, **kwargs):
        print("   ¡Hola! Voy a ejecutar algo...")
        resultado = funcion(*args, **kwargs)
        print("   ¡Listo! Ya terminé.")
        return resultado
    return wrapper

@saludar_antes
def sumar(a, b):
    """Suma dos números."""
    resultado = a + b
    print(f"   {a} + {b} = {resultado}")
    return resultado

print("\nLlamando a sumar(3, 5):")
sumar(3, 5)


# ── Ejemplo práctico: verificar acceso ───────────────────────────────────
print("\n" + "=" * 60)
print("PARTE 2: Decorador de Autenticación")
print("=" * 60)

from functools import wraps

# Simulamos una sesión
sesion_actual = {'usuario': None, 'rol': None}

def login_required(f):
    """
    Decorador que verifica si el usuario está logueado.

    Si no está logueado, muestra un mensaje de error.
    Si está logueado, ejecuta la función normalmente.

    USO:
    @login_required
    def mi_ruta():
        ...
    """
    @wraps(f)  # Preserva el nombre y docstring de la función original
    def decorated_function(*args, **kwargs):
        if sesion_actual['usuario'] is None:
            print(f"   [BLOQUEADO] Debes iniciar sesión para acceder a '{f.__name__}'")
            return None
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorador que verifica si el usuario es administrador.

    Primero verifica login, luego verifica el rol.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if sesion_actual['usuario'] is None:
            print(f"   [BLOQUEADO] Debes iniciar sesión para acceder a '{f.__name__}'")
            return None
        if sesion_actual['rol'] != 'admin':
            print(f"   [PROHIBIDO] No tienes permisos de admin para '{f.__name__}'")
            return None
        return f(*args, **kwargs)
    return decorated_function


# ── Funciones protegidas ─────────────────────────────────────────────────

@login_required
def ver_productos():
    """Muestra la lista de productos (requiere login)."""
    print(f"   [OK] Mostrando productos a {sesion_actual['usuario']}")

@login_required
def crear_producto():
    """Crea un producto (requiere login)."""
    print(f"   [OK] {sesion_actual['usuario']} está creando un producto")

@admin_required
def eliminar_usuario():
    """Elimina un usuario (requiere admin)."""
    print(f"   [OK] Admin {sesion_actual['usuario']} eliminando usuario")


# ── Prueba 1: Sin login ──────────────────────────────────────────────────
print("\nPrueba 1: Sin iniciar sesión")
print("-" * 40)
ver_productos()
crear_producto()
eliminar_usuario()

# ── Prueba 2: Login como usuario normal ──────────────────────────────────
print("\nPrueba 2: Login como usuario normal")
print("-" * 40)
sesion_actual['usuario'] = 'Ana'
sesion_actual['rol'] = 'usuario'
ver_productos()       # OK
crear_producto()      # OK
eliminar_usuario()    # PROHIBIDO

# ── Prueba 3: Login como admin ───────────────────────────────────────────
print("\nPrueba 3: Login como administrador")
print("-" * 40)
sesion_actual['usuario'] = 'Admin'
sesion_actual['rol'] = 'admin'
ver_productos()       # OK
crear_producto()      # OK
eliminar_usuario()    # OK


# ============================================================================
# 3. CÓMO FUNCIONA EN FLASK
# ============================================================================

print("\n" + "=" * 60)
print("PARTE 3: Así se usa en Flask (app_flask.py)")
print("=" * 60)

print("""
En Flask, el decorador login_required funciona así:

    from flask import session, redirect, url_for, flash
    from functools import wraps

    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # ¿Hay un usuario en la sesión de Flask?
            if 'usuario_id' not in session:
                flash('Debes iniciar sesión', 'warning')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function

    # USO:
    @app.route('/productos')
    @login_required                    ← Protege la ruta
    def listar_productos():
        # Este código solo se ejecuta si el usuario está logueado
        productos = db.query(Producto).all()
        return render_template('productos/lista.html', productos=productos)

FLUJO:
    1. Usuario visita /productos
    2. Flask ejecuta login_required ANTES de listar_productos
    3. login_required verifica si 'usuario_id' está en session
    4a. SI está → ejecuta listar_productos() normalmente
    4b. NO está → redirige a /login con mensaje flash

ORDEN DE DECORADORES:
    @app.route('/ruta')    ← Primero: registra la URL
    @login_required        ← Segundo: agrega la protección
    def mi_funcion():      ← La función que se ejecuta
        ...

    El orden importa: @app.route siempre va PRIMERO.
""")


# ============================================================================
# 4. RESUMEN DE DECORADORES
# ============================================================================

print("=" * 60)
print("RESUMEN")
print("=" * 60)
print("""
┌─────────────────────────────────────────────────────────────────┐
│ DECORADOR        │ PROTEGE                                      │
├─────────────────────────────────────────────────────────────────┤
│ @login_required  │ Solo usuarios logueados pueden acceder       │
│ @admin_required  │ Solo administradores pueden acceder          │
│ @app.route       │ Registra una URL en Flask (no es protección) │
└─────────────────────────────────────────────────────────────────┘

BENEFICIOS DE USAR DECORADORES:
1. Código DRY (Don't Repeat Yourself)
   - Sin decorador: cada ruta tiene 5 líneas de verificación
   - Con decorador: una sola línea @login_required

2. Separación de responsabilidades
   - La ruta se encarga de su lógica
   - El decorador se encarga de la seguridad

3. Fácil de mantener
   - Cambiar la lógica de autenticación en UN solo lugar
   - Todas las rutas se benefician automáticamente
""")
