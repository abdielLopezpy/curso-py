# ============================================================================
# SEMANA 10 - PROYECTO 1: MINI TIENDA E-COMMERCE
# ============================================================================
# Aplicacion web de comercio electronico que integra todos los conceptos
# aprendidos en el curso:
#
# - Modelos SQLAlchemy con relaciones (Semanas 6-7)
# - CRUD completo (Semana 8)
# - Autenticacion con sesiones y roles (Semana 9)
# - Carrito de compras y proceso de checkout
# - Panel de administracion
#
# COMO EJECUTAR:
# 1. pip install flask sqlalchemy psycopg2-binary werkzeug
# 2. python app.py
# 3. Abre: http://localhost:5010
#
# CREDENCIALES:
# - Admin: admin@ejemplo.com / admin123
# ============================================================================

from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import os

# ============================================================================
# CONFIGURACION DE LA APLICACION
# ============================================================================

app = Flask(__name__)
app.secret_key = 'ecommerce-secreto-cambiar-en-produccion'

# ============================================================================
# BASE DE DATOS
# ============================================================================
# Usamos la misma cadena de conexion de Neon (PostgreSQL en la nube).
# Si no esta configurada, usa la URL por defecto.
# ============================================================================

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://neondb_owner:npg_xnKz5VIdoiv7@ep-hidden-voice-ahdtczjv-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
)

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
Base = declarative_base()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


# ============================================================================
# MODELOS DE LA BASE DE DATOS
# ============================================================================
# NOTA: Todos los nombres de tabla usan prefijo "ec_" para evitar
# conflictos con las tablas de las semanas anteriores.
# ============================================================================

# ----------------------------------------------------------------------------
# MODELO: Usuario
# ----------------------------------------------------------------------------
# Igual que en Semana 9. Maneja autenticacion con hashing de contrasenas.
# Dos roles: 'admin' (gestiona tienda) y 'usuario' (compra productos).
# ----------------------------------------------------------------------------

class Usuario(Base):
    __tablename__ = 'ec_usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    rol = Column(String(20), default='usuario')
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relaciones: un usuario puede tener un carrito y muchos pedidos
    carrito = relationship("Carrito", back_populates="usuario", uselist=False)
    pedidos = relationship("Pedido", back_populates="usuario")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def es_admin(self):
        return self.rol == 'admin'


# ----------------------------------------------------------------------------
# MODELO: Categoria
# ----------------------------------------------------------------------------
# Agrupa los productos. Ejemplo: "Electronica", "Ropa", "Hogar".
# Un producto PERTENECE a una categoria (relacion one-to-many).
# ----------------------------------------------------------------------------

class Categoria(Base):
    __tablename__ = 'ec_categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    imagen_url = Column(String(500))
    activa = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    productos = relationship("Producto", back_populates="categoria", cascade="all, delete-orphan")

    @property
    def cantidad_productos(self):
        return len(self.productos)


# ----------------------------------------------------------------------------
# MODELO: Producto
# ----------------------------------------------------------------------------
# Articulo a la venta. Tiene precio, stock (cantidad disponible) y
# pertenece a una categoria.
# La propiedad "en_stock" indica si hay unidades disponibles.
# ----------------------------------------------------------------------------

class Producto(Base):
    __tablename__ = 'ec_productos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    imagen_url = Column(String(500))
    destacado = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    categoria_id = Column(Integer, ForeignKey('ec_categorias.id'))
    categoria = relationship("Categoria", back_populates="productos")

    @property
    def precio_formateado(self):
        return f"${self.precio:,.2f}"

    @property
    def en_stock(self):
        return self.stock > 0


# ----------------------------------------------------------------------------
# MODELO: Carrito
# ----------------------------------------------------------------------------
# Cada usuario tiene UN carrito (relacion one-to-one con Usuario).
# El carrito contiene ItemCarrito (relacion one-to-many).
#
# FLUJO:
# 1. Usuario agrega producto → se crea ItemCarrito
# 2. Usuario hace checkout → Carrito se convierte en Pedido
# 3. Los items del carrito se copian a ItemPedido
# 4. El carrito se vacia
# ----------------------------------------------------------------------------

