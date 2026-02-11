# ============================================================================
# SEMANA 9: Autenticación en Flask
# ============================================================================
# Esta aplicación extiende la Semana 8 agregando:
# - Modelo de Usuario con hashing de contraseñas
# - Registro e inicio de sesión
# - Protección de rutas con decorador login_required
# - Perfil de usuario y cambio de contraseña
# - Roles de usuario (admin / usuario)
#
# CÓMO EJECUTAR:
# 1. Configura tu DATABASE_URL abajo
# 2. Ejecuta: python app_flask.py
# 3. Abre: http://localhost:5003
# ============================================================================

# ============================================================================
# IMPORTACIONES
# ============================================================================
# Flask: framework web
# werkzeug.security: hashing de contraseñas (viene incluido con Flask)
# functools.wraps: para crear decoradores correctamente
# ============================================================================

from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import os

# ============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================================================

app = Flask(__name__)
app.secret_key = 'clave-secreta-cambiar-en-produccion'  # Para sesiones y flash

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURA TU CADENA DE CONEXIÓN AQUÍ                                     ║
# ║                                                                           ║
# ║  Obtén tu cadena de conexión en: https://console.neon.tech                ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://neondb_owner:npg_xnKz5VIdoiv7@ep-hidden-voice-ahdtczjv-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
)

# ============================================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================================================

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
Base = declarative_base()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


# ============================================================================
# MODELOS DE LA BASE DE DATOS
# ============================================================================

# ----------------------------------------------------------------------------
# MODELO DE USUARIO (NUEVO EN SEMANA 9)
# ----------------------------------------------------------------------------
# Este modelo almacena la información de autenticación.
#
# CONCEPTOS CLAVE:
# - La contraseña NUNCA se guarda en texto plano
# - Se usa werkzeug.security para hashear contraseñas
# - generate_password_hash() convierte "mi_password" → "pbkdf2:sha256:..."
# - check_password_hash() verifica si una contraseña coincide con el hash
# ----------------------------------------------------------------------------

class Usuario(Base):
    """
    Modelo para usuarios del sistema.

    Campos:
    - nombre: nombre visible del usuario
    - email: correo electrónico (único, se usa para login)
    - password_hash: contraseña hasheada (NUNCA texto plano)
    - rol: 'admin' o 'usuario'
    - activo: si la cuenta está activa
    """
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    rol = Column(String(20), default='usuario')  # 'admin' o 'usuario'
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Usuario {self.email}>"

    # ── Métodos de contraseña ──────────────────────────────────────────────
    # Estos métodos encapsulan la lógica de hashing.
    # Así el resto de la app nunca toca la contraseña directamente.

    def set_password(self, password):
        """
        Hashea y guarda la contraseña.

        EJEMPLO:
        usuario.set_password('mi_password_seguro')
        # Internamente guarda: 'pbkdf2:sha256:260000$...'
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verifica si la contraseña proporcionada coincide con el hash.

        EJEMPLO:
        if usuario.check_password('mi_password_seguro'):
            print("Contraseña correcta")
        """
        return check_password_hash(self.password_hash, password)

    @property
    def es_admin(self):
        """Retorna True si el usuario tiene rol de administrador."""
        return self.rol == 'admin'


# ----------------------------------------------------------------------------
# MODELOS EXISTENTES (igual que Semana 8)
# ----------------------------------------------------------------------------

