# ============================================================================
# SEMANA 10 - PROYECTO 2: SISTEMA DE CITAS PARA CLIENTES
# ============================================================================
# Plataforma de agendamiento de citas que integra:
#
# - Modelos SQLAlchemy con relaciones (Semanas 6-7)
# - CRUD completo (Semana 8)
# - Autenticacion con sesiones y roles (Semana 9)
# - Gestion de servicios, profesionales y horarios
# - Agendamiento y seguimiento de citas
#
# COMO EJECUTAR:
# 1. pip install flask sqlalchemy psycopg2-binary werkzeug
# 2. python app.py
# 3. Abre: http://localhost:5011
#
# CREDENCIALES:
# - Admin: admin@ejemplo.com / admin123
# ============================================================================

from flask import Flask, render_template, request, redirect, url_for, flash, session
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, scoped_session, joinedload
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, date, timedelta
import os

# ============================================================================
# CONFIGURACION
# ============================================================================

app = Flask(__name__)
app.secret_key = 'citas-secreto-cambiar-en-produccion'

DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://neondb_owner:npg_xnKz5VIdoiv7@ep-hidden-voice-ahdtczjv-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require'
)

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
Base = declarative_base()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


# ============================================================================
# MODELOS
# ============================================================================
# Prefijo "citas_" en tablas para evitar conflictos con otros proyectos.
# ============================================================================

class Usuario(Base):
    """Usuarios del sistema: admin o cliente."""
    __tablename__ = 'citas_usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)
    telefono = Column(String(20))
    rol = Column(String(20), default='cliente')  # admin / cliente
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    citas = relationship("Cita", back_populates="cliente")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def es_admin(self):
        return self.rol == 'admin'


# ----------------------------------------------------------------------------
# MODELO: Servicio
# ----------------------------------------------------------------------------
# Representa un servicio que se ofrece (ej: "Consulta General", "Corte").
# Tiene duracion en minutos y precio.
# ----------------------------------------------------------------------------

class Servicio(Base):
    __tablename__ = 'citas_servicios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    duracion_minutos = Column(Integer, nullable=False, default=30)
    precio = Column(Float, nullable=False, default=0)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    citas = relationship("Cita", back_populates="servicio")

    @property
    def precio_formateado(self):
        return f"${self.precio:,.2f}"

    @property
    def duracion_formateada(self):
        if self.duracion_minutos >= 60:
            horas = self.duracion_minutos // 60
            mins = self.duracion_minutos % 60
            return f"{horas}h {mins}min" if mins else f"{horas}h"
        return f"{self.duracion_minutos} min"


# ----------------------------------------------------------------------------
# MODELO: Profesional
# ----------------------------------------------------------------------------
# Persona que atiende las citas. Tiene una especialidad.
# Puede tener multiples horarios y citas asignadas.
# ----------------------------------------------------------------------------

class Profesional(Base):
    __tablename__ = 'citas_profesionales'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    especialidad = Column(String(100))
    email = Column(String(200))
    telefono = Column(String(20))
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    horarios = relationship("HorarioDisponible", back_populates="profesional", cascade="all, delete-orphan")
    citas = relationship("Cita", back_populates="profesional")


# ----------------------------------------------------------------------------
# MODELO: HorarioDisponible
# ----------------------------------------------------------------------------
# Define cuando un profesional esta disponible.
# dia_semana: 0=Lunes, 1=Martes, ..., 6=Domingo
# hora_inicio/hora_fin: formato "09:00", "17:00"
# ----------------------------------------------------------------------------

class HorarioDisponible(Base):
    __tablename__ = 'citas_horarios'

    id = Column(Integer, primary_key=True)
    profesional_id = Column(Integer, ForeignKey('citas_profesionales.id'))
    dia_semana = Column(Integer, nullable=False)  # 0=Lun ... 6=Dom
    hora_inicio = Column(String(5), nullable=False, default='09:00')
    hora_fin = Column(String(5), nullable=False, default='17:00')
    activo = Column(Boolean, default=True)

    profesional = relationship("Profesional", back_populates="horarios")

    @property
    def dia_nombre(self):
        dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        return dias[self.dia_semana] if 0 <= self.dia_semana <= 6 else '?'


