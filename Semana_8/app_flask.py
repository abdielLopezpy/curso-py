# ============================================================================
# SEMANA 8: Aplicación Flask Completa con Neon (PostgreSQL)
# ============================================================================
# Esta es una aplicación web completa que demuestra:
# - Flask como framework web
# - SQLAlchemy como ORM
# - Neon (PostgreSQL) como base de datos en la nube
# - CRUD completo para múltiples entidades
#
# CÓMO EJECUTAR:
# 1. Configura tu DATABASE_URL abajo
# 2. Ejecuta: python app_flask.py
# 3. Abre: http://localhost:5000
# ============================================================================

# ============================================================================
# IMPORTACIONES
# ============================================================================
# Flask: framework web minimalista
# SQLAlchemy: ORM para base de datos
# ============================================================================

from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, scoped_session
from datetime import datetime
import os

# ============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================================================

app = Flask(__name__)
app.secret_key = 'clave-secreta-cambiar-en-produccion'  # Para mensajes flash

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

# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

# Base para los modelos
Base = declarative_base()

# Fábrica de sesiones (scoped para Flask)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


# ============================================================================
# MODELOS DE LA BASE DE DATOS
# ============================================================================
# Estos modelos definen la estructura de nuestras tablas.
# Puedes agregar nuevos modelos siguiendo el mismo patrón.
# ============================================================================