class Categoria(Base):
    """Modelo para categorías de productos."""
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    activa = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    productos = relationship(
        "Producto",
        back_populates="categoria",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Categoria {self.nombre}>"

    @property
    def cantidad_productos(self):
        return len(self.productos)


class Producto(Base):
    """Modelo para productos."""
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    categoria = relationship("Categoria", back_populates="productos")

    def __repr__(self):
        return f"<Producto {self.nombre}>"

    @property
    def precio_formateado(self):
        return f"${self.precio:.2f}"


# ============================================================================
# CREAR LAS TABLAS
# ============================================================================

def crear_tablas(reset=False):
    """Crea todas las tablas en la base de datos."""
    if reset:
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS productos CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS categorias CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS usuarios CASCADE"))
            conn.commit()
        print("[OK] Tablas eliminadas (CASCADE)")
    Base.metadata.create_all(engine)
    print("[OK] Tablas creadas/verificadas")


def crear_admin_por_defecto():
    """
    Crea un usuario administrador si no existe ninguno.

    Esto es útil para la primera vez que se ejecuta la app.
    Credenciales por defecto:
    - Email: admin@ejemplo.com
    - Password: admin123
    """
    db = Session()
    try:
        admin = db.query(Usuario).filter(Usuario.email == 'admin@ejemplo.com').first()
        if not admin:
            admin = Usuario(
                nombre='Administrador',
                email='admin@ejemplo.com',
                rol='admin'
            )
            admin.set_password('admin123')
            db.add(admin)
            db.commit()
            print("[OK] Usuario admin creado (admin@ejemplo.com / admin123)")
        else:
            print("[OK] Usuario admin ya existe")
    finally:
        db.close()


# ============================================================================
# DECORADORES DE AUTENTICACIÓN
# ============================================================================
# Los decoradores son funciones que "envuelven" otras funciones para
# agregar comportamiento adicional.
#
# CÓMO FUNCIONA login_required:
# 1. Antes de ejecutar la ruta, verifica si hay un usuario en la sesión
# 2. Si no hay usuario → redirige al login
# 3. Si hay usuario → ejecuta la ruta normalmente
#
# USO:
# @app.route('/ruta-protegida')
# @login_required
# def mi_ruta():
#     ...
# ============================================================================

def login_required(f):
    """
    Decorador que protege rutas.

    Si el usuario no está logueado, lo redirige al login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    Decorador que requiere rol de administrador.

    Primero verifica que el usuario esté logueado,
    luego verifica que sea admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        if session.get('usuario_rol') != 'admin':
            flash('No tienes permisos para acceder a esta página', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# CONTEXTO GLOBAL PARA TEMPLATES
# ============================================================================
# Esto inyecta la información del usuario en TODAS las plantillas,
# así no necesitamos pasarla manualmente en cada render_template().
# ============================================================================

@app.context_processor
def inject_user():
    """
    Inyecta datos del usuario actual en todas las plantillas.

    En cualquier template puedes usar:
    - {{ usuario_actual.nombre }}
    - {% if esta_logueado %}...{% endif %}
    - {% if es_admin %}...{% endif %}
    """
    if 'usuario_id' in session:
        db = Session()
        try:
            usuario = db.query(Usuario).get(session['usuario_id'])
            return {
                'usuario_actual': usuario,
                'esta_logueado': True,
                'es_admin': session.get('usuario_rol') == 'admin'
            }
        finally:
            db.close()
    return {
        'usuario_actual': None,
        'esta_logueado': False,
        'es_admin': False
    }


# ============================================================================
# RUTAS DE AUTENTICACIÓN
# ============================================================================

# ----------------------------------------------------------------------------
# REGISTRO DE USUARIO
# ----------------------------------------------------------------------------

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """
    Registra un nuevo usuario.

    GET: Muestra el formulario de registro
    POST: Procesa el formulario y crea el usuario

    VALIDACIONES:
    1. Todos los campos son obligatorios
    2. Las contraseñas deben coincidir
    3. La contraseña debe tener al menos 6 caracteres
    4. El email no debe estar registrado
    """
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirmar_password = request.form.get('confirmar_password', '')

        # ── Validaciones ──────────────────────────────────────────────────
        errores = []

        if not nombre:
            errores.append('El nombre es obligatorio')
        if not email:
            errores.append('El email es obligatorio')
        if not password:
            errores.append('La contraseña es obligatoria')
        if len(password) < 6:
            errores.append('La contraseña debe tener al menos 6 caracteres')
        if password != confirmar_password:
            errores.append('Las contraseñas no coinciden')

        if errores:
            for error in errores:
                flash(error, 'danger')
            return render_template('auth/registro.html',
                                   nombre=nombre, email=email)

        # ── Crear usuario ─────────────────────────────────────────────────
        db = Session()
        try:
            # Verificar si el email ya existe
            existente = db.query(Usuario).filter(Usuario.email == email).first()
            if existente:
                flash('Ya existe una cuenta con ese email', 'danger')
                return render_template('auth/registro.html',
                                       nombre=nombre, email=email)

            # Crear el usuario
            usuario = Usuario(nombre=nombre, email=email)
            usuario.set_password(password)  # Hashea la contraseña
            db.add(usuario)
            db.commit()

            flash('Cuenta creada exitosamente. ¡Inicia sesión!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.rollback()
            flash(f'Error al crear la cuenta: {e}', 'danger')
        finally:
            db.close()

    return render_template('auth/registro.html')


# ----------------------------------------------------------------------------
# INICIO DE SESIÓN
# ----------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Inicia sesión de un usuario.

    GET: Muestra el formulario de login
    POST: Verifica credenciales y crea la sesión

    PROCESO DE LOGIN:
    1. Buscar usuario por email
    2. Verificar que la cuenta esté activa
    3. Verificar la contraseña con check_password()
    4. Guardar datos del usuario en la sesión de Flask
    5. Redirigir a la página principal
    """
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        db = Session()
        try:
            usuario = db.query(Usuario).filter(Usuario.email == email).first()

            # Verificar credenciales
            # NOTA: Usamos el mismo mensaje para email incorrecto y password
            # incorrecto. Esto es una BUENA PRÁCTICA de seguridad porque
            # no le dice al atacante si el email existe o no.
            if not usuario or not usuario.check_password(password):
                flash('Email o contraseña incorrectos', 'danger')
                return render_template('auth/login.html', email=email)

            if not usuario.activo:
                flash('Tu cuenta ha sido desactivada. Contacta al administrador.', 'warning')
                return render_template('auth/login.html', email=email)

            # ── Crear sesión ──────────────────────────────────────────────
            # Flask usa cookies firmadas para mantener la sesión.
            # Los datos se guardan en el lado del servidor de forma segura.
            session['usuario_id'] = usuario.id
            session['usuario_nombre'] = usuario.nombre
            session['usuario_email'] = usuario.email
            session['usuario_rol'] = usuario.rol

            flash(f'¡Bienvenido, {usuario.nombre}!', 'success')
            return redirect(url_for('index'))
        finally:
            db.close()

    return render_template('auth/login.html')


# ----------------------------------------------------------------------------
# CERRAR SESIÓN
# ----------------------------------------------------------------------------

@app.route('/logout')
def logout():
    """
    Cierra la sesión del usuario.

    session.clear() elimina TODOS los datos de la sesión,
    incluyendo usuario_id, nombre, etc.
    """
    nombre = session.get('usuario_nombre', '')
    session.clear()
    flash(f'¡Hasta luego, {nombre}!', 'info')
    return redirect(url_for('login'))


# ----------------------------------------------------------------------------
# PERFIL DE USUARIO
# ----------------------------------------------------------------------------

@app.route('/perfil')
@login_required
def perfil():
    """Muestra el perfil del usuario logueado."""
    db = Session()
    try:
        usuario = db.query(Usuario).get(session['usuario_id'])
        if not usuario:
            session.clear()
            return redirect(url_for('login'))
        return render_template('auth/perfil.html', usuario=usuario)
    finally:
        db.close()


# ----------------------------------------------------------------------------
# EDITAR PERFIL
# ----------------------------------------------------------------------------

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    """Permite al usuario editar su nombre y email."""
    db = Session()
    try:
        usuario = db.query(Usuario).get(session['usuario_id'])
        if not usuario:
            session.clear()
            return redirect(url_for('login'))

        if request.method == 'POST':
            nombre = request.form.get('nombre', '').strip()
            email = request.form.get('email', '').strip().lower()

            if not nombre or not email:
                flash('Nombre y email son obligatorios', 'danger')
                return render_template('auth/editar_perfil.html', usuario=usuario)

            # Verificar que el email no esté en uso por otro usuario
            existente = db.query(Usuario).filter(
                Usuario.email == email,
                Usuario.id != usuario.id
            ).first()
            if existente:
                flash('Ese email ya está en uso por otro usuario', 'danger')
                return render_template('auth/editar_perfil.html', usuario=usuario)

            usuario.nombre = nombre
            usuario.email = email
            db.commit()

            # Actualizar datos en la sesión
            session['usuario_nombre'] = nombre
            session['usuario_email'] = email

            flash('Perfil actualizado exitosamente', 'success')
            return redirect(url_for('perfil'))

        return render_template('auth/editar_perfil.html', usuario=usuario)
    finally:
        db.close()


# ----------------------------------------------------------------------------
# CAMBIAR CONTRASEÑA
# ----------------------------------------------------------------------------

@app.route('/perfil/cambiar-password', methods=['GET', 'POST'])
@login_required
def cambiar_password():
    """
    Permite al usuario cambiar su contraseña.

    Requiere la contraseña actual como verificación de seguridad.
    """
    if request.method == 'POST':
        password_actual = request.form.get('password_actual', '')
        password_nueva = request.form.get('password_nueva', '')
        confirmar_password = request.form.get('confirmar_password', '')

        db = Session()
        try:
            usuario = db.query(Usuario).get(session['usuario_id'])

            # Verificar contraseña actual
            if not usuario.check_password(password_actual):
                flash('La contraseña actual es incorrecta', 'danger')
                return render_template('auth/cambiar_password.html')

            # Validar nueva contraseña
            if len(password_nueva) < 6:
                flash('La nueva contraseña debe tener al menos 6 caracteres', 'danger')
                return render_template('auth/cambiar_password.html')

            if password_nueva != confirmar_password:
                flash('Las contraseñas nuevas no coinciden', 'danger')
                return render_template('auth/cambiar_password.html')

            # Cambiar contraseña
            usuario.set_password(password_nueva)
            db.commit()

            flash('Contraseña cambiada exitosamente', 'success')
            return redirect(url_for('perfil'))
        finally:
            db.close()

    return render_template('auth/cambiar_password.html')


# ============================================================================
# RUTAS DE ADMINISTRACIÓN DE USUARIOS (solo admin)
# ============================================================================

@app.route('/admin/usuarios')
@admin_required
def listar_usuarios():
    """Lista todos los usuarios (solo admin)."""
    db = Session()
    try:
        usuarios = db.query(Usuario).order_by(Usuario.fecha_creacion.desc()).all()
        return render_template('auth/lista_usuarios.html', usuarios=usuarios)
    finally:
        db.close()


@app.route('/admin/usuarios/<int:id>/toggle', methods=['POST'])
@admin_required
def toggle_usuario(id):
    """Activa/desactiva un usuario (solo admin)."""
    db = Session()
    try:
        usuario = db.query(Usuario).get(id)
        if not usuario:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('listar_usuarios'))

        # No permitir desactivarse a sí mismo
        if usuario.id == session['usuario_id']:
            flash('No puedes desactivar tu propia cuenta', 'warning')
            return redirect(url_for('listar_usuarios'))

        usuario.activo = not usuario.activo
        estado = 'activado' if usuario.activo else 'desactivado'
        db.commit()
        flash(f'Usuario "{usuario.nombre}" {estado}', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('listar_usuarios'))