# ----------------------------------------------------------------------------
# MODELO: Cita
# ----------------------------------------------------------------------------
# Una cita vincula: cliente + profesional + servicio + fecha/hora.
# Estados:
# - pendiente: recien creada, esperando confirmacion
# - confirmada: el admin/profesional la confirmo
# - completada: la cita ya se realizo
# - cancelada: el cliente o admin la cancelo
# ----------------------------------------------------------------------------

class Cita(Base):
    __tablename__ = 'citas_citas'

    id = Column(Integer, primary_key=True)
    cliente_id = Column(Integer, ForeignKey('citas_usuarios.id'))
    profesional_id = Column(Integer, ForeignKey('citas_profesionales.id'))
    servicio_id = Column(Integer, ForeignKey('citas_servicios.id'))
    fecha = Column(Date, nullable=False)
    hora = Column(String(5), nullable=False)
    estado = Column(String(20), default='pendiente')
    notas = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    cliente = relationship("Usuario", back_populates="citas")
    profesional = relationship("Profesional", back_populates="citas")
    servicio = relationship("Servicio", back_populates="citas")

    @property
    def estado_color(self):
        colores = {
            'pendiente': 'warning',
            'confirmada': 'info',
            'completada': 'success',
            'cancelada': 'danger'
        }
        return colores.get(self.estado, 'secondary')

    @property
    def es_futura(self):
        return self.fecha >= date.today()


# ============================================================================
# CREAR TABLAS Y DATOS DE EJEMPLO
# ============================================================================

def crear_tablas():
    Base.metadata.create_all(engine)
    print("[OK] Tablas del Sistema de Citas creadas/verificadas")


def crear_datos_ejemplo():
    db = Session()
    try:
        if db.query(Usuario).filter(Usuario.email == 'admin@ejemplo.com').first():
            print("[OK] Datos ya existen")
            return

        # Admin
        admin = Usuario(nombre='Administrador', email='admin@ejemplo.com', rol='admin')
        admin.set_password('admin123')
        db.add(admin)

        # Cliente de ejemplo (contexto Panama)
        cliente = Usuario(nombre='Maria Garcia', email='maria@ejemplo.com', telefono='6700-1234', rol='cliente')
        cliente.set_password('cliente123')
        db.add(cliente)

        # Servicios (precios en USD/Balboas - moneda de Panama)
        servicios = [
            Servicio(nombre='Consulta General', descripcion='Consulta medica general con revision completa. Incluye diagnostico y recomendaciones.', duracion_minutos=30, precio=35.00),
            Servicio(nombre='Limpieza Dental', descripcion='Limpieza dental profesional con ultrasonido. Incluye pulido y fluoruro.', duracion_minutos=45, precio=55.00),
            Servicio(nombre='Corte de Cabello', descripcion='Corte de cabello personalizado con lavado y secado incluido.', duracion_minutos=40, precio=15.00),
            Servicio(nombre='Masaje Relajante', descripcion='Masaje terapeutico de cuerpo completo. Reduce estres y tension muscular.', duracion_minutos=60, precio=65.00),
            Servicio(nombre='Consulta Nutricional', descripcion='Evaluacion nutricional personalizada con plan de alimentacion.', duracion_minutos=45, precio=45.00),
        ]
        for s in servicios:
            db.add(s)

        # Profesionales
        profesionales = [
            Profesional(nombre='Dr. Carlos Mendez', especialidad='Medicina General', email='carlos@clinica.com', telefono='6600-0001'),
            Profesional(nombre='Dra. Ana Rodriguez', especialidad='Odontologia', email='ana@clinica.com', telefono='6600-0002'),
            Profesional(nombre='Luis Fernandez', especialidad='Estilismo', email='luis@salon.com', telefono='6600-0003'),
            Profesional(nombre='Sofia Martinez', especialidad='Terapia y Masajes', email='sofia@spa.com', telefono='6600-0004'),
        ]
        for p in profesionales:
            db.add(p)
        db.flush()

        # Horarios (Lunes a Viernes, 9:00-17:00 para todos)
        for prof in profesionales:
            for dia in range(5):  # 0=Lun a 4=Vie
                horario = HorarioDisponible(
                    profesional_id=prof.id,
                    dia_semana=dia,
                    hora_inicio='09:00',
                    hora_fin='17:00'
                )
                db.add(horario)

        db.commit()
        print("[OK] Datos de ejemplo creados (admin + cliente + 5 servicios + 4 profesionales)")
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