class Carrito(Base):
    __tablename__ = 'ec_carritos'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('ec_usuarios.id'), unique=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="carrito")
    items = relationship("ItemCarrito", back_populates="carrito", cascade="all, delete-orphan")

    @property
    def total(self):
        """Calcula el total sumando el subtotal de cada item."""
        return sum(item.subtotal for item in self.items)

    @property
    def total_formateado(self):
        return f"${self.total:,.2f}"

    @property
    def cantidad_items(self):
        return sum(item.cantidad for item in self.items)


class ItemCarrito(Base):
    __tablename__ = 'ec_items_carrito'

    id = Column(Integer, primary_key=True)
    carrito_id = Column(Integer, ForeignKey('ec_carritos.id'))
    producto_id = Column(Integer, ForeignKey('ec_productos.id'))
    cantidad = Column(Integer, default=1)

    carrito = relationship("Carrito", back_populates="items")
    producto = relationship("Producto")

    @property
    def subtotal(self):
        """Subtotal = precio del producto x cantidad."""
        return self.producto.precio * self.cantidad


# ----------------------------------------------------------------------------
# MODELO: Pedido
# ----------------------------------------------------------------------------
# Cuando el usuario hace checkout, el carrito se convierte en un pedido.
# Estados posibles:
# - pendiente: recien creado
# - pagado: pago confirmado
# - enviado: en camino
# - entregado: recibido por el cliente
# - cancelado: el cliente o admin cancelo
# ----------------------------------------------------------------------------

class Pedido(Base):
    __tablename__ = 'ec_pedidos'

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('ec_usuarios.id'))
    total = Column(Float, nullable=False)
    estado = Column(String(20), default='pendiente')
    direccion_envio = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="pedidos")
    items = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")

    @property
    def total_formateado(self):
        return f"${self.total:,.2f}"

    @property
    def estado_color(self):
        """Retorna la clase CSS segun el estado del pedido."""
        colores = {
            'pendiente': 'warning',
            'pagado': 'info',
            'enviado': 'primary',
            'entregado': 'success',
            'cancelado': 'danger'
        }
        return colores.get(self.estado, 'secondary')


class ItemPedido(Base):
    __tablename__ = 'ec_items_pedido'

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('ec_pedidos.id'))
    producto_id = Column(Integer, ForeignKey('ec_productos.id'))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)

    pedido = relationship("Pedido", back_populates="items")
    producto = relationship("Producto")

    @property
    def subtotal(self):
        return self.precio_unitario * self.cantidad


# ============================================================================
# CREAR TABLAS Y DATOS DE EJEMPLO
# ============================================================================

def crear_tablas():
    Base.metadata.create_all(engine)
    print("[OK] Tablas del E-Commerce creadas/verificadas")


