# ============================================================================
# SEMANA 10 - PROYECTO 3: SISTEMA DE PUBLICIDAD PARA AEROPUERTOS
# ============================================================================
# Plataforma B2B para contratar espacios publicitarios en aeropuertos.
# Integra todos los conceptos del curso:
#
# - Modelos SQLAlchemy con relaciones complejas (Semanas 6-7)
# - CRUD completo (Semana 8)
# - Autenticacion con sesiones y roles (Semana 9)
# - Gestion de aeropuertos, espacios publicitarios, campanas y contratos
#
# CONCEPTOS DE DOMINIO:
# - Codigo IATA: codigo de 3 letras que identifica un aeropuerto (ej: SJO)
# - Espacio publicitario: lugar fisico donde se coloca publicidad
# - Campana: conjunto de acciones publicitarias de un cliente
# - Contrato: acuerdo para usar un espacio en una campana
#
# COMO EJECUTAR:
# 1. pip install flask sqlalchemy psycopg2-binary werkzeug
# 2. python app.py
# 3. Abre: http://localhost:5012
#
# CREDENCIALES:
# - Admin: admin@ejemplo.com / admin123
# - Cliente: cliente@ejemplo.com / cliente123
# ============================================================================

from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, date
import os

# ============================================================================
# CONFIGURACION
# ============================================================================

app = Flask(__name__)
app.secret_key = 'publicidad-aeropuertos-secreto'

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://neondb_owner:npg_xnKz5VIdoiv7@ep-hidden-voice-ahdtczjv-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
)

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
Base = declarative_base()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


# ============================================================================
# MODELOS (prefijo "pub_" para evitar conflictos)
# ============================================================================

class Usuario(Base):
    """Usuario del sistema. admin = gestiona todo, cliente = contrata publicidad."""
    __tablename__ = 'pub_usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    empresa = Column(String(200))
    telefono = Column(String(20))
    rol = Column(String(20), default='cliente')
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    campanas = relationship("Campana", back_populates="cliente")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def es_admin(self):
        return self.rol == 'admin'


# ----------------------------------------------------------------------------
# MODELO: Aeropuerto
# ----------------------------------------------------------------------------
# Representa un aeropuerto real con su codigo IATA.
# El codigo IATA es un estandar internacional de 3 letras:
# - SJO = Juan Santamaria (Costa Rica)
# - PTY = Tocumen (Panama)
# - BOG = El Dorado (Colombia)
# ----------------------------------------------------------------------------

class Aeropuerto(Base):
    __tablename__ = 'pub_aeropuertos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    codigo_iata = Column(String(3), nullable=False, unique=True)
    ciudad = Column(String(100), nullable=False)
    pais = Column(String(100), nullable=False)
    pasajeros_anuales = Column(Integer, default=0)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    espacios = relationship("EspacioPublicitario", back_populates="aeropuerto", cascade="all, delete-orphan")

    @property
    def pasajeros_formateado(self):
        """Formatea millones de pasajeros para mostrar."""
        if self.pasajeros_anuales >= 1000000:
            return f"{self.pasajeros_anuales / 1000000:.1f}M"
        elif self.pasajeros_anuales >= 1000:
            return f"{self.pasajeros_anuales / 1000:.0f}K"
        return str(self.pasajeros_anuales)

    @property
    def espacios_disponibles(self):
        return sum(1 for e in self.espacios if e.disponible)


# ----------------------------------------------------------------------------
# MODELO: EspacioPublicitario
# ----------------------------------------------------------------------------
# Un espacio fisico donde se coloca publicidad dentro del aeropuerto.
# Tipos: pantalla_digital, valla, banner, stand, display_interactivo
# Ubicaciones: terminal, sala_espera, pasillo, exterior, gate
# Precio mensual: lo que cuesta contratar ese espacio por mes.
# ----------------------------------------------------------------------------