@app.route('/admin/usuarios/<int:id>/cambiar-rol', methods=['POST'])
@admin_required
def cambiar_rol_usuario(id):
    """Cambia el rol de un usuario (solo admin)."""
    db = Session()
    try:
        usuario = db.query(Usuario).get(id)
        if not usuario:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('listar_usuarios'))

        if usuario.id == session['usuario_id']:
            flash('No puedes cambiar tu propio rol', 'warning')
            return redirect(url_for('listar_usuarios'))

        usuario.rol = 'admin' if usuario.rol == 'usuario' else 'usuario'
        db.commit()
        flash(f'Rol de "{usuario.nombre}" cambiado a {usuario.rol}', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('listar_usuarios'))


# ============================================================================
# PÁGINA PRINCIPAL (protegida)
# ============================================================================

@app.route('/')
@login_required
def index():
    """Página principal con estadísticas (requiere login)."""
    db = Session()
    try:
        total_categorias = db.query(Categoria).count()
        total_productos = db.query(Producto).count()
        productos_activos = db.query(Producto).filter(Producto.activo == True).count()
        productos_sin_stock = db.query(Producto).filter(Producto.stock == 0).count()
        total_usuarios = db.query(Usuario).count()

        return render_template(
            'index.html',
            total_categorias=total_categorias,
            total_productos=total_productos,
            productos_activos=productos_activos,
            productos_sin_stock=productos_sin_stock,
            total_usuarios=total_usuarios
        )
    finally:
        db.close()