def crear_datos_ejemplo():
    """
    Crea datos de ejemplo para que la tienda no este vacia.
    Solo se ejecuta si no existe el admin.
    """
    db = Session()
    try:
        if db.query(Usuario).filter(Usuario.email == 'admin@ejemplo.com').first():
            print("[OK] Datos de ejemplo ya existen")
            return

        # --- Admin ---
        admin = Usuario(nombre='Administrador', email='admin@ejemplo.com', rol='admin')
        admin.set_password('admin123')
        db.add(admin)

        # --- Categorias ---
        # Categorias con contexto panameño - precios en USD/Balboas (moneda de Panama)
        categorias = {
            'Electronica': Categoria(nombre='Electronica', descripcion='Dispositivos y gadgets tecnologicos', activa=True),
            'Ropa': Categoria(nombre='Ropa y Moda', descripcion='Moda y vestimenta para el clima tropical', activa=True),
            'Hogar': Categoria(nombre='Hogar', descripcion='Todo para tu casa y decoracion', activa=True),
            'Deportes': Categoria(nombre='Deportes', descripcion='Equipamiento y ropa deportiva', activa=True),
        }
        for cat in categorias.values():
            db.add(cat)
        db.flush()

        # --- Productos (precios en USD/Balboas) ---
        productos = [
            Producto(nombre='Audifonos Bluetooth', descripcion='Audifonos inalambricos con cancelacion de ruido. Bateria de 30 horas. Envio a todo Panama.', precio=45.99, stock=25, destacado=True, categoria=categorias['Electronica']),
            Producto(nombre='Teclado Mecanico RGB', descripcion='Teclado mecanico con switches Cherry MX e iluminacion RGB personalizable.', precio=79.99, stock=15, destacado=True, categoria=categorias['Electronica']),
            Producto(nombre='Monitor 27 pulgadas 4K', descripcion='Monitor IPS de 27 pulgadas con resolucion 4K UHD. Ideal para trabajo y entretenimiento.', precio=329.99, stock=8, destacado=True, categoria=categorias['Electronica']),
            Producto(nombre='Camiseta Dry-Fit Tropical', descripcion='Camiseta ligera de secado rapido, ideal para el clima panameño. Disponible en multiples colores.', precio=19.99, stock=50, destacado=False, categoria=categorias['Ropa']),
            Producto(nombre='Bermudas Cargo', descripcion='Bermudas comodas y resistentes. Perfectas para el dia a dia en Panama.', precio=29.99, stock=30, destacado=False, categoria=categorias['Ropa']),
            Producto(nombre='Chubasquero Ligero', descripcion='Chubasquero compacto e impermeable. Indispensable para la temporada lluviosa.', precio=49.99, stock=20, destacado=True, categoria=categorias['Ropa']),
            Producto(nombre='Ventilador de Torre Silencioso', descripcion='Ventilador de torre con 3 velocidades y temporizador. Ideal para el calor tropical.', precio=59.99, stock=18, destacado=True, categoria=categorias['Hogar']),
            Producto(nombre='Set de Toallas Premium', descripcion='Set de 4 toallas de algodon egipcio ultra absorbentes.', precio=34.99, stock=35, destacado=False, categoria=categorias['Hogar']),
            Producto(nombre='Mancuernas Ajustables', descripcion='Par de mancuernas ajustables de 2.5kg a 25kg. Ahorra espacio.', precio=119.99, stock=12, destacado=True, categoria=categorias['Deportes']),
            Producto(nombre='Yoga Mat Premium', descripcion='Colchoneta de yoga antideslizante de 6mm. Material ecologico.', precio=24.99, stock=45, destacado=False, categoria=categorias['Deportes']),
            Producto(nombre='Smartwatch Deportivo', descripcion='Reloj inteligente con GPS, monitor cardiaco y resistencia al agua.', precio=189.99, stock=18, destacado=True, categoria=categorias['Electronica']),
            Producto(nombre='Zapatillas Running', descripcion='Zapatillas ligeras con amortiguacion avanzada para correr en la Cinta Costera.', precio=74.99, stock=22, destacado=False, categoria=categorias['Deportes']),
        ]
        for p in productos:
            db.add(p)

        db.commit()
        print("[OK] Datos de ejemplo creados (admin + 4 categorias + 12 productos)")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Al crear datos de ejemplo: {e}")
    finally:
        db.close()


# ============================================================================
# DECORADORES DE AUTENTICACION
# ============================================================================