class EspacioPublicitario(Base):
    __tablename__ = 'pub_espacios'

    id = Column(Integer, primary_key=True)
    aeropuerto_id = Column(Integer, ForeignKey('pub_aeropuertos.id'))
    nombre = Column(String(200), nullable=False)
    ubicacion = Column(String(50), nullable=False)  # terminal, sala_espera, etc.
    tipo = Column(String(50), nullable=False)        # pantalla_digital, valla, etc.
    dimensiones = Column(String(50))                  # ej: "3m x 2m"
    precio_mensual = Column(Float, nullable=False)
    disponible = Column(Boolean, default=True)
    descripcion = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    aeropuerto = relationship("Aeropuerto", back_populates="espacios")
    contratos = relationship("Contrato", back_populates="espacio")

    @property
    def precio_formateado(self):
        return f"${self.precio_mensual:,.2f}"

    @property
    def tipo_display(self):
        tipos = {
            'pantalla_digital': 'Pantalla Digital',
            'valla': 'Valla Publicitaria',
            'banner': 'Banner',
            'stand': 'Stand Promocional',
            'display_interactivo': 'Display Interactivo'
        }
        return tipos.get(self.tipo, self.tipo)

    @property
    def ubicacion_display(self):
        ubicaciones = {
            'terminal': 'Terminal',
            'sala_espera': 'Sala de Espera',
            'pasillo': 'Pasillo',
            'exterior': 'Exterior',
            'gate': 'Puerta de Embarque'
        }
        return ubicaciones.get(self.ubicacion, self.ubicacion)


# ----------------------------------------------------------------------------
# MODELO: Campana
# ----------------------------------------------------------------------------
# Una campana publicitaria de un cliente. Agrupa uno o varios contratos.
# Estados:
# - borrador: en preparacion
# - activa: campana en ejecucion
# - pausada: temporalmente detenida
# - completada: campana finalizada
# - cancelada: cancelada por el cliente o admin
# ----------------------------------------------------------------------------

class Campana(Base):
    __tablename__ = 'pub_campanas'

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('pub_usuarios.id'))
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    presupuesto = Column(Float, default=0)
    estado = Column(String(20), default='borrador')
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    cliente = relationship("Usuario", back_populates="campanas")
    contratos = relationship("Contrato", back_populates="campana", cascade="all, delete-orphan")

    @property
    def presupuesto_formateado(self):
        return f"${self.presupuesto:,.2f}"

    @property
    def estado_color(self):
        colores = {
            'borrador': 'secondary',
            'activa': 'success',
            'pausada': 'warning',
            'completada': 'info',
            'cancelada': 'danger'
        }
        return colores.get(self.estado, 'secondary')

    @property
    def total_contratos(self):
        return sum(c.precio_total for c in self.contratos)


# ----------------------------------------------------------------------------
# MODELO: Contrato
# ----------------------------------------------------------------------------
# Un contrato vincula una campana con un espacio publicitario.
# Tiene fechas de vigencia y precio total.
# Estados: pendiente, activo, vencido, cancelado
# ----------------------------------------------------------------------------

class Contrato(Base):
    __tablename__ = 'pub_contratos'

    id = Column(Integer, primary_key=True)
    campana_id = Column(Integer, ForeignKey('pub_campanas.id'))
    espacio_id = Column(Integer, ForeignKey('pub_espacios.id'))
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    precio_total = Column(Float, nullable=False)
    estado = Column(String(20), default='pendiente')
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    campana = relationship("Campana", back_populates="contratos")
    espacio = relationship("EspacioPublicitario", back_populates="contratos")

    @property
    def precio_formateado(self):
        return f"${self.precio_total:,.2f}"

    @property
    def estado_color(self):
        colores = {
            'pendiente': 'warning',
            'activo': 'success',
            'vencido': 'secondary',
            'cancelado': 'danger'
        }
        return colores.get(self.estado, 'secondary')


# ============================================================================
# CREAR TABLAS Y DATOS DE EJEMPLO
# ============================================================================

def crear_tablas():
    Base.metadata.create_all(engine)
    print("[OK] Tablas de Publicidad Aeropuertos creadas/verificadas")