# ============================================================================
# RUTAS CRUD PARA CATEGORÍAS (protegidas)
# ============================================================================

@app.route('/categorias')
@login_required
def listar_categorias():
    """Lista todas las categorías."""
    db = Session()
    try:
        categorias = db.query(Categoria).order_by(Categoria.nombre).all()
        return render_template('categorias/lista.html', categorias=categorias)
    finally:
        db.close()


@app.route('/categorias/nueva', methods=['GET', 'POST'])
@login_required
def crear_categoria():
    """Crea una nueva categoría."""
    if request.method == 'POST':
        db = Session()
        try:
            categoria = Categoria(
                nombre=request.form['nombre'],
                descripcion=request.form.get('descripcion', '')
            )
            db.add(categoria)
            db.commit()
            flash(f'Categoría "{categoria.nombre}" creada exitosamente', 'success')
            return redirect(url_for('listar_categorias'))
        except Exception as e:
            db.rollback()
            flash(f'Error al crear categoría: {e}', 'danger')
        finally:
            db.close()

    return render_template('categorias/formulario.html', categoria=None)


@app.route('/categorias/<int:id>')
@login_required
def ver_categoria(id):
    """Muestra el detalle de una categoría."""
    db = Session()
    try:
        categoria = db.query(Categoria).get(id)
        if not categoria:
            flash('Categoría no encontrada', 'danger')
            return redirect(url_for('listar_categorias'))
        return render_template('categorias/detalle.html', categoria=categoria)
    finally:
        db.close()