# ============================================================================
# CONTEXTO GLOBAL
# ============================================================================

@app.context_processor
def inject_user():
    datos = {
        'usuario_actual': None,
        'esta_logueado': False,
        'es_admin': False,
    }
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
        telefono = request.form.get('telefono', '').strip()
        password = request.form.get('password', '')
        confirmar = request.form.get('confirmar_password', '')

        errores = []
        if not nombre: errores.append('El nombre es obligatorio')
        if not email: errores.append('El email es obligatorio')
        if len(password) < 6: errores.append('La contrasena debe tener al menos 6 caracteres')
        if password != confirmar: errores.append('Las contrasenas no coinciden')

        if errores:
            for e in errores: flash(e, 'danger')
            return render_template('auth/registro.html', nombre=nombre, email=email, telefono=telefono)

        db = Session()
        try:
            if db.query(Usuario).filter(Usuario.email == email).first():
                flash('Ya existe una cuenta con ese email', 'danger')
                return render_template('auth/registro.html', nombre=nombre, email=email, telefono=telefono)

            usuario = Usuario(nombre=nombre, email=email, telefono=telefono)
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
# PAGINA PRINCIPAL
# ============================================================================

@app.route('/')
@login_required
def index():
    """Dashboard del cliente: proximas citas y acciones rapidas."""
    db = Session()
    try:
        hoy = date.today()
        proximas_citas = db.query(Cita).filter(
            Cita.cliente_id == session['usuario_id'],
            Cita.fecha >= hoy,
            Cita.estado.in_(['pendiente', 'confirmada'])
        ).order_by(Cita.fecha, Cita.hora).limit(5).all()

        total_citas = db.query(Cita).filter(Cita.cliente_id == session['usuario_id']).count()
        citas_pendientes = db.query(Cita).filter(
            Cita.cliente_id == session['usuario_id'],
            Cita.estado == 'pendiente'
        ).count()

        return render_template('index.html',
                               proximas_citas=proximas_citas,
                               total_citas=total_citas,
                               citas_pendientes=citas_pendientes)
    finally:
        db.close()


# ============================================================================
# SERVICIOS (vista cliente)
# ============================================================================

@app.route('/servicios')
@login_required
def listar_servicios():
    db = Session()
    try:
        servicios = db.query(Servicio).filter(Servicio.activo == True).order_by(Servicio.nombre).all()
        return render_template('servicios/lista.html', servicios=servicios)
    finally:
        db.close()


@app.route('/servicios/<int:id>')
@login_required
def ver_servicio(id):
    db = Session()
    try:
        servicio = db.query(Servicio).get(id)
        if not servicio:
            flash('Servicio no encontrado', 'danger')
            return redirect(url_for('listar_servicios'))
        return render_template('servicios/detalle.html', servicio=servicio)
    finally:
        db.close()


# ============================================================================
# AGENDAR CITA
# ============================================================================
# Flujo de agendamiento:
# 1. GET /agendar → Muestra formulario con servicios, profesionales y fecha
# 2. POST /agendar → Valida y crea la cita
#
# VALIDACIONES:
# - El servicio y profesional deben existir y estar activos
# - La fecha no puede ser pasada
# - No se puede agendar si ya hay una cita en esa hora
# ============================================================================