def login_required(f):
    """Protege rutas: redirige al login si no hay sesion activa."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesion para acceder', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Protege rutas de admin: requiere login + rol admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesion para acceder', 'warning')
            return redirect(url_for('login'))
        if session.get('usuario_rol') != 'admin':
            flash('No tienes permisos de administrador', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# ============================================================================
# CONTEXTO GLOBAL PARA TEMPLATES
# ============================================================================
# Inyecta datos del usuario y carrito en TODAS las plantillas.
# Asi podemos mostrar el contador del carrito en la navbar sin
# pasarlo manualmente en cada render_template().
# ============================================================================

@app.context_processor
def inject_user():
    datos = {
        'usuario_actual': None,
        'esta_logueado': False,
        'es_admin': False,
        'carrito_count': 0
    }
    if 'usuario_id' in session:
        # Usar una sesion NO-scoped aqui evita cerrar accidentalmente
        # la sesion de la vista actual durante render_template().
        db = session_factory()
        try:
            usuario = db.query(Usuario).get(session['usuario_id'])
            if usuario:
                datos['usuario_actual'] = usuario
                datos['esta_logueado'] = True
                datos['es_admin'] = usuario.es_admin
                if usuario.carrito:
                    datos['carrito_count'] = usuario.carrito.cantidad_items
        finally:
            db.close()
    return datos


# ============================================================================
# RUTAS DE AUTENTICACION
# ============================================================================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registro de nuevo usuario."""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirmar = request.form.get('confirmar_password', '')

        errores = []
        if not nombre:
            errores.append('El nombre es obligatorio')
        if not email:
            errores.append('El email es obligatorio')
        if len(password) < 6:
            errores.append('La contrasena debe tener al menos 6 caracteres')
        if password != confirmar:
            errores.append('Las contrasenas no coinciden')

        if errores:
            for e in errores:
                flash(e, 'danger')
            return render_template('auth/registro.html', nombre=nombre, email=email)

        db = Session()
        try:
            if db.query(Usuario).filter(Usuario.email == email).first():
                flash('Ya existe una cuenta con ese email', 'danger')
                return render_template('auth/registro.html', nombre=nombre, email=email)

            usuario = Usuario(nombre=nombre, email=email)
            usuario.set_password(password)
            db.add(usuario)
            db.commit()
            flash('Cuenta creada. Inicia sesion!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.rollback()
            flash(f'Error al crear cuenta: {e}', 'danger')
        finally:
            db.close()

    return render_template('auth/registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Inicio de sesion."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        db = Session()
        try:
            usuario = db.query(Usuario).filter(Usuario.email == email).first()
            if not usuario or not usuario.check_password(password):
                flash('Email o contrasena incorrectos', 'danger')
                return render_template('auth/login.html', email=email)
            if not usuario.activo:
                flash('Tu cuenta esta desactivada', 'warning')
                return render_template('auth/login.html', email=email)

            session['usuario_id'] = usuario.id
            session['usuario_nombre'] = usuario.nombre
            session['usuario_email'] = usuario.email
            session['usuario_rol'] = usuario.rol
            flash(f'Bienvenido, {usuario.nombre}!', 'success')
            return redirect(url_for('index'))
        finally:
            db.close()

    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    """Cerrar sesion."""
    session.clear()
    flash('Sesion cerrada', 'info')
    return redirect(url_for('login'))


# ============================================================================
# PAGINA PRINCIPAL (PUBLICA - muestra catalogo)
# ============================================================================

@app.route('/')
def index():
    """
    Pagina principal de la tienda.
    Muestra productos destacados y categorias.
    Es PUBLICA para que los visitantes vean el catalogo.
    """
    db = Session()
    try:
        destacados = db.query(Producto).filter(
            Producto.activo == True,
            Producto.destacado == True
        ).limit(6).all()
        categorias = db.query(Categoria).filter(Categoria.activa == True).all()
        return render_template('index.html', destacados=destacados, categorias=categorias)
    finally:
        db.close()


# ============================================================================
# CATALOGO DE PRODUCTOS (PUBLICO)
# ============================================================================

@app.route('/catalogo')
def catalogo():
    """
    Muestra todos los productos con filtro por categoria.
    El parametro ?categoria=ID filtra por categoria.
    """
    db = Session()
    try:
        categoria_id = request.args.get('categoria', type=int)
        categorias = db.query(Categoria).filter(Categoria.activa == True).all()

        query = db.query(Producto).filter(Producto.activo == True)
        if categoria_id:
            query = query.filter(Producto.categoria_id == categoria_id)

        productos = query.order_by(Producto.nombre).all()
        return render_template('productos/catalogo.html',
                               productos=productos,
                               categorias=categorias,
                               categoria_actual=categoria_id)
    finally:
        db.close()


@app.route('/producto/<int:id>')
def ver_producto(id):
    """Detalle de un producto."""
    db = Session()
    try:
        producto = db.query(Producto).get(id)
        if not producto or not producto.activo:
            flash('Producto no encontrado', 'danger')
            return redirect(url_for('catalogo'))
        return render_template('productos/detalle.html', producto=producto)
    finally:
        db.close()


# ============================================================================
# CARRITO DE COMPRAS
# ============================================================================
# El carrito funciona asi:
# 1. Cada usuario tiene UN carrito (se crea automaticamente)
# 2. Al agregar un producto, se busca si ya existe en el carrito
#    - Si existe: se incrementa la cantidad
#    - Si no existe: se crea un nuevo ItemCarrito
# 3. Al hacer checkout, los items se copian a un Pedido
# ============================================================================

def obtener_o_crear_carrito(db, usuario_id):
    """Obtiene el carrito del usuario o crea uno nuevo."""
    carrito = db.query(Carrito).filter(Carrito.usuario_id == usuario_id).first()
    if not carrito:
        carrito = Carrito(usuario_id=usuario_id)
        db.add(carrito)
        db.commit()
    return carrito


@app.route('/carrito')
@login_required
def ver_carrito():
    """Muestra el carrito del usuario."""
    db = Session()
    try:
        carrito = obtener_o_crear_carrito(db, session['usuario_id'])
        return render_template('carrito/ver.html', carrito=carrito)
    finally:
        db.close()


@app.route('/carrito/agregar/<int:producto_id>', methods=['POST'])
@login_required
def agregar_al_carrito(producto_id):
    """
    Agrega un producto al carrito.
    Si el producto ya esta en el carrito, incrementa la cantidad.
    Verifica que haya stock disponible.
    """
    db = Session()
    try:
        producto = db.query(Producto).get(producto_id)
        if not producto or not producto.activo:
            flash('Producto no encontrado', 'danger')
            return redirect(url_for('catalogo'))

        if not producto.en_stock:
            flash('Producto sin stock disponible', 'warning')
            return redirect(url_for('ver_producto', id=producto_id))

        carrito = obtener_o_crear_carrito(db, session['usuario_id'])

        # Buscar si el producto ya esta en el carrito
        item = db.query(ItemCarrito).filter(
            ItemCarrito.carrito_id == carrito.id,
            ItemCarrito.producto_id == producto_id
        ).first()

        cantidad = int(request.form.get('cantidad', 1))

        if item:
            # Ya existe: incrementar cantidad
            if item.cantidad + cantidad > producto.stock:
                flash(f'Solo hay {producto.stock} unidades disponibles', 'warning')
            else:
                item.cantidad += cantidad
                flash(f'"{producto.nombre}" actualizado en el carrito', 'success')
        else:
            # No existe: crear nuevo item
            if cantidad > producto.stock:
                flash(f'Solo hay {producto.stock} unidades disponibles', 'warning')
            else:
                item = ItemCarrito(carrito_id=carrito.id, producto_id=producto_id, cantidad=cantidad)
                db.add(item)
                flash(f'"{producto.nombre}" agregado al carrito', 'success')

        db.commit()
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()

    return redirect(request.referrer or url_for('catalogo'))


@app.route('/carrito/actualizar/<int:item_id>', methods=['POST'])
@login_required
def actualizar_carrito(item_id):
    """Actualiza la cantidad de un item en el carrito."""
    db = Session()
    try:
        item = db.query(ItemCarrito).get(item_id)
        if not item:
            flash('Item no encontrado', 'danger')
            return redirect(url_for('ver_carrito'))

        # Verificar que el item pertenece al usuario actual
        if item.carrito.usuario_id != session['usuario_id']:
            flash('No autorizado', 'danger')
            return redirect(url_for('ver_carrito'))

        cantidad = int(request.form.get('cantidad', 1))
        if cantidad <= 0:
            db.delete(item)
            flash('Item eliminado del carrito', 'info')
        elif cantidad > item.producto.stock:
            flash(f'Solo hay {item.producto.stock} unidades disponibles', 'warning')
        else:
            item.cantidad = cantidad
            flash('Cantidad actualizada', 'success')

        db.commit()
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()

    return redirect(url_for('ver_carrito'))


@app.route('/carrito/eliminar/<int:item_id>', methods=['POST'])
@login_required
def eliminar_del_carrito(item_id):
    """Elimina un item del carrito."""
    db = Session()
    try:
        item = db.query(ItemCarrito).get(item_id)
        if item and item.carrito.usuario_id == session['usuario_id']:
            db.delete(item)
            db.commit()
            flash('Producto eliminado del carrito', 'info')
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()

    return redirect(url_for('ver_carrito'))


# ============================================================================
# CHECKOUT Y PEDIDOS
# ============================================================================
# El checkout convierte el carrito en un pedido:
# 1. Verifica que el carrito no este vacio
# 2. Verifica stock de cada producto
# 3. Crea el Pedido con ItemPedido (copia del carrito)
# 4. Reduce el stock de cada producto
# 5. Vacia el carrito
# ============================================================================

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """
    Proceso de checkout.
    GET: muestra resumen del pedido y pide direccion
    POST: crea el pedido
    """
    db = Session()
    try:
        carrito = obtener_o_crear_carrito(db, session['usuario_id'])

        if not carrito.items:
            flash('Tu carrito esta vacio', 'warning')
            return redirect(url_for('catalogo'))

        if request.method == 'POST':
            direccion = request.form.get('direccion', '').strip()
            if not direccion:
                flash('La direccion de envio es obligatoria', 'danger')
                return render_template('pedidos/checkout.html', carrito=carrito)

            # Verificar stock antes de crear el pedido
            for item in carrito.items:
                if item.cantidad > item.producto.stock:
                    flash(f'"{item.producto.nombre}" no tiene suficiente stock', 'danger')
                    return render_template('pedidos/checkout.html', carrito=carrito)

            # Crear el pedido
            pedido = Pedido(
                usuario_id=session['usuario_id'],
                total=carrito.total,
                direccion_envio=direccion
            )
            db.add(pedido)
            db.flush()  # Para obtener el ID del pedido

            # Copiar items del carrito al pedido y reducir stock
            for item in carrito.items:
                item_pedido = ItemPedido(
                    pedido_id=pedido.id,
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                    precio_unitario=item.producto.precio
                )
                db.add(item_pedido)
                item.producto.stock -= item.cantidad

            # Vaciar el carrito
            for item in carrito.items:
                db.delete(item)

            db.commit()
            flash('Pedido creado exitosamente!', 'success')
            return redirect(url_for('confirmacion_pedido', id=pedido.id))

        return render_template('pedidos/checkout.html', carrito=carrito)
    except Exception as e:
        db.rollback()
        flash(f'Error al crear pedido: {e}', 'danger')
        return redirect(url_for('ver_carrito'))
    finally:
        db.close()


@app.route('/pedido/<int:id>/confirmacion')
@login_required
def confirmacion_pedido(id):
    """Pagina de confirmacion despues del checkout."""
    db = Session()
    try:
        pedido = db.query(Pedido).get(id)
        if not pedido or pedido.usuario_id != session['usuario_id']:
            flash('Pedido no encontrado', 'danger')
            return redirect(url_for('mis_pedidos'))
        return render_template('pedidos/confirmacion.html', pedido=pedido)
    finally:
        db.close()


@app.route('/pedidos')
@login_required
def mis_pedidos():
    """Lista los pedidos del usuario actual."""
    db = Session()
    try:
        pedidos = db.query(Pedido).filter(
            Pedido.usuario_id == session['usuario_id']
        ).order_by(Pedido.fecha_creacion.desc()).all()
        return render_template('pedidos/mis_pedidos.html', pedidos=pedidos)
    finally:
        db.close()


@app.route('/pedido/<int:id>')
@login_required
def ver_pedido(id):
    """Detalle de un pedido."""
    db = Session()
    try:
        pedido = db.query(Pedido).get(id)
        if not pedido:
            flash('Pedido no encontrado', 'danger')
            return redirect(url_for('mis_pedidos'))
        # Solo el dueno o admin puede ver el pedido
        if pedido.usuario_id != session['usuario_id'] and session.get('usuario_rol') != 'admin':
            flash('No autorizado', 'danger')
            return redirect(url_for('mis_pedidos'))
        return render_template('pedidos/detalle.html', pedido=pedido)
    finally:
        db.close()


# ============================================================================
# PANEL DE ADMINISTRACION
# ============================================================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Dashboard de administracion con estadisticas."""
    db = Session()
    try:
        stats = {
            'total_productos': db.query(Producto).count(),
            'total_categorias': db.query(Categoria).count(),
            'total_pedidos': db.query(Pedido).count(),
            'total_usuarios': db.query(Usuario).count(),
            'pedidos_pendientes': db.query(Pedido).filter(Pedido.estado == 'pendiente').count(),
            'productos_sin_stock': db.query(Producto).filter(Producto.stock == 0).count(),
        }
        pedidos_recientes = db.query(Pedido).order_by(Pedido.fecha_creacion.desc()).limit(5).all()
        return render_template('admin/dashboard.html', stats=stats, pedidos_recientes=pedidos_recientes)
    finally:
        db.close()


# --- Admin: Productos ---

@app.route('/admin/productos')
@admin_required
def admin_productos():
    """Lista todos los productos para administracion."""
    db = Session()
    try:
        productos = db.query(Producto).order_by(Producto.nombre).all()
        return render_template('admin/productos.html', productos=productos)
    finally:
        db.close()


@app.route('/admin/productos/nuevo', methods=['GET', 'POST'])
@admin_required
def admin_crear_producto():
    """Crear un nuevo producto."""
    db = Session()
    try:
        categorias = db.query(Categoria).filter(Categoria.activa == True).all()

        if request.method == 'POST':
            producto = Producto(
                nombre=request.form['nombre'],
                descripcion=request.form.get('descripcion', ''),
                precio=float(request.form['precio']),
                stock=int(request.form.get('stock', 0)),
                imagen_url=request.form.get('imagen_url', ''),
                destacado='destacado' in request.form,
                categoria_id=int(request.form['categoria_id']) if request.form.get('categoria_id') else None
            )
            db.add(producto)
            db.commit()
            flash(f'Producto "{producto.nombre}" creado', 'success')
            return redirect(url_for('admin_productos'))

        return render_template('admin/form_producto.html', producto=None, categorias=categorias)
    finally:
        db.close()


@app.route('/admin/productos/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def admin_editar_producto(id):
    """Editar un producto existente."""
    db = Session()
    try:
        producto = db.query(Producto).get(id)
        if not producto:
            flash('Producto no encontrado', 'danger')
            return redirect(url_for('admin_productos'))

        categorias = db.query(Categoria).filter(Categoria.activa == True).all()

        if request.method == 'POST':
            producto.nombre = request.form['nombre']
            producto.descripcion = request.form.get('descripcion', '')
            producto.precio = float(request.form['precio'])
            producto.stock = int(request.form.get('stock', 0))
            producto.imagen_url = request.form.get('imagen_url', '')
            producto.destacado = 'destacado' in request.form
            producto.activo = 'activo' in request.form
            producto.categoria_id = int(request.form['categoria_id']) if request.form.get('categoria_id') else None
            db.commit()
            flash(f'Producto "{producto.nombre}" actualizado', 'success')
            return redirect(url_for('admin_productos'))

        return render_template('admin/form_producto.html', producto=producto, categorias=categorias)
    finally:
        db.close()


@app.route('/admin/productos/<int:id>/eliminar', methods=['POST'])
@admin_required
def admin_eliminar_producto(id):
    """Eliminar un producto."""
    db = Session()
    try:
        producto = db.query(Producto).get(id)
        if producto:
            nombre = producto.nombre
            db.delete(producto)
            db.commit()
            flash(f'Producto "{nombre}" eliminado', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error al eliminar: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('admin_productos'))


# --- Admin: Categorias ---

@app.route('/admin/categorias')
@admin_required
def admin_categorias():
    db = Session()
    try:
        categorias = db.query(Categoria).order_by(Categoria.nombre).all()
        return render_template('admin/categorias.html', categorias=categorias)
    finally:
        db.close()


@app.route('/admin/categorias/nueva', methods=['GET', 'POST'])
@admin_required
def admin_crear_categoria():
    if request.method == 'POST':
        db = Session()
        try:
            categoria = Categoria(
                nombre=request.form['nombre'],
                descripcion=request.form.get('descripcion', '')
            )
            db.add(categoria)
            db.commit()
            flash(f'Categoria "{categoria.nombre}" creada', 'success')
            return redirect(url_for('admin_categorias'))
        except Exception as e:
            db.rollback()
            flash(f'Error: {e}', 'danger')
        finally:
            db.close()
    return render_template('admin/form_categoria.html', categoria=None)


@app.route('/admin/categorias/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def admin_editar_categoria(id):
    db = Session()
    try:
        categoria = db.query(Categoria).get(id)
        if not categoria:
            flash('Categoria no encontrada', 'danger')
            return redirect(url_for('admin_categorias'))

        if request.method == 'POST':
            categoria.nombre = request.form['nombre']
            categoria.descripcion = request.form.get('descripcion', '')
            categoria.activa = 'activa' in request.form
            db.commit()
            flash(f'Categoria "{categoria.nombre}" actualizada', 'success')
            return redirect(url_for('admin_categorias'))

        return render_template('admin/form_categoria.html', categoria=categoria)
    finally:
        db.close()


@app.route('/admin/categorias/<int:id>/eliminar', methods=['POST'])
@admin_required
def admin_eliminar_categoria(id):
    db = Session()
    try:
        categoria = db.query(Categoria).get(id)
        if categoria:
            nombre = categoria.nombre
            db.delete(categoria)
            db.commit()
            flash(f'Categoria "{nombre}" eliminada', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('admin_categorias'))


# --- Admin: Pedidos ---

@app.route('/admin/pedidos')
@admin_required
def admin_pedidos():
    """Lista todos los pedidos."""
    db = Session()
    try:
        pedidos = db.query(Pedido).order_by(Pedido.fecha_creacion.desc()).all()
        return render_template('admin/pedidos.html', pedidos=pedidos)
    finally:
        db.close()


@app.route('/admin/pedidos/<int:id>/estado', methods=['POST'])
@admin_required
def admin_cambiar_estado_pedido(id):
    """Cambia el estado de un pedido."""
    db = Session()
    try:
        pedido = db.query(Pedido).get(id)
        if not pedido:
            flash('Pedido no encontrado', 'danger')
            return redirect(url_for('admin_pedidos'))

        nuevo_estado = request.form.get('estado')
        estados_validos = ['pendiente', 'pagado', 'enviado', 'entregado', 'cancelado']
        if nuevo_estado in estados_validos:
            pedido.estado = nuevo_estado
            db.commit()
            flash(f'Pedido #{pedido.id} actualizado a "{nuevo_estado}"', 'success')
        else:
            flash('Estado no valido', 'danger')
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('admin_pedidos'))


# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('error.html', mensaje='Pagina no encontrada'), 404

@app.errorhandler(500)
def error_servidor(e):
    return render_template('error.html', mensaje='Error interno del servidor'), 500

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("SEMANA 10 - PROYECTO 1: MINI TIENDA E-COMMERCE")
    print("=" * 70)

    crear_tablas()
    crear_datos_ejemplo()

    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                    MINI TIENDA E-COMMERCE                           ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║  URL: http://localhost:5010                                         ║
║                                                                     ║
║  RUTAS PUBLICAS:                                                    ║
║  /                  → Pagina principal (productos destacados)       ║
║  /catalogo          → Catalogo completo                             ║
║  /producto/<id>     → Detalle de producto                           ║
║  /login             → Iniciar sesion                                ║
║  /registro          → Crear cuenta                                  ║
║                                                                     ║
║  RUTAS PROTEGIDAS (login):                                          ║
║  /carrito           → Ver carrito                                   ║
║  /checkout          → Procesar compra                               ║
║  /pedidos           → Mis pedidos                                   ║
║                                                                     ║
║  ADMIN:                                                             ║
║  /admin             → Dashboard                                     ║
║  /admin/productos   → Gestionar productos                           ║
║  /admin/categorias  → Gestionar categorias                          ║
║  /admin/pedidos     → Gestionar pedidos                             ║
║                                                                     ║
║  CREDENCIALES: admin@ejemplo.com / admin123                         ║
╚═══════════════════════════════════════════════════════════════════════╝
    """)

    app.run(debug=True, port=5010)
