# ============================================================================
# SEMANA 9 - PARTE 2: Sesiones en Flask
# ============================================================================
#
# Las SESIONES permiten que Flask "recuerde" información del usuario
# entre diferentes peticiones HTTP.
#
# HTTP es un protocolo SIN ESTADO (stateless):
# - Cada petición es independiente
# - El servidor no sabe si dos peticiones vienen del mismo usuario
#
# Las sesiones resuelven esto usando COOKIES:
# 1. El servidor crea una sesión y envía un ID al navegador (cookie)
# 2. El navegador envía esa cookie en cada petición siguiente
# 3. El servidor lee la cookie y recupera los datos de la sesión
#
# ============================================================================

from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)

# ============================================================================
# SECRET_KEY: Clave para firmar las cookies de sesión
# ============================================================================
# Flask firma las cookies con esta clave para evitar que alguien
# las modifique. Si la clave cambia, todas las sesiones se invalidan.
#
# EN PRODUCCIÓN: usar una clave larga y aleatoria
# import secrets
# app.secret_key = secrets.token_hex(32)
# ============================================================================

app.secret_key = 'clave-secreta-para-desarrollo'


# ============================================================================
# RUTA: Página principal
# ============================================================================
@app.route('/')
def index():
    # Verificamos si hay un usuario en la sesión
    if 'usuario' in session:
        return f"""
        <h1>Bienvenido, {session['usuario']}</h1>
        <p>Visitas a esta página: {session.get('visitas', 0)}</p>
        <p><a href="/incrementar">Incrementar visitas</a></p>
        <p><a href="/logout">Cerrar sesión</a></p>
        """
    else:
        return """
        <h1>No has iniciado sesión</h1>
        <p><a href="/login">Iniciar sesión</a></p>
        """


# ============================================================================
# RUTA: Login simple (sin base de datos)
# ============================================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '')
        if nombre:
            # ── Guardar datos en la sesión ─────────────────────────────
            # session es un diccionario especial de Flask
            # Los datos se almacenan en una cookie firmada
            session['usuario'] = nombre
            session['visitas'] = 0
            return redirect(url_for('index'))

    return """
    <h1>Iniciar Sesión</h1>
    <form method="POST">
        <label>Tu nombre:</label><br>
        <input type="text" name="nombre" required><br><br>
        <button type="submit">Entrar</button>
    </form>
    """


# ============================================================================
# RUTA: Incrementar visitas (ejemplo de modificar sesión)
# ============================================================================
@app.route('/incrementar')
def incrementar():
    if 'usuario' in session:
        # Modificamos un valor de la sesión
        session['visitas'] = session.get('visitas', 0) + 1
    return redirect(url_for('index'))


# ============================================================================
# RUTA: Logout
# ============================================================================
@app.route('/logout')
def logout():
    # session.clear() elimina TODOS los datos de la sesión
    session.clear()
    return redirect(url_for('index'))


# ============================================================================
# CONCEPTOS IMPORTANTES SOBRE SESIONES
# ============================================================================
#
# ┌──────────────────────────────────────────────────────────────────────┐
# │ OPERACIÓN               │ CÓDIGO                                    │
# ├──────────────────────────────────────────────────────────────────────┤
# │ Guardar dato             │ session['clave'] = valor                 │
# │ Leer dato                │ session.get('clave', default)            │
# │ Verificar si existe      │ if 'clave' in session:                   │
# │ Eliminar un dato         │ session.pop('clave', None)               │
# │ Eliminar todo            │ session.clear()                          │
# │ Sesión permanente        │ session.permanent = True                 │
# └──────────────────────────────────────────────────────────────────────┘
#
# SESIONES vs COOKIES:
# - Cookie: dato almacenado en el NAVEGADOR (visible al usuario)
# - Sesión: dato almacenado en el SERVIDOR (solo el ID va al navegador)
# - Flask usa cookies FIRMADAS: los datos van al navegador pero encriptados
#
# CUÁNDO USAR SESIONES:
# - Almacenar ID del usuario logueado
# - Guardar preferencias temporales
# - Carrito de compras
# - Mensajes flash (flash())
#
# CUÁNDO NO USAR SESIONES:
# - Datos grandes (>4KB limitación de cookies)
# - Datos que deben persistir (usar base de datos)
# - APIs REST (usar tokens/JWT en su lugar)
#
# ============================================================================


if __name__ == '__main__':
    print("=" * 60)
    print("EJEMPLO: Sesiones en Flask")
    print("=" * 60)
    print("""
    Abre http://localhost:5004 en tu navegador

    PRUEBA:
    1. Visita / → verás que no estás logueado
    2. Ve a /login → escribe tu nombre
    3. Visita / → verás tu nombre y contador de visitas
    4. Ve a /incrementar → el contador sube
    5. Ve a /logout → se cierra la sesión
    """)
    app.run(debug=True, port=5004)