def crear_datos_ejemplo():
    db = Session()
    try:
        if db.query(Usuario).filter(Usuario.email == 'admin@ejemplo.com').first():
            print("[OK] Datos ya existen")
            return

        # Admin
        admin = Usuario(nombre='Administrador', email='admin@ejemplo.com', rol='admin', empresa='AeroAds Corp')
        admin.set_password('admin123')
        db.add(admin)

        # Cliente
        cliente = Usuario(nombre='Carlos Publicista', email='cliente@ejemplo.com', rol='cliente',
                          empresa='MediaGroup Panama', telefono='6789-5678')
        cliente.set_password('cliente123')
        db.add(cliente)

        # Aeropuertos - Contexto Panama y Latinoamerica
        aeropuertos = [
            Aeropuerto(nombre='Aeropuerto Int. de Tocumen', codigo_iata='PTY', ciudad='Ciudad de Panama', pais='Panama', pasajeros_anuales=16000000),
            Aeropuerto(nombre='Aeropuerto Enrique Malek', codigo_iata='DAV', ciudad='David', pais='Panama', pasajeros_anuales=350000),
            Aeropuerto(nombre='Aeropuerto Scarlett Martinez', codigo_iata='RIH', ciudad='Rio Hato', pais='Panama', pasajeros_anuales=180000),
            Aeropuerto(nombre='Aeropuerto Int. El Dorado', codigo_iata='BOG', ciudad='Bogota', pais='Colombia', pasajeros_anuales=35000000),
            Aeropuerto(nombre='Aeropuerto Int. Benito Juarez', codigo_iata='MEX', ciudad='Ciudad de Mexico', pais='Mexico', pasajeros_anuales=50000000),
            Aeropuerto(nombre='Aeropuerto Int. de Ezeiza', codigo_iata='EZE', ciudad='Buenos Aires', pais='Argentina', pasajeros_anuales=14000000),
        ]
        for a in aeropuertos:
            db.add(a)
        db.flush()

        # Espacios publicitarios
        tipos = ['pantalla_digital', 'valla', 'banner', 'stand', 'display_interactivo']
        ubicaciones = ['terminal', 'sala_espera', 'pasillo', 'exterior', 'gate']

        espacios_data = [
            # PTY - Tocumen (aeropuerto principal de Panama)
            ('Pantalla Gigante Terminal 2', aeropuertos[0], 'terminal', 'pantalla_digital', '6m x 3m', 5000),
            ('Display Interactivo Gate B12', aeropuertos[0], 'gate', 'display_interactivo', '1.5m x 1m', 2200),
            ('Valla Exterior Llegadas', aeropuertos[0], 'exterior', 'valla', '8m x 3m', 4500),
            ('Stand Zona Duty Free T2', aeropuertos[0], 'terminal', 'stand', '4m x 4m', 6500),
            ('Banner Pasillo Conexiones', aeropuertos[0], 'pasillo', 'banner', '3m x 1.5m', 1800),
            ('Pantalla LED Migraciones', aeropuertos[0], 'terminal', 'pantalla_digital', '4m x 2m', 3500),
            # DAV - David
            ('Pantalla LED Terminal Principal', aeropuertos[1], 'terminal', 'pantalla_digital', '3m x 1.5m', 800),
            ('Valla Sala de Espera', aeropuertos[1], 'sala_espera', 'valla', '2m x 1m', 500),
            # RIH - Rio Hato
            ('Banner Entrada Terminal', aeropuertos[2], 'terminal', 'banner', '2m x 1m', 400),
            ('Stand Area de Check-in', aeropuertos[2], 'terminal', 'stand', '2m x 2m', 600),
            # BOG
            ('Pantalla HD Terminal 1', aeropuertos[3], 'terminal', 'pantalla_digital', '5m x 2.5m', 4000),
            ('Banner Puente Aereo', aeropuertos[3], 'pasillo', 'banner', '3m x 1m', 1500),
            ('Stand Premium Sala VIP', aeropuertos[3], 'sala_espera', 'stand', '4m x 4m', 6000),
            # MEX
            ('Mega Pantalla Terminal 2', aeropuertos[4], 'terminal', 'pantalla_digital', '8m x 4m', 8000),
            ('Valla Premium Acceso Principal', aeropuertos[4], 'exterior', 'valla', '12m x 5m', 7500),
            ('Stand Zona Comercial T2', aeropuertos[4], 'terminal', 'stand', '5m x 5m', 9000),
            # EZE
            ('Pantalla LED Migraciones EZE', aeropuertos[5], 'terminal', 'pantalla_digital', '4m x 2m', 3000),
            ('Banner Recogida Equipajes', aeropuertos[5], 'terminal', 'banner', '2.5m x 1.5m', 1200),
        ]

        for nombre, aeropuerto, ubicacion, tipo, dims, precio in espacios_data:
            espacio = EspacioPublicitario(
                aeropuerto_id=aeropuerto.id,
                nombre=nombre,
                ubicacion=ubicacion,
                tipo=tipo,
                dimensiones=dims,
                precio_mensual=precio,
                descripcion=f'Espacio publicitario tipo {tipo} ubicado en {ubicacion} del {aeropuerto.nombre}.'
            )
            db.add(espacio)

        db.commit()
        print("[OK] Datos de ejemplo creados (2 usuarios + 6 aeropuertos + 18 espacios)")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] {e}")
    finally:
        db.close()