@app.route('/categorias/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    """Edita una categoría existente."""
    db = Session()
    try:
        categoria = db.query(Categoria).get(id)
        if not categoria:
            flash('Categoría no encontrada', 'danger')
            return redirect(url_for('listar_categorias'))

        if request.method == 'POST':
            categoria.nombre = request.form['nombre']
            categoria.descripcion = request.form.get('descripcion', '')
            db.commit()
            flash(f'Categoría "{categoria.nombre}" actualizada', 'success')
            return redirect(url_for('listar_categorias'))

        return render_template('categorias/formulario.html', categoria=categoria)
    finally:
        db.close()


@app.route('/categorias/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_categoria(id):
    """Elimina una categoría."""
    db = Session()
    try:
        categoria = db.query(Categoria).get(id)
        if categoria:
            nombre = categoria.nombre
            db.delete(categoria)
            db.commit()
            flash(f'Categoría "{nombre}" eliminada', 'success')
        else:
            flash('Categoría no encontrada', 'danger')
    except Exception as e:
        db.rollback()
        flash(f'Error al eliminar: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('listar_categorias'))


# ============================================================================
# RUTAS CRUD PARA PRODUCTOS (protegidas)
# ============================================================================

@app.route('/productos')
@login_required
def listar_productos():
    """Lista todos los productos."""
    db = Session()
    try:
        productos = db.query(Producto).order_by(Producto.nombre).all()
        return render_template('productos/lista.html', productos=productos)
    finally:
        db.close()


@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def crear_producto():
    """Crea un nuevo producto."""
    db = Session()
    try:
        categorias = db.query(Categoria).filter(Categoria.activa == True).all()

        if request.method == 'POST':
            producto = Producto(
                nombre=request.form['nombre'],
                descripcion=request.form.get('descripcion', ''),
                precio=float(request.form['precio']),
                stock=int(request.form.get('stock', 0)),
                categoria_id=int(request.form['categoria_id']) if request.form.get('categoria_id') else None
            )
            db.add(producto)
            db.commit()
            flash(f'Producto "{producto.nombre}" creado exitosamente', 'success')
            return redirect(url_for('listar_productos'))

        return render_template('productos/formulario.html', producto=None, categorias=categorias)
    finally:
        db.close()


@app.route('/productos/<int:id>')
@login_required
def ver_producto(id):
    """Muestra el detalle de un producto."""
    db = Session()
    try:
        producto = db.query(Producto).get(id)
        if not producto:
            flash('Producto no encontrado', 'danger')
            return redirect(url_for('listar_productos'))
        return render_template('productos/detalle.html', producto=producto)
    finally:
        db.close()


@app.route('/productos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    """Edita un producto existente."""
    db = Session()
    try:
        producto = db.query(Producto).get(id)
        categorias = db.query(Categoria).filter(Categoria.activa == True).all()

        if not producto:
            flash('Producto no encontrado', 'danger')
            return redirect(url_for('listar_productos'))

        if request.method == 'POST':
            producto.nombre = request.form['nombre']
            producto.descripcion = request.form.get('descripcion', '')
            producto.precio = float(request.form['precio'])
            producto.stock = int(request.form.get('stock', 0))
            producto.categoria_id = int(request.form['categoria_id']) if request.form.get('categoria_id') else None
            db.commit()
            flash(f'Producto "{producto.nombre}" actualizado', 'success')
            return redirect(url_for('listar_productos'))

        return render_template('productos/formulario.html', producto=producto, categorias=categorias)
    finally:
        db.close()


@app.route('/productos/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_producto(id):
    """Elimina un producto."""
    db = Session()
    try:
        producto = db.query(Producto).get(id)
        if producto:
            nombre = producto.nombre
            db.delete(producto)
            db.commit()
            flash(f'Producto "{nombre}" eliminado', 'success')
        else:
            flash('Producto no encontrado', 'danger')
    except Exception as e:
        db.rollback()
        flash(f'Error al eliminar: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('listar_productos'))


# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('error.html', mensaje='Página no encontrada'), 404


@app.errorhandler(500)
def error_servidor(e):
    return render_template('error.html', mensaje='Error interno del servidor'), 500


# ============================================================================
# CERRAR SESIÓN DE BD AL FINAL DE CADA REQUEST
# ============================================================================

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("SEMANA 9: Autenticación en Flask")
    print("=" * 70)

    crear_tablas(reset=False)
    crear_admin_por_defecto()

    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                         APLICACIÓN INICIADA                               ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  URL: http://localhost:5003                                               ║
║                                                                           ║
║  RUTAS PÚBLICAS:                                                          ║
║  ────────────────                                                         ║
║  /login                → Iniciar sesión                                   ║
║  /registro             → Crear cuenta                                     ║
║  /logout               → Cerrar sesión                                    ║
║                                                                           ║
║  RUTAS PROTEGIDAS (requieren login):                                      ║
║  ───────────────────────────────────                                      ║
║  /                     → Página principal                                 ║
║  /perfil               → Mi perfil                                        ║
║  /perfil/editar        → Editar perfil                                    ║
║  /perfil/cambiar-password → Cambiar contraseña                            ║
║  /categorias           → Lista de categorías                              ║
║  /productos            → Lista de productos                               ║
║                                                                           ║
║  RUTAS DE ADMIN:                                                          ║
║  ───────────────                                                          ║
║  /admin/usuarios       → Gestionar usuarios                               ║
║                                                                           ║
║  CREDENCIALES POR DEFECTO:                                                ║
║  ─────────────────────────                                                ║
║  Email: admin@ejemplo.com                                                 ║
║  Password: admin123                                                       ║
║                                                                           ║
║  Presiona Ctrl+C para detener el servidor                                 ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)

    app.run(debug=True, port=5003)