class Categoria(Base):
    """
    Modelo para categorías de productos.

    Una categoría agrupa productos relacionados.
    Relación: Una categoría tiene MUCHOS productos.
    """
    __tablename__ = 'categorias'

    # Columnas
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    activa = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Relación con productos
    productos = relationship(
        "Producto",
        back_populates="categoria",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Categoria {self.nombre}>"

    @property
    def cantidad_productos(self):
        """Retorna la cantidad de productos en esta categoría."""
        return len(self.productos)


class Producto(Base):
    """
    Modelo para productos.

    Cada producto pertenece a una categoría.
    Relación: Un producto pertenece a UNA categoría.
    """
    __tablename__ = 'productos'

    # Columnas básicas
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # Clave foránea a categoría
    categoria_id = Column(Integer, ForeignKey('categorias.id'))

    # Relación con categoría
    categoria = relationship("Categoria", back_populates="productos")

    def __repr__(self):
        return f"<Producto {self.nombre}>"

    @property
    def precio_formateado(self):
        """Retorna el precio con formato de moneda."""
        return f"${self.precio:.2f}"


# ============================================================================
# PLANTILLA PARA AGREGAR NUEVAS ENTIDADES
# ============================================================================
# Copia y modifica esta plantilla para agregar nuevas entidades al sistema.
# ============================================================================

# class NuevaEntidad(Base):
#     """
#     Plantilla para crear nuevas entidades.
#
#     PASOS PARA AGREGAR UNA NUEVA ENTIDAD:
#     1. Copia esta clase y renómbrala
#     2. Define __tablename__
#     3. Define las columnas que necesites
#     4. (Opcional) Agrega relaciones con otras entidades
#     5. Agrega las rutas CRUD (ver sección de rutas abajo)
#     6. Crea las plantillas HTML en templates/tu_entidad/
#     7. Reinicia la aplicación
#     """
#     __tablename__ = 'nueva_entidad'
#
#     id = Column(Integer, primary_key=True)
#     nombre = Column(String(100), nullable=False)
#     descripcion = Column(Text)
#     activo = Column(Boolean, default=True)
#     fecha_creacion = Column(DateTime, default=datetime.utcnow)
#
#     # Si necesitas una relación con otra tabla:
#     # otra_entidad_id = Column(Integer, ForeignKey('otra_entidad.id'))
#     # otra_entidad = relationship("OtraEntidad", back_populates="nuevas_entidades")
#
#     def __repr__(self):
#         return f"<NuevaEntidad {self.nombre}>"


# ============================================================================
# CREAR LAS TABLAS
# ============================================================================

def crear_tablas(reset=False):
    """Crea todas las tablas en la base de datos."""
    if reset:
        # Eliminar tablas existentes con CASCADE (elimina dependencias)
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS productos CASCADE"))
            conn.execute(text("DROP TABLE IF EXISTS categorias CASCADE"))
            conn.commit()
        print("[OK] Tablas eliminadas (CASCADE)")
    Base.metadata.create_all(engine)
    print("[OK] Tablas creadas/verificadas")


# ============================================================================
# RUTAS DE LA APLICACIÓN
# ============================================================================
# Las rutas definen las URLs y qué hacer cuando se accede a ellas.
# ============================================================================

# ----------------------------------------------------------------------------
# PÁGINA PRINCIPAL
# ----------------------------------------------------------------------------

@app.route('/')
def index():
    """
    Página principal de la aplicación.

    Muestra un resumen con estadísticas y enlaces a las secciones.
    """
    session = Session()
    try:
        # Obtener estadísticas
        total_categorias = session.query(Categoria).count()
        total_productos = session.query(Producto).count()
        productos_activos = session.query(Producto).filter(Producto.activo == True).count()
        productos_sin_stock = session.query(Producto).filter(Producto.stock == 0).count()

        return render_template(
            'index.html',
            total_categorias=total_categorias,
            total_productos=total_productos,
            productos_activos=productos_activos,
            productos_sin_stock=productos_sin_stock
        )
    finally:
        session.close()


# ----------------------------------------------------------------------------
# RUTAS CRUD PARA CATEGORÍAS
# ----------------------------------------------------------------------------

@app.route('/categorias')
def listar_categorias():
    """Lista todas las categorías."""
    session = Session()
    try:
        categorias = session.query(Categoria).order_by(Categoria.nombre).all()
        return render_template('categorias/lista.html', categorias=categorias)
    finally:
        session.close()


@app.route('/categorias/nueva', methods=['GET', 'POST'])
def crear_categoria():
    """Crea una nueva categoría."""
    if request.method == 'POST':
        session = Session()
        try:
            categoria = Categoria(
                nombre=request.form['nombre'],
                descripcion=request.form.get('descripcion', '')
            )
            session.add(categoria)
            session.commit()
            flash(f'Categoría "{categoria.nombre}" creada exitosamente', 'success')
            return redirect(url_for('listar_categorias'))
        except Exception as e:
            session.rollback()
            flash(f'Error al crear categoría: {e}', 'error')
        finally:
            session.close()

    return render_template('categorias/formulario.html', categoria=None)


@app.route('/categorias/<int:id>')
def ver_categoria(id):
    """Muestra el detalle de una categoría."""
    session = Session()
    try:
        categoria = session.query(Categoria).get(id)
        if not categoria:
            flash('Categoría no encontrada', 'error')
            return redirect(url_for('listar_categorias'))
        return render_template('categorias/detalle.html', categoria=categoria)
    finally:
        session.close()


@app.route('/categorias/<int:id>/editar', methods=['GET', 'POST'])
def editar_categoria(id):
    """Edita una categoría existente."""
    session = Session()
    try:
        categoria = session.query(Categoria).get(id)
        if not categoria:
            flash('Categoría no encontrada', 'error')
            return redirect(url_for('listar_categorias'))

        if request.method == 'POST':
            categoria.nombre = request.form['nombre']
            categoria.descripcion = request.form.get('descripcion', '')
            session.commit()
            flash(f'Categoría "{categoria.nombre}" actualizada', 'success')
            return redirect(url_for('listar_categorias'))

        return render_template('categorias/formulario.html', categoria=categoria)
    finally:
        session.close()


@app.route('/categorias/<int:id>/eliminar', methods=['POST'])
def eliminar_categoria(id):
    """Elimina una categoría."""
    session = Session()
    try:
        categoria = session.query(Categoria).get(id)
        if categoria:
            nombre = categoria.nombre
            session.delete(categoria)
            session.commit()
            flash(f'Categoría "{nombre}" eliminada', 'success')
        else:
            flash('Categoría no encontrada', 'error')
    except Exception as e:
        session.rollback()
        flash(f'Error al eliminar: {e}', 'error')
    finally:
        session.close()
    return redirect(url_for('listar_categorias'))


# ----------------------------------------------------------------------------
# RUTAS CRUD PARA PRODUCTOS
# ----------------------------------------------------------------------------

@app.route('/productos')
def listar_productos():
    """Lista todos los productos."""
    session = Session()
    try:
        productos = session.query(Producto).order_by(Producto.nombre).all()
        return render_template('productos/lista.html', productos=productos)
    finally:
        session.close()


@app.route('/productos/nuevo', methods=['GET', 'POST'])
def crear_producto():
    """Crea un nuevo producto."""
    session = Session()
    try:
        categorias = session.query(Categoria).filter(Categoria.activa == True).all()

        if request.method == 'POST':
            producto = Producto(
                nombre=request.form['nombre'],
                descripcion=request.form.get('descripcion', ''),
                precio=float(request.form['precio']),
                stock=int(request.form.get('stock', 0)),
                categoria_id=int(request.form['categoria_id']) if request.form.get('categoria_id') else None
            )
            session.add(producto)
            session.commit()
            flash(f'Producto "{producto.nombre}" creado exitosamente', 'success')
            return redirect(url_for('listar_productos'))

        return render_template('productos/formulario.html', producto=None, categorias=categorias)
    finally:
        session.close()


@app.route('/productos/<int:id>')
def ver_producto(id):
    """Muestra el detalle de un producto."""
    session = Session()
    try:
        producto = session.query(Producto).get(id)
        if not producto:
            flash('Producto no encontrado', 'error')
            return redirect(url_for('listar_productos'))
        return render_template('productos/detalle.html', producto=producto)
    finally:
        session.close()


@app.route('/productos/<int:id>/editar', methods=['GET', 'POST'])
def editar_producto(id):
    """Edita un producto existente."""
    session = Session()
    try:
        producto = session.query(Producto).get(id)
        categorias = session.query(Categoria).filter(Categoria.activa == True).all()

        if not producto:
            flash('Producto no encontrado', 'error')
            return redirect(url_for('listar_productos'))

        if request.method == 'POST':
            producto.nombre = request.form['nombre']
            producto.descripcion = request.form.get('descripcion', '')
            producto.precio = float(request.form['precio'])
            producto.stock = int(request.form.get('stock', 0))
            producto.categoria_id = int(request.form['categoria_id']) if request.form.get('categoria_id') else None
            session.commit()
            flash(f'Producto "{producto.nombre}" actualizado', 'success')
            return redirect(url_for('listar_productos'))

        return render_template('productos/formulario.html', producto=producto, categorias=categorias)
    finally:
        session.close()


@app.route('/productos/<int:id>/eliminar', methods=['POST'])
def eliminar_producto(id):
    """Elimina un producto."""
    session = Session()
    try:
        producto = session.query(Producto).get(id)
        if producto:
            nombre = producto.nombre
            session.delete(producto)
            session.commit()
            flash(f'Producto "{nombre}" eliminado', 'success')
        else:
            flash('Producto no encontrado', 'error')
    except Exception as e:
        session.rollback()
        flash(f'Error al eliminar: {e}', 'error')
    finally:
        session.close()
    return redirect(url_for('listar_productos'))


# ----------------------------------------------------------------------------
# PLANTILLA DE RUTAS PARA NUEVAS ENTIDADES
# ----------------------------------------------------------------------------
# Copia y modifica estas rutas para agregar nuevas entidades al sistema.
# ----------------------------------------------------------------------------

# @app.route('/mi_entidad')
# def listar_mi_entidad():
#     """Lista todos los items de MiEntidad."""
#     session = Session()
#     try:
#         items = session.query(MiEntidad).order_by(MiEntidad.nombre).all()
#         return render_template('mi_entidad/lista.html', items=items)
#     finally:
#         session.close()
#
# @app.route('/mi_entidad/nuevo', methods=['GET', 'POST'])
# def crear_mi_entidad():
#     """Crea un nuevo item de MiEntidad."""
#     if request.method == 'POST':
#         session = Session()
#         try:
#             item = MiEntidad(
#                 nombre=request.form['nombre'],
#                 descripcion=request.form.get('descripcion', '')
#             )
#             session.add(item)
#             session.commit()
#             flash(f'Item "{item.nombre}" creado exitosamente', 'success')
#             return redirect(url_for('listar_mi_entidad'))
#         finally:
#             session.close()
#     return render_template('mi_entidad/formulario.html', item=None)


# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def pagina_no_encontrada(e):
    """Maneja errores 404."""
    return render_template('error.html', mensaje='Página no encontrada'), 404


@app.errorhandler(500)
def error_servidor(e):
    """Maneja errores 500."""
    return render_template('error.html', mensaje='Error interno del servidor'), 500


# ============================================================================
# CERRAR SESIÓN AL FINAL DE CADA REQUEST
# ============================================================================

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Cierra la sesión de base de datos al final de cada request."""
    Session.remove()


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("SEMANA 8: Aplicación Flask con Neon")
    print("=" * 70)

    # Crear las tablas (reset=False conserva los datos existentes)
    crear_tablas(reset=False)

    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                         APLICACIÓN INICIADA                               ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  URL: http://localhost:5001                                               ║
║                                                                           ║
║  RUTAS DISPONIBLES:                                                       ║
║  ──────────────────                                                       ║
║  /                    → Página principal                                  ║
║  /categorias          → Lista de categorías                               ║
║  /categorias/nueva    → Crear categoría                                   ║
║  /productos           → Lista de productos                                ║
║  /productos/nuevo     → Crear producto                                    ║
║                                                                           ║
║  Presiona Ctrl+C para detener el servidor                                 ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)

    # Ejecutar la aplicación
    app.run(debug=True, port=5002)