# ============================================================================
# DECORADORES
# ============================================================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesion para acceder', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesion', 'warning')
            return redirect(url_for('login'))
        if session.get('usuario_rol') != 'admin':
            flash('No tienes permisos de administrador', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.context_processor
def inject_user():
    datos = {'usuario_actual': None, 'esta_logueado': False, 'es_admin': False}
    if 'usuario_id' in session:
        db = Session()
        try:
            usuario = db.query(Usuario).get(session['usuario_id'])
            if usuario:
                datos['usuario_actual'] = usuario
                datos['esta_logueado'] = True
                datos['es_admin'] = usuario.es_admin
        finally:
            db.close()
    return datos


# ============================================================================
# AUTENTICACION
# ============================================================================

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip().lower()
        empresa = request.form.get('empresa', '').strip()
        telefono = request.form.get('telefono', '').strip()
        password = request.form.get('password', '')
        confirmar = request.form.get('confirmar_password', '')

        errores = []
        if not nombre: errores.append('El nombre es obligatorio')
        if not email: errores.append('El email es obligatorio')
        if not empresa: errores.append('La empresa es obligatoria')
        if len(password) < 6: errores.append('La contrasena debe tener al menos 6 caracteres')
        if password != confirmar: errores.append('Las contrasenas no coinciden')

        if errores:
            for e in errores: flash(e, 'danger')
            return render_template('auth/registro.html', nombre=nombre, email=email, empresa=empresa, telefono=telefono)

        db = Session()
        try:
            if db.query(Usuario).filter(Usuario.email == email).first():
                flash('Ya existe una cuenta con ese email', 'danger')
                return render_template('auth/registro.html', nombre=nombre, email=email, empresa=empresa, telefono=telefono)

            usuario = Usuario(nombre=nombre, email=email, empresa=empresa, telefono=telefono)
            usuario.set_password(password)
            db.add(usuario)
            db.commit()
            flash('Cuenta creada! Inicia sesion.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.rollback()
            flash(f'Error: {e}', 'danger')
        finally:
            db.close()

    return render_template('auth/registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
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
            session['usuario_rol'] = usuario.rol
            flash(f'Bienvenido, {usuario.nombre}!', 'success')
            return redirect(url_for('index'))
        finally:
            db.close()

    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Sesion cerrada', 'info')
    return redirect(url_for('login'))


# ============================================================================
# PAGINA PRINCIPAL (CLIENTE)
# ============================================================================

@app.route('/')
@login_required
def index():
    db = Session()
    try:
        mis_campanas = db.query(Campana).filter(
            Campana.cliente_id == session['usuario_id']
        ).count()
        campanas_activas = db.query(Campana).filter(
            Campana.cliente_id == session['usuario_id'],
            Campana.estado == 'activa'
        ).count()
        mis_contratos = db.query(Contrato).join(Campana).filter(
            Campana.cliente_id == session['usuario_id']
        ).count()
        total_aeropuertos = db.query(Aeropuerto).filter(Aeropuerto.activo == True).count()

        campanas_recientes = db.query(Campana).filter(
            Campana.cliente_id == session['usuario_id']
        ).order_by(Campana.fecha_creacion.desc()).limit(5).all()

        return render_template('index.html',
                               mis_campanas=mis_campanas,
                               campanas_activas=campanas_activas,
                               mis_contratos=mis_contratos,
                               total_aeropuertos=total_aeropuertos,
                               campanas_recientes=campanas_recientes)
    finally:
        db.close()


# ============================================================================
# AEROPUERTOS (vista cliente)
# ============================================================================

@app.route('/aeropuertos')
@login_required
def listar_aeropuertos():
    db = Session()
    try:
        aeropuertos = db.query(Aeropuerto).filter(Aeropuerto.activo == True).order_by(Aeropuerto.nombre).all()
        return render_template('aeropuertos/lista.html', aeropuertos=aeropuertos)
    finally:
        db.close()


@app.route('/aeropuertos/<int:id>')
@login_required
def ver_aeropuerto(id):
    db = Session()
    try:
        aeropuerto = db.query(Aeropuerto).get(id)
        if not aeropuerto:
            flash('Aeropuerto no encontrado', 'danger')
            return redirect(url_for('listar_aeropuertos'))
        return render_template('aeropuertos/detalle.html', aeropuerto=aeropuerto)
    finally:
        db.close()


# ============================================================================
# ESPACIOS PUBLICITARIOS (vista cliente)
# ============================================================================

@app.route('/espacios')
@login_required
def listar_espacios():
    db = Session()
    try:
        aeropuerto_id = request.args.get('aeropuerto', type=int)
        tipo = request.args.get('tipo', '')

        query = db.query(EspacioPublicitario).filter(EspacioPublicitario.disponible == True)
        if aeropuerto_id:
            query = query.filter(EspacioPublicitario.aeropuerto_id == aeropuerto_id)
        if tipo:
            query = query.filter(EspacioPublicitario.tipo == tipo)

        espacios = query.order_by(EspacioPublicitario.precio_mensual).all()
        aeropuertos = db.query(Aeropuerto).filter(Aeropuerto.activo == True).all()
        tipos = ['pantalla_digital', 'valla', 'banner', 'stand', 'display_interactivo']

        return render_template('espacios/disponibles.html',
                               espacios=espacios, aeropuertos=aeropuertos,
                               tipos=tipos, aeropuerto_actual=aeropuerto_id, tipo_actual=tipo)
    finally:
        db.close()


@app.route('/espacios/<int:id>')
@login_required
def ver_espacio(id):
    db = Session()
    try:
        espacio = db.query(EspacioPublicitario).get(id)
        if not espacio:
            flash('Espacio no encontrado', 'danger')
            return redirect(url_for('listar_espacios'))
        return render_template('espacios/detalle.html', espacio=espacio)
    finally:
        db.close()


# ============================================================================
# CAMPANAS
# ============================================================================

@app.route('/campanas')
@login_required
def listar_campanas():
    db = Session()
    try:
        campanas = db.query(Campana).filter(
            Campana.cliente_id == session['usuario_id']
        ).order_by(Campana.fecha_creacion.desc()).all()
        return render_template('campanas/lista.html', campanas=campanas)
    finally:
        db.close()


@app.route('/campanas/nueva', methods=['GET', 'POST'])
@login_required
def crear_campana():
    if request.method == 'POST':
        db = Session()
        try:
            fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d').date() if request.form.get('fecha_inicio') else None
            fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d').date() if request.form.get('fecha_fin') else None

            campana = Campana(
                cliente_id=session['usuario_id'],
                nombre=request.form['nombre'],
                descripcion=request.form.get('descripcion', ''),
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                presupuesto=float(request.form.get('presupuesto', 0))
            )
            db.add(campana)
            db.commit()
            flash(f'Campana "{campana.nombre}" creada', 'success')
            return redirect(url_for('ver_campana', id=campana.id))
        except Exception as e:
            db.rollback()
            flash(f'Error: {e}', 'danger')
        finally:
            db.close()

    return render_template('campanas/formulario.html', campana=None)


@app.route('/campanas/<int:id>')
@login_required
def ver_campana(id):
    db = Session()
    try:
        campana = db.query(Campana).get(id)
        if not campana:
            flash('Campana no encontrada', 'danger')
            return redirect(url_for('listar_campanas'))
        if campana.cliente_id != session['usuario_id'] and session.get('usuario_rol') != 'admin':
            flash('No autorizado', 'danger')
            return redirect(url_for('listar_campanas'))
        return render_template('campanas/detalle.html', campana=campana)
    finally:
        db.close()


@app.route('/campanas/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_campana(id):
    db = Session()
    try:
        campana = db.query(Campana).get(id)
        if not campana or campana.cliente_id != session['usuario_id']:
            flash('Campana no encontrada', 'danger')
            return redirect(url_for('listar_campanas'))

        if request.method == 'POST':
            campana.nombre = request.form['nombre']
            campana.descripcion = request.form.get('descripcion', '')
            campana.presupuesto = float(request.form.get('presupuesto', 0))
            if request.form.get('fecha_inicio'):
                campana.fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d').date()
            if request.form.get('fecha_fin'):
                campana.fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d').date()
            db.commit()
            flash('Campana actualizada', 'success')
            return redirect(url_for('ver_campana', id=campana.id))

        return render_template('campanas/formulario.html', campana=campana)
    finally:
        db.close()


# ============================================================================
# CONTRATAR ESPACIO
# ============================================================================
# Flujo:
# 1. Cliente navega espacios disponibles
# 2. Selecciona un espacio y hace clic en "Contratar"
# 3. Selecciona campana, fechas de inicio y fin
# 4. Se calcula el precio total (meses x precio_mensual)
# 5. Se crea el contrato
# ============================================================================

@app.route('/contratar/<int:espacio_id>', methods=['GET', 'POST'])
@login_required
def contratar_espacio(espacio_id):
    db = Session()
    try:
        espacio = db.query(EspacioPublicitario).get(espacio_id)
        if not espacio or not espacio.disponible:
            flash('Espacio no disponible', 'danger')
            return redirect(url_for('listar_espacios'))

        campanas = db.query(Campana).filter(
            Campana.cliente_id == session['usuario_id'],
            Campana.estado.in_(['borrador', 'activa'])
        ).all()

        if request.method == 'POST':
            campana_id = request.form.get('campana_id', type=int)
            fecha_inicio_str = request.form.get('fecha_inicio', '')
            fecha_fin_str = request.form.get('fecha_fin', '')

            if not campana_id or not fecha_inicio_str or not fecha_fin_str:
                flash('Todos los campos son obligatorios', 'danger')
                return render_template('campanas/contratar.html', espacio=espacio, campanas=campanas)

            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()

            if fecha_fin <= fecha_inicio:
                flash('La fecha de fin debe ser posterior a la de inicio', 'danger')
                return render_template('campanas/contratar.html', espacio=espacio, campanas=campanas)

            # Calcular precio: meses (minimo 1) x precio mensual
            dias = (fecha_fin - fecha_inicio).days
            meses = max(1, dias / 30)
            precio_total = meses * espacio.precio_mensual

            contrato = Contrato(
                campana_id=campana_id,
                espacio_id=espacio_id,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                precio_total=round(precio_total, 2)
            )
            db.add(contrato)
            db.commit()
            flash(f'Contrato creado! Total: ${precio_total:,.2f}', 'success')
            return redirect(url_for('ver_campana', id=campana_id))

        return render_template('campanas/contratar.html', espacio=espacio, campanas=campanas)
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
        return redirect(url_for('listar_espacios'))
    finally:
        db.close()


# ============================================================================
# ADMINISTRACION
# ============================================================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    db = Session()
    try:
        total_contratos = db.query(Contrato).count()
        contratos_activos = db.query(Contrato).filter(Contrato.estado == 'activo').count()
        ingresos = sum(c.precio_total for c in db.query(Contrato).filter(Contrato.estado.in_(['activo', 'pendiente'])).all())
        total_espacios = db.query(EspacioPublicitario).count()
        espacios_ocupados = db.query(EspacioPublicitario).filter(EspacioPublicitario.disponible == False).count()

        stats = {
            'total_aeropuertos': db.query(Aeropuerto).count(),
            'total_espacios': total_espacios,
            'total_campanas': db.query(Campana).count(),
            'total_contratos': total_contratos,
            'ingresos': f"${ingresos:,.2f}",
            'espacios_ocupados': espacios_ocupados,
        }

        contratos_recientes = db.query(Contrato).order_by(Contrato.fecha_creacion.desc()).limit(5).all()
        return render_template('admin/dashboard.html', stats=stats, contratos_recientes=contratos_recientes)
    finally:
        db.close()


# --- Admin: Aeropuertos ---

@app.route('/admin/aeropuertos')
@admin_required
def admin_aeropuertos():
    db = Session()
    try:
        aeropuertos = db.query(Aeropuerto).order_by(Aeropuerto.nombre).all()
        return render_template('admin/aeropuertos.html', aeropuertos=aeropuertos)
    finally:
        db.close()


@app.route('/admin/aeropuertos/nuevo', methods=['GET', 'POST'])
@admin_required
def admin_crear_aeropuerto():
    if request.method == 'POST':
        db = Session()
        try:
            aeropuerto = Aeropuerto(
                nombre=request.form['nombre'],
                codigo_iata=request.form['codigo_iata'].upper().strip(),
                ciudad=request.form['ciudad'],
                pais=request.form['pais'],
                pasajeros_anuales=int(request.form.get('pasajeros_anuales', 0))
            )
            db.add(aeropuerto)
            db.commit()
            flash(f'Aeropuerto "{aeropuerto.codigo_iata}" creado', 'success')
            return redirect(url_for('admin_aeropuertos'))
        except Exception as e:
            db.rollback()
            flash(f'Error: {e}', 'danger')
        finally:
            db.close()
    return render_template('admin/aeropuerto_form.html', aeropuerto=None)


@app.route('/admin/aeropuertos/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def admin_editar_aeropuerto(id):
    db = Session()
    try:
        aeropuerto = db.query(Aeropuerto).get(id)
        if not aeropuerto:
            flash('Aeropuerto no encontrado', 'danger')
            return redirect(url_for('admin_aeropuertos'))

        if request.method == 'POST':
            aeropuerto.nombre = request.form['nombre']
            aeropuerto.codigo_iata = request.form['codigo_iata'].upper().strip()
            aeropuerto.ciudad = request.form['ciudad']
            aeropuerto.pais = request.form['pais']
            aeropuerto.pasajeros_anuales = int(request.form.get('pasajeros_anuales', 0))
            aeropuerto.activo = 'activo' in request.form
            db.commit()
            flash('Aeropuerto actualizado', 'success')
            return redirect(url_for('admin_aeropuertos'))

        return render_template('admin/aeropuerto_form.html', aeropuerto=aeropuerto)
    finally:
        db.close()


@app.route('/admin/aeropuertos/<int:id>/eliminar', methods=['POST'])
@admin_required
def admin_eliminar_aeropuerto(id):
    db = Session()
    try:
        aeropuerto = db.query(Aeropuerto).get(id)
        if aeropuerto:
            db.delete(aeropuerto)
            db.commit()
            flash('Aeropuerto eliminado', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('admin_aeropuertos'))


# --- Admin: Espacios ---

@app.route('/admin/espacios')
@admin_required
def admin_espacios():
    db = Session()
    try:
        espacios = db.query(EspacioPublicitario).order_by(EspacioPublicitario.nombre).all()
        return render_template('admin/espacios.html', espacios=espacios)
    finally:
        db.close()


@app.route('/admin/espacios/nuevo', methods=['GET', 'POST'])
@admin_required
def admin_crear_espacio():
    db = Session()
    try:
        aeropuertos = db.query(Aeropuerto).filter(Aeropuerto.activo == True).all()
        if request.method == 'POST':
            espacio = EspacioPublicitario(
                aeropuerto_id=int(request.form['aeropuerto_id']),
                nombre=request.form['nombre'],
                ubicacion=request.form['ubicacion'],
                tipo=request.form['tipo'],
                dimensiones=request.form.get('dimensiones', ''),
                precio_mensual=float(request.form['precio_mensual']),
                descripcion=request.form.get('descripcion', '')
            )
            db.add(espacio)
            db.commit()
            flash(f'Espacio "{espacio.nombre}" creado', 'success')
            return redirect(url_for('admin_espacios'))
        return render_template('admin/espacio_form.html', espacio=None, aeropuertos=aeropuertos)
    finally:
        db.close()


@app.route('/admin/espacios/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def admin_editar_espacio(id):
    db = Session()
    try:
        espacio = db.query(EspacioPublicitario).get(id)
        aeropuertos = db.query(Aeropuerto).filter(Aeropuerto.activo == True).all()
        if not espacio:
            flash('Espacio no encontrado', 'danger')
            return redirect(url_for('admin_espacios'))

        if request.method == 'POST':
            espacio.nombre = request.form['nombre']
            espacio.aeropuerto_id = int(request.form['aeropuerto_id'])
            espacio.ubicacion = request.form['ubicacion']
            espacio.tipo = request.form['tipo']
            espacio.dimensiones = request.form.get('dimensiones', '')
            espacio.precio_mensual = float(request.form['precio_mensual'])
            espacio.descripcion = request.form.get('descripcion', '')
            espacio.disponible = 'disponible' in request.form
            db.commit()
            flash('Espacio actualizado', 'success')
            return redirect(url_for('admin_espacios'))

        return render_template('admin/espacio_form.html', espacio=espacio, aeropuertos=aeropuertos)
    finally:
        db.close()


@app.route('/admin/espacios/<int:id>/eliminar', methods=['POST'])
@admin_required
def admin_eliminar_espacio(id):
    db = Session()
    try:
        espacio = db.query(EspacioPublicitario).get(id)
        if espacio:
            db.delete(espacio)
            db.commit()
            flash('Espacio eliminado', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('admin_espacios'))


# --- Admin: Campanas y Contratos ---

@app.route('/admin/campanas')
@admin_required
def admin_campanas():
    db = Session()
    try:
        campanas = db.query(Campana).order_by(Campana.fecha_creacion.desc()).all()
        return render_template('admin/campanas.html', campanas=campanas)
    finally:
        db.close()


@app.route('/admin/contratos')
@admin_required
def admin_contratos():
    db = Session()
    try:
        contratos = db.query(Contrato).order_by(Contrato.fecha_creacion.desc()).all()
        return render_template('admin/contratos.html', contratos=contratos)
    finally:
        db.close()


@app.route('/admin/contratos/<int:id>/estado', methods=['POST'])
@admin_required
def admin_cambiar_estado_contrato(id):
    db = Session()
    try:
        contrato = db.query(Contrato).get(id)
        if not contrato:
            flash('Contrato no encontrado', 'danger')
            return redirect(url_for('admin_contratos'))

        nuevo_estado = request.form.get('estado')
        if nuevo_estado in ['pendiente', 'activo', 'vencido', 'cancelado']:
            contrato.estado = nuevo_estado
            db.commit()
            flash(f'Contrato #{contrato.id} actualizado a "{nuevo_estado}"', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('admin_contratos'))


# ============================================================================
# ERRORES
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
    print("SEMANA 10 - PROYECTO 3: PUBLICIDAD EN AEROPUERTOS")
    print("=" * 70)

    crear_tablas()
    crear_datos_ejemplo()

    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║              SISTEMA DE PUBLICIDAD EN AEROPUERTOS                   ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║  URL: http://localhost:5012                                         ║
║                                                                     ║
║  RUTAS CLIENTE:                                                     ║
║  /                  → Dashboard                                     ║
║  /aeropuertos       → Directorio de aeropuertos                     ║
║  /espacios          → Espacios publicitarios disponibles            ║
║  /campanas          → Mis campanas                                  ║
║  /contratar/<id>    → Contratar un espacio                          ║
║                                                                     ║
║  ADMIN:                                                             ║
║  /admin             → Dashboard admin                               ║
║  /admin/aeropuertos → Gestionar aeropuertos                         ║
║  /admin/espacios    → Gestionar espacios                            ║
║  /admin/campanas    → Ver campanas                                  ║
║  /admin/contratos   → Gestionar contratos                           ║
║                                                                     ║
║  ADMIN:   admin@ejemplo.com / admin123                              ║
║  CLIENTE: cliente@ejemplo.com / cliente123                          ║
╚═══════════════════════════════════════════════════════════════════════╝
    """)

    app.run(debug=True, port=5012)