@app.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar_cita():
    db = Session()
    try:
        servicios = db.query(Servicio).filter(Servicio.activo == True).all()
        profesionales = db.query(Profesional).filter(Profesional.activo == True).all()

        # Generar horarios disponibles (cada 30 min de 9 a 17)
        horas_disponibles = []
        for h in range(9, 17):
            horas_disponibles.append(f"{h:02d}:00")
            horas_disponibles.append(f"{h:02d}:30")

        if request.method == 'POST':
            servicio_id = request.form.get('servicio_id', type=int)
            profesional_id = request.form.get('profesional_id', type=int)
            fecha_str = request.form.get('fecha', '')
            hora = request.form.get('hora', '')
            notas = request.form.get('notas', '').strip()

            errores = []
            if not servicio_id: errores.append('Selecciona un servicio')
            if not profesional_id: errores.append('Selecciona un profesional')
            if not fecha_str: errores.append('Selecciona una fecha')
            if not hora: errores.append('Selecciona una hora')

            if errores:
                for e in errores: flash(e, 'danger')
                return render_template('citas/agendar.html',
                                       servicios=servicios, profesionales=profesionales,
                                       horas_disponibles=horas_disponibles)

            try:
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de fecha invalido', 'danger')
                return render_template('citas/agendar.html',
                                       servicios=servicios, profesionales=profesionales,
                                       horas_disponibles=horas_disponibles)

            if fecha < date.today():
                flash('No puedes agendar en una fecha pasada', 'danger')
                return render_template('citas/agendar.html',
                                       servicios=servicios, profesionales=profesionales,
                                       horas_disponibles=horas_disponibles)

            # Verificar que no haya conflicto de horario
            conflicto = db.query(Cita).filter(
                Cita.profesional_id == profesional_id,
                Cita.fecha == fecha,
                Cita.hora == hora,
                Cita.estado.in_(['pendiente', 'confirmada'])
            ).first()

            if conflicto:
                flash('Ese horario ya esta ocupado. Elige otra hora.', 'warning')
                return render_template('citas/agendar.html',
                                       servicios=servicios, profesionales=profesionales,
                                       horas_disponibles=horas_disponibles)

            cita = Cita(
                cliente_id=session['usuario_id'],
                servicio_id=servicio_id,
                profesional_id=profesional_id,
                fecha=fecha,
                hora=hora,
                notas=notas
            )
            db.add(cita)
            db.commit()
            flash('Cita agendada exitosamente!', 'success')
            return redirect(url_for('mis_citas'))

        return render_template('citas/agendar.html',
                               servicios=servicios,
                               profesionales=profesionales,
                               horas_disponibles=horas_disponibles)
    finally:
        db.close()


# ============================================================================
# MIS CITAS
# ============================================================================

@app.route('/mis-citas')
@login_required
def mis_citas():
    db = Session()
    try:
        filtro = request.args.get('filtro', 'todas')
        query = db.query(Cita).options(
            joinedload(Cita.servicio),
            joinedload(Cita.profesional)
        ).filter(Cita.cliente_id == session['usuario_id'])

        if filtro == 'proximas':
            query = query.filter(Cita.fecha >= date.today(), Cita.estado.in_(['pendiente', 'confirmada']))
        elif filtro == 'pasadas':
            query = query.filter(Cita.fecha < date.today())
        elif filtro == 'canceladas':
            query = query.filter(Cita.estado == 'cancelada')

        citas = query.order_by(Cita.fecha.desc(), Cita.hora.desc()).all()
        return render_template('citas/mis_citas.html', citas=citas, filtro=filtro)
    finally:
        db.close()


@app.route('/mis-citas/<int:id>')
@login_required
def ver_cita(id):
    db = Session()
    try:
        cita = db.query(Cita).options(
            joinedload(Cita.servicio),
            joinedload(Cita.profesional),
            joinedload(Cita.cliente)
        ).get(id)
        if not cita or cita.cliente_id != session['usuario_id']:
            flash('Cita no encontrada', 'danger')
            return redirect(url_for('mis_citas'))
        return render_template('citas/detalle.html', cita=cita)
    finally:
        db.close()


@app.route('/mis-citas/<int:id>/cancelar', methods=['POST'])
@login_required
def cancelar_cita(id):
    """
    Cancelar una cita.
    Solo se puede cancelar si esta pendiente o confirmada.
    No se puede cancelar una cita que ya se completo.
    """
    db = Session()
    try:
        cita = db.query(Cita).get(id)
        if not cita or cita.cliente_id != session['usuario_id']:
            flash('Cita no encontrada', 'danger')
            return redirect(url_for('mis_citas'))

        if cita.estado in ['completada', 'cancelada']:
            flash('Esta cita no se puede cancelar', 'warning')
            return redirect(url_for('ver_cita', id=id))

        cita.estado = 'cancelada'
        db.commit()
        flash('Cita cancelada', 'info')
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('mis_citas'))


# ============================================================================
# ADMINISTRACION
# ============================================================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    db = Session()
    try:
        hoy = date.today()
        stats = {
            'total_citas': db.query(Cita).count(),
            'citas_hoy': db.query(Cita).filter(Cita.fecha == hoy, Cita.estado.in_(['pendiente', 'confirmada'])).count(),
            'total_servicios': db.query(Servicio).count(),
            'total_profesionales': db.query(Profesional).count(),
            'citas_pendientes': db.query(Cita).filter(Cita.estado == 'pendiente').count(),
        }

        citas_hoy = db.query(Cita).filter(
            Cita.fecha == hoy,
            Cita.estado.in_(['pendiente', 'confirmada'])
        ).order_by(Cita.hora).all()

        citas_recientes = db.query(Cita).order_by(Cita.fecha_creacion.desc()).limit(5).all()

        return render_template('admin/dashboard.html',
                               stats=stats,
                               citas_hoy=citas_hoy,
                               citas_recientes=citas_recientes)
    finally:
        db.close()


# --- Admin: Servicios ---

@app.route('/admin/servicios')
@admin_required
def admin_servicios():
    db = Session()
    try:
        servicios = db.query(Servicio).order_by(Servicio.nombre).all()
        return render_template('admin/servicios.html', servicios=servicios)
    finally:
        db.close()


@app.route('/admin/servicios/nuevo', methods=['GET', 'POST'])
@admin_required
def admin_crear_servicio():
    if request.method == 'POST':
        db = Session()
        try:
            servicio = Servicio(
                nombre=request.form['nombre'],
                descripcion=request.form.get('descripcion', ''),
                duracion_minutos=int(request.form.get('duracion_minutos', 30)),
                precio=float(request.form.get('precio', 0))
            )
            db.add(servicio)
            db.commit()
            flash(f'Servicio "{servicio.nombre}" creado', 'success')
            return redirect(url_for('admin_servicios'))
        except Exception as e:
            db.rollback()
            flash(f'Error: {e}', 'danger')
        finally:
            db.close()
    return render_template('admin/servicio_form.html', servicio=None)


@app.route('/admin/servicios/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def admin_editar_servicio(id):
    db = Session()
    try:
        servicio = db.query(Servicio).get(id)
        if not servicio:
            flash('Servicio no encontrado', 'danger')
            return redirect(url_for('admin_servicios'))

        if request.method == 'POST':
            servicio.nombre = request.form['nombre']
            servicio.descripcion = request.form.get('descripcion', '')
            servicio.duracion_minutos = int(request.form.get('duracion_minutos', 30))
            servicio.precio = float(request.form.get('precio', 0))
            servicio.activo = 'activo' in request.form
            db.commit()
            flash(f'Servicio actualizado', 'success')
            return redirect(url_for('admin_servicios'))

        return render_template('admin/servicio_form.html', servicio=servicio)
    finally:
        db.close()


@app.route('/admin/servicios/<int:id>/eliminar', methods=['POST'])
@admin_required
def admin_eliminar_servicio(id):
    db = Session()
    try:
        servicio = db.query(Servicio).get(id)
        if servicio:
            db.delete(servicio)
            db.commit()
            flash('Servicio eliminado', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('admin_servicios'))


# --- Admin: Profesionales ---

@app.route('/admin/profesionales')
@admin_required
def admin_profesionales():
    db = Session()
    try:
        profesionales = db.query(Profesional).order_by(Profesional.nombre).all()
        return render_template('admin/profesionales.html', profesionales=profesionales)
    finally:
        db.close()


@app.route('/admin/profesionales/nuevo', methods=['GET', 'POST'])
@admin_required
def admin_crear_profesional():
    if request.method == 'POST':
        db = Session()
        try:
            prof = Profesional(
                nombre=request.form['nombre'],
                especialidad=request.form.get('especialidad', ''),
                email=request.form.get('email', ''),
                telefono=request.form.get('telefono', '')
            )
            db.add(prof)
            db.commit()
            flash(f'Profesional "{prof.nombre}" creado', 'success')
            return redirect(url_for('admin_profesionales'))
        except Exception as e:
            db.rollback()
            flash(f'Error: {e}', 'danger')
        finally:
            db.close()
    return render_template('admin/profesional_form.html', profesional=None)


@app.route('/admin/profesionales/<int:id>/editar', methods=['GET', 'POST'])
@admin_required
def admin_editar_profesional(id):
    db = Session()
    try:
        prof = db.query(Profesional).get(id)
        if not prof:
            flash('Profesional no encontrado', 'danger')
            return redirect(url_for('admin_profesionales'))

        if request.method == 'POST':
            prof.nombre = request.form['nombre']
            prof.especialidad = request.form.get('especialidad', '')
            prof.email = request.form.get('email', '')
            prof.telefono = request.form.get('telefono', '')
            prof.activo = 'activo' in request.form
            db.commit()
            flash('Profesional actualizado', 'success')
            return redirect(url_for('admin_profesionales'))

        return render_template('admin/profesional_form.html', profesional=prof)
    finally:
        db.close()


@app.route('/admin/profesionales/<int:id>/eliminar', methods=['POST'])
@admin_required
def admin_eliminar_profesional(id):
    db = Session()
    try:
        prof = db.query(Profesional).get(id)
        if prof:
            db.delete(prof)
            db.commit()
            flash('Profesional eliminado', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('admin_profesionales'))


# --- Admin: Citas ---

@app.route('/admin/citas')
@admin_required
def admin_citas():
    db = Session()
    try:
        citas = db.query(Cita).order_by(Cita.fecha.desc(), Cita.hora.desc()).all()
        return render_template('admin/citas.html', citas=citas)
    finally:
        db.close()


@app.route('/admin/citas/<int:id>/estado', methods=['POST'])
@admin_required
def admin_cambiar_estado_cita(id):
    db = Session()
    try:
        cita = db.query(Cita).get(id)
        if not cita:
            flash('Cita no encontrada', 'danger')
            return redirect(url_for('admin_citas'))

        nuevo_estado = request.form.get('estado')
        if nuevo_estado in ['pendiente', 'confirmada', 'completada', 'cancelada']:
            cita.estado = nuevo_estado
            db.commit()
            flash(f'Cita #{cita.id} actualizada a "{nuevo_estado}"', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        db.close()
    return redirect(url_for('admin_citas'))


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
    print("SEMANA 10 - PROYECTO 2: SISTEMA DE CITAS")
    print("=" * 70)

    crear_tablas()
    crear_datos_ejemplo()

    print("""
╔═══════════════════════════════════════════════════════════════════════╗
║                     SISTEMA DE CITAS                                ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                     ║
║  URL: http://localhost:5011                                         ║
║                                                                     ║
║  RUTAS CLIENTE:                                                     ║
║  /                  → Dashboard (proximas citas)                    ║
║  /servicios         → Ver servicios disponibles                     ║
║  /agendar           → Agendar una nueva cita                        ║
║  /mis-citas         → Ver mis citas                                 ║
║                                                                     ║
║  ADMIN:                                                             ║
║  /admin             → Dashboard admin                               ║
║  /admin/servicios   → Gestionar servicios                           ║
║  /admin/profesionales → Gestionar profesionales                     ║
║  /admin/citas       → Gestionar todas las citas                     ║
║                                                                     ║
║  CREDENCIALES: admin@ejemplo.com / admin123                         ║
║  CLIENTE:      maria@ejemplo.com / cliente123                       ║
╚═══════════════════════════════════════════════════════════════════════╝
    """)

    app.run(debug=True, port=5011)
