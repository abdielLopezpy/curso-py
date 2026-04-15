# ============================================================================
# SEMANA 11 - PROYECTO: DASHBOARD DE ANALISIS DE VENTAS
# ============================================================================
# Aplicacion web que analiza datos de ventas usando pandas, genera graficos
# con matplotlib y ofrece predicciones con regresion lineal.
#
# Conceptos aplicados:
# - pandas: DataFrames, groupby, pivot_table, describe, filtros
# - numpy: arrays, calculos numericos eficientes
# - matplotlib: graficos de barras, lineas, pastel
# - scipy: regresion lineal para prediccion
# - Flask + SQLAlchemy: backend web con base de datos
# - Autenticacion con sesiones y roles (Semana 9)
#
# COMO EJECUTAR:
# 1. pip install flask sqlalchemy werkzeug pandas numpy matplotlib scipy
# 2. python app.py
# 3. Abre: http://localhost:5013
#
# CREDENCIALES:
# - Admin: admin@ejemplo.com / admin123
# ============================================================================

import os
import json
import random
from datetime import datetime, timedelta
from functools import wraps
from io import BytesIO

# ============================================================================
# IMPORTS DE CIENCIA DE DATOS
# ============================================================================
# pandas  → Manipulacion de datos tabulares (DataFrames)
# numpy   → Calculos numericos eficientes (arrays, operaciones matematicas)
# matplotlib → Generacion de graficos (barras, lineas, pastel, etc.)
# scipy   → Funciones estadisticas avanzadas (regresion lineal)
# ============================================================================

import numpy as np
import pandas as pd

# matplotlib.use('Agg') DEBE llamarse ANTES de importar pyplot.
# 'Agg' es un backend que renderiza graficos a archivos/memoria sin necesitar
# una ventana grafica (GUI). Esto es OBLIGATORIO en servidores web.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from scipy.stats import linregress

from flask import (
    Flask, render_template, request, redirect, url_for,
    flash, session, Response, make_response
)
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================================
# CONFIGURACION DE LA APLICACION
# ============================================================================

app = Flask(__name__)
app.secret_key = 'analisis-ventas-secreto-cambiar-en-produccion'

# ============================================================================
# BASE DE DATOS - SQLite
# ============================================================================
# Usamos SQLite para simplicidad. El archivo se crea automaticamente.
# ============================================================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'ventas.db')
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


# ============================================================================
# MODELOS DE LA BASE DE DATOS
# ============================================================================

class Usuario(Base):
    """Modelo de usuario para autenticacion."""
    __tablename__ = 'ds_usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    rol = Column(String(20), default='usuario')  # 'admin' o 'usuario'
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    @property
    def es_admin(self):
        return self.rol == 'admin'


class Venta(Base):
    """
    Modelo de venta.
    Cada registro representa una transaccion de venta con producto,
    categoria, cantidad, precio y datos geograficos.
    """
    __tablename__ = 'ds_ventas'

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, nullable=False)
    producto = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    region = Column(String(50), nullable=False)
    cliente = Column(String(100), nullable=False)

    @property
    def fecha_formato(self):
        return self.fecha.strftime('%d/%m/%Y')

    @property
    def total_formato(self):
        return f'${self.total:,.2f}'


class Reporte(Base):
    """Modelo para reportes generados y guardados."""
    __tablename__ = 'ds_reportes'

    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    fecha_generacion = Column(DateTime, default=datetime.utcnow)
    tipo = Column(String(50), nullable=False)  # 'general', 'categoria', 'region', 'prediccion'
    parametros_json = Column(Text, default='{}')
    ruta_archivo = Column(String(300), default='')

    @property
    def fecha_formato(self):
        return self.fecha_generacion.strftime('%d/%m/%Y %H:%M')

    @property
    def parametros(self):
        try:
            return json.loads(self.parametros_json)
        except Exception:
            return {}


# Crear todas las tablas
Base.metadata.create_all(engine)


# ============================================================================
# GENERACION DE DATOS DE EJEMPLO
# ============================================================================
# Generamos 500+ registros de ventas realistas para tener datos suficientes
# para analisis estadistico significativo.
#
# random.seed(42) asegura que los datos generados sean siempre los mismos
# (reproducibilidad), lo cual es importante para depuracion y pruebas.
# ============================================================================

def generar_datos_ejemplo():
    """Genera datos de ejemplo: usuario admin + 500 ventas realistas."""
    db = Session()

    # Verificar si ya hay datos
    if db.query(Venta).count() > 0:
        db.close()
        return

    # --- Crear usuario admin ---
    admin = db.query(Usuario).filter_by(email='admin@ejemplo.com').first()
    if not admin:
        admin = Usuario(
            nombre='Administrador',
            email='admin@ejemplo.com',
            password_hash=generate_password_hash('admin123'),
            rol='admin'
        )
        db.add(admin)

    # --- Catalogo de productos por categoria ---
    # Cada categoria tiene productos con rangos de precio realistas
    catalogo = {
        'Electronica': [
            ('Laptop HP', 800, 1500),
            ('Mouse Inalambrico', 15, 45),
            ('Teclado Mecanico', 50, 150),
            ('Monitor 24"', 200, 500),
            ('Audifonos Bluetooth', 25, 120),
            ('Tablet Samsung', 250, 600),
            ('Cargador USB-C', 10, 30),
            ('Webcam HD', 30, 80),
        ],
        'Ropa': [
            ('Camiseta Basica', 10, 30),
            ('Jeans Slim', 35, 80),
            ('Chaqueta Deportiva', 45, 120),
            ('Zapatillas Running', 50, 150),
            ('Gorra Ajustable', 8, 25),
            ('Sudadera Con Capucha', 30, 70),
        ],
        'Alimentos': [
            ('Cafe Premium 500g', 8, 20),
            ('Aceite de Oliva 1L', 6, 15),
            ('Chocolate Artesanal', 5, 18),
            ('Te Verde Organico', 4, 12),
            ('Miel Natural 500g', 7, 16),
            ('Frutos Secos Mix', 6, 14),
        ],
        'Hogar': [
            ('Lampara LED', 15, 60),
            ('Juego de Sabanas', 25, 80),
            ('Organizador Escritorio', 12, 35),
            ('Cafetera Electrica', 30, 90),
            ('Set de Toallas', 18, 50),
            ('Reloj de Pared', 10, 40),
        ],
        'Deportes': [
            ('Pelota de Futbol', 15, 50),
            ('Mancuernas 5kg', 20, 60),
            ('Colchoneta Yoga', 12, 40),
            ('Botella Deportiva', 8, 25),
            ('Banda Elastica Set', 10, 30),
            ('Guantes de Boxeo', 25, 70),
        ],
    }

    regiones = ['Norte', 'Sur', 'Centro', 'Este', 'Oeste']

    # Nombres de clientes ficticios
    nombres = [
        'Carlos Garcia', 'Maria Lopez', 'Juan Martinez', 'Ana Rodriguez',
        'Pedro Sanchez', 'Laura Fernandez', 'Diego Torres', 'Sofia Ramirez',
        'Andres Morales', 'Valentina Castro', 'Luis Herrera', 'Camila Diaz',
        'Ricardo Vargas', 'Isabella Flores', 'Fernando Mendoza', 'Gabriela Ruiz',
        'Miguel Ortega', 'Daniela Paredes', 'Alejandro Silva', 'Paula Navarro',
        'Roberto Reyes', 'Natalia Guerrero', 'Jorge Perez', 'Elena Romero',
        'David Jimenez', 'Carolina Molina', 'Santiago Acosta', 'Lucia Medina',
        'Oscar Cardenas', 'Mariana Soto',
    ]

    random.seed(42)  # Semilla para reproducibilidad

    # Fecha inicial: 1 de enero de 2024
    fecha_inicio = datetime(2024, 1, 1)
    # Fecha final: 31 de diciembre de 2025
    fecha_fin = datetime(2025, 12, 31)
    dias_total = (fecha_fin - fecha_inicio).days

    ventas = []
    for _ in range(550):
        # Seleccionar categoria y producto aleatorio
        categoria = random.choice(list(catalogo.keys()))
        producto_info = random.choice(catalogo[categoria])
        nombre_producto, precio_min, precio_max = producto_info

        # Generar precio y cantidad
        precio = round(random.uniform(precio_min, precio_max), 2)
        cantidad = random.randint(1, 10)
        total = round(precio * cantidad, 2)

        # Fecha aleatoria en el rango 2024-2025
        dias_offset = random.randint(0, dias_total)
        fecha = fecha_inicio + timedelta(days=dias_offset)

        # Region y cliente aleatorios
        region = random.choice(regiones)
        cliente = random.choice(nombres)

        venta = Venta(
            fecha=fecha,
            producto=nombre_producto,
            categoria=categoria,
            cantidad=cantidad,
            precio_unitario=precio,
            total=total,
            region=region,
            cliente=cliente,
        )
        ventas.append(venta)

    db.add_all(ventas)
    db.commit()
    db.close()
    print(f'[INFO] Se generaron {len(ventas)} registros de venta de ejemplo.')


# ============================================================================
# DECORADORES DE AUTENTICACION
# ============================================================================
# Estos decoradores protegen las rutas que requieren login o rol admin.
# Son los mismos que usamos en la Semana 9.
# ============================================================================

def login_requerido(f):
    """Decorador que exige que el usuario haya iniciado sesion."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesion para acceder a esta pagina.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper


def admin_requerido(f):
    """Decorador que exige que el usuario sea administrador."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Debes iniciar sesion.', 'warning')
            return redirect(url_for('login'))
        db = Session()
        usuario = db.query(Usuario).get(session['usuario_id'])
        db.close()
        if not usuario or not usuario.es_admin:
            flash('No tienes permisos de administrador.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return wrapper


# ============================================================================
# CONTEXT PROCESSOR
# ============================================================================
# Inyecta variables globales en TODOS los templates automaticamente.
# Asi no hay que pasarlas manualmente en cada render_template().
# ============================================================================

@app.context_processor
def variables_globales():
    """Variables disponibles en todos los templates."""
    usuario_actual = None
    esta_logueado = False
    es_admin = False

    if 'usuario_id' in session:
        db = Session()
        usuario_actual = db.query(Usuario).get(session['usuario_id'])
        db.close()
        if usuario_actual:
            esta_logueado = True
            es_admin = usuario_actual.es_admin

    return {
        'usuario_actual': usuario_actual,
        'esta_logueado': esta_logueado,
        'es_admin': es_admin,
    }


# ============================================================================
# FUNCIONES AUXILIARES DE CIENCIA DE DATOS
# ============================================================================
# Estas funciones convierten datos de SQLAlchemy a DataFrames de pandas
# y realizan los calculos estadisticos necesarios.
# ============================================================================

def obtener_dataframe(filtros=None):
    """
    Convierte todas las ventas de la base de datos a un DataFrame de pandas.

    Parametros:
        filtros (dict): Diccionario opcional con filtros:
            - fecha_inicio: str 'YYYY-MM-DD'
            - fecha_fin: str 'YYYY-MM-DD'
            - categoria: str
            - region: str

    Retorna:
        pd.DataFrame con columnas: fecha, producto, categoria, cantidad,
        precio_unitario, total, region, cliente
    """
    db = Session()
    query = db.query(Venta)

    if filtros:
        if filtros.get('fecha_inicio'):
            try:
                fi = datetime.strptime(filtros['fecha_inicio'], '%Y-%m-%d')
                query = query.filter(Venta.fecha >= fi)
            except ValueError:
                pass
        if filtros.get('fecha_fin'):
            try:
                ff = datetime.strptime(filtros['fecha_fin'], '%Y-%m-%d')
                ff = ff.replace(hour=23, minute=59, second=59)
                query = query.filter(Venta.fecha <= ff)
            except ValueError:
                pass
        if filtros.get('categoria'):
            query = query.filter(Venta.categoria == filtros['categoria'])
        if filtros.get('region'):
            query = query.filter(Venta.region == filtros['region'])

    ventas = query.all()
    db.close()

    if not ventas:
        return pd.DataFrame(columns=[
            'fecha', 'producto', 'categoria', 'cantidad',
            'precio_unitario', 'total', 'region', 'cliente'
        ])

    # Convertir lista de objetos SQLAlchemy a lista de diccionarios,
    # luego a DataFrame. Esta es la forma estandar de hacerlo.
    datos = [{
        'fecha': v.fecha,
        'producto': v.producto,
        'categoria': v.categoria,
        'cantidad': v.cantidad,
        'precio_unitario': v.precio_unitario,
        'total': v.total,
        'region': v.region,
        'cliente': v.cliente,
    } for v in ventas]

    df = pd.DataFrame(datos)
    df['fecha'] = pd.to_datetime(df['fecha'])
    return df


def calcular_kpis(df):
    """
    Calcula los KPIs (Key Performance Indicators) principales.

    Los KPIs son metricas clave que resumen el estado del negocio
    de un vistazo. Son esenciales en cualquier dashboard.

    Retorna un diccionario con:
    - total_ventas: Suma de todos los totales
    - num_transacciones: Cantidad de registros
    - ticket_promedio: Promedio de total por transaccion (media)
    - ticket_mediana: Mediana del total (menos afectada por extremos)
    - producto_top: Producto con mas ventas totales
    - categoria_top: Categoria con mas ventas totales
    - region_top: Region con mas ventas totales
    - cliente_top: Cliente que mas ha gastado
    """
    if df.empty:
        return {
            'total_ventas': 0, 'num_transacciones': 0,
            'ticket_promedio': 0, 'ticket_mediana': 0,
            'producto_top': 'N/A', 'categoria_top': 'N/A',
            'region_top': 'N/A', 'cliente_top': 'N/A',
        }

    return {
        'total_ventas': round(df['total'].sum(), 2),
        'num_transacciones': len(df),
        'ticket_promedio': round(df['total'].mean(), 2),
        'ticket_mediana': round(df['total'].median(), 2),
        'producto_top': df.groupby('producto')['total'].sum().idxmax(),
        'categoria_top': df.groupby('categoria')['total'].sum().idxmax(),
        'region_top': df.groupby('region')['total'].sum().idxmax(),
        'cliente_top': df.groupby('cliente')['total'].sum().idxmax(),
    }


def calcular_estadisticas(df):
    """
    Calcula estadisticas descriptivas completas.

    Incluye:
    - describe(): Resumen automatico (count, mean, std, min, 25%, 50%, 75%, max)
    - Correlacion entre cantidad y total
    - Desviacion estandar
    - Coeficiente de variacion
    """
    if df.empty:
        return {
            'descripcion': {},
            'correlacion_cantidad_total': 0,
            'desviacion_total': 0,
            'coeficiente_variacion': 0,
            'por_categoria': {},
            'por_region': {},
        }

    desc = df[['cantidad', 'precio_unitario', 'total']].describe().round(2)

    correlacion = df['cantidad'].corr(df['total'])

    por_cat = df.groupby('categoria')['total'].agg(['sum', 'mean', 'median', 'std', 'count']).round(2)
    por_reg = df.groupby('region')['total'].agg(['sum', 'mean', 'median', 'std', 'count']).round(2)

    return {
        'descripcion': desc.to_dict(),
        'correlacion_cantidad_total': round(correlacion, 4),
        'desviacion_total': round(df['total'].std(), 2),
        'coeficiente_variacion': round(df['total'].std() / df['total'].mean() * 100, 2) if df['total'].mean() != 0 else 0,
        'por_categoria': por_cat.to_dict('index'),
        'por_region': por_reg.to_dict('index'),
    }


def calcular_prediccion(df, meses_futuro=3):
    """
    Realiza regresion lineal simple para predecir ventas futuras.

    Regresion lineal: y = slope * x + intercept
    - slope (pendiente): cuanto cambian las ventas por cada unidad de tiempo
    - intercept (intercepto): valor base de las ventas
    - r_value: coeficiente de correlacion (-1 a 1)
    - r_value**2 (R²): coeficiente de determinacion (0 a 1)
      Indica que porcentaje de la variacion es explicada por el modelo

    Retorna:
    - datos historicos mensuales
    - predicciones para los proximos meses
    - metricas del modelo (R², pendiente, etc.)
    """
    if df.empty or len(df) < 3:
        return {
            'historico': [],
            'predicciones': [],
            'r_cuadrado': 0,
            'pendiente': 0,
            'intercepto': 0,
            'tendencia': 'sin datos',
        }

    # Agrupar ventas por mes
    df_temp = df.copy()
    df_temp['mes'] = df_temp['fecha'].dt.to_period('M')
    mensual = df_temp.groupby('mes')['total'].sum()

    if len(mensual) < 2:
        return {
            'historico': [],
            'predicciones': [],
            'r_cuadrado': 0,
            'pendiente': 0,
            'intercepto': 0,
            'tendencia': 'insuficientes datos',
        }

    # Preparar datos para regresion
    # x = numeros consecutivos (0, 1, 2, ..., n-1)
    # y = total de ventas por mes
    x = np.arange(len(mensual))
    y = mensual.values.astype(float)

    # scipy.stats.linregress() calcula la regresion lineal
    slope, intercept, r_value, p_value, std_err = linregress(x, y)

    # Datos historicos para el grafico
    historico = []
    for i, (periodo, valor) in enumerate(mensual.items()):
        historico.append({
            'mes': str(periodo),
            'real': round(valor, 2),
            'modelo': round(slope * i + intercept, 2),
        })

    # Predicciones futuras
    predicciones = []
    ultimo_periodo = mensual.index[-1]
    for j in range(1, meses_futuro + 1):
        idx = len(mensual) + j - 1
        valor_pred = slope * idx + intercept
        # Calcular el mes futuro
        mes_futuro = ultimo_periodo + j
        predicciones.append({
            'mes': str(mes_futuro),
            'prediccion': round(max(valor_pred, 0), 2),
        })

    # Determinar tendencia
    if slope > 50:
        tendencia = 'crecimiento fuerte'
    elif slope > 0:
        tendencia = 'crecimiento moderado'
    elif slope > -50:
        tendencia = 'estable / leve descenso'
    else:
        tendencia = 'descenso'

    return {
        'historico': historico,
        'predicciones': predicciones,
        'r_cuadrado': round(r_value ** 2, 4),
        'pendiente': round(slope, 2),
        'intercepto': round(intercept, 2),
        'tendencia': tendencia,
    }


# ============================================================================
# FUNCIONES DE GENERACION DE GRAFICOS
# ============================================================================
# Cada funcion genera un grafico con matplotlib y lo devuelve como bytes PNG.
#
# Patron comun:
# 1. Crear figura: fig, ax = plt.subplots()
# 2. Dibujar el grafico: ax.bar(), ax.plot(), ax.pie()
# 3. Configurar: titulo, etiquetas, colores
# 4. Guardar en memoria: fig.savefig(buf, format='png')
# 5. Cerrar la figura: plt.close(fig)  ← IMPORTANTE para liberar memoria
# 6. Retornar los bytes del PNG
# ============================================================================

# Paleta de colores consistente para todos los graficos
COLORES = ['#6366f1', '#8b5cf6', '#a78bfa', '#c4b5fd', '#ddd6fe',
           '#818cf8', '#6d28d9', '#7c3aed', '#5b21b6', '#4c1d95']


def generar_grafico_ventas_mensual(df):
    """Grafico de lineas: evolucion de ventas mensuales."""
    if df.empty:
        return _grafico_vacio('Sin datos de ventas mensuales')

    df_temp = df.copy()
    df_temp['mes'] = df_temp['fecha'].dt.to_period('M')
    mensual = df_temp.groupby('mes')['total'].sum()

    fig, ax = plt.subplots(figsize=(10, 5))

    x_labels = [str(p) for p in mensual.index]
    x_pos = range(len(x_labels))

    ax.plot(x_pos, mensual.values, color=COLORES[0], linewidth=2.5,
            marker='o', markersize=6, markerfacecolor='white',
            markeredgecolor=COLORES[0], markeredgewidth=2)
    ax.fill_between(x_pos, mensual.values, alpha=0.1, color=COLORES[0])

    ax.set_title('Ventas Mensuales', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Mes', fontsize=11)
    ax.set_ylabel('Total ($)', fontsize=11)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x_labels, rotation=45, ha='right', fontsize=8)
    ax.grid(axis='y', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.tight_layout()
    return _fig_a_bytes(fig)


def generar_grafico_por_categoria(df):
    """Grafico de barras: ventas totales por categoria."""
    if df.empty:
        return _grafico_vacio('Sin datos por categoria')

    por_cat = df.groupby('categoria')['total'].sum().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.barh(por_cat.index, por_cat.values, color=COLORES[:len(por_cat)],
                   edgecolor='white', linewidth=0.5)

    # Etiquetas de valor en cada barra
    for bar, val in zip(bars, por_cat.values):
        ax.text(val + por_cat.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f'${val:,.0f}', va='center', fontsize=9, color=COLORES[0])

    ax.set_title('Ventas por Categoria', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Total ($)', fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3)

    fig.tight_layout()
    return _fig_a_bytes(fig)


def generar_grafico_por_region(df):
    """Grafico de pastel: distribucion de ventas por region."""
    if df.empty:
        return _grafico_vacio('Sin datos por region')

    por_region = df.groupby('region')['total'].sum()

    fig, ax = plt.subplots(figsize=(7, 5))

    wedges, texts, autotexts = ax.pie(
        por_region.values,
        labels=por_region.index,
        autopct='%1.1f%%',
        colors=COLORES[:len(por_region)],
        startangle=90,
        pctdistance=0.85,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2},
    )

    for text in autotexts:
        text.set_fontsize(9)
        text.set_fontweight('bold')

    ax.set_title('Distribucion por Region', fontsize=14, fontweight='bold', pad=15)

    fig.tight_layout()
    return _fig_a_bytes(fig)


def generar_grafico_top_productos(df, top_n=10):
    """Grafico de barras: top N productos mas vendidos."""
    if df.empty:
        return _grafico_vacio('Sin datos de productos')

    top = df.groupby('producto')['total'].sum().nlargest(top_n).sort_values()

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.barh(top.index, top.values, color=COLORES[1], edgecolor='white')

    for bar, val in zip(bars, top.values):
        ax.text(val + top.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f'${val:,.0f}', va='center', fontsize=9)

    ax.set_title(f'Top {top_n} Productos por Ventas', fontsize=14,
                 fontweight='bold', pad=15)
    ax.set_xlabel('Total ($)', fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3)

    fig.tight_layout()
    return _fig_a_bytes(fig)


def generar_grafico_top_clientes(df, top_n=10):
    """Grafico de barras: top N clientes por gasto total."""
    if df.empty:
        return _grafico_vacio('Sin datos de clientes')

    top = df.groupby('cliente')['total'].sum().nlargest(top_n).sort_values()

    fig, ax = plt.subplots(figsize=(9, 5))

    bars = ax.barh(top.index, top.values, color=COLORES[2], edgecolor='white')

    for bar, val in zip(bars, top.values):
        ax.text(val + top.max() * 0.01, bar.get_y() + bar.get_height() / 2,
                f'${val:,.0f}', va='center', fontsize=9)

    ax.set_title(f'Top {top_n} Clientes por Gasto', fontsize=14,
                 fontweight='bold', pad=15)
    ax.set_xlabel('Total ($)', fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.3)

    fig.tight_layout()
    return _fig_a_bytes(fig)


def generar_grafico_prediccion(df, meses_futuro=3):
    """Grafico de lineas: historico + prediccion con regresion lineal."""
    pred = calcular_prediccion(df, meses_futuro)

    if not pred['historico']:
        return _grafico_vacio('Datos insuficientes para prediccion')

    fig, ax = plt.subplots(figsize=(10, 5))

    # Datos historicos
    meses_hist = [h['mes'] for h in pred['historico']]
    valores_hist = [h['real'] for h in pred['historico']]
    linea_modelo = [h['modelo'] for h in pred['historico']]

    # Datos predichos
    meses_pred = [p['mes'] for p in pred['predicciones']]
    valores_pred = [p['prediccion'] for p in pred['predicciones']]

    # Todos los meses juntos para el eje X
    todos_meses = meses_hist + meses_pred
    x_hist = range(len(meses_hist))
    x_pred = range(len(meses_hist) - 1, len(todos_meses))

    # Linea de datos reales
    ax.plot(x_hist, valores_hist, color=COLORES[0], linewidth=2,
            marker='o', markersize=5, label='Ventas reales')

    # Linea del modelo (regresion)
    x_modelo = list(x_hist) + list(range(len(meses_hist), len(todos_meses)))
    y_modelo = linea_modelo + valores_pred
    ax.plot(x_modelo, y_modelo, color=COLORES[3], linewidth=2,
            linestyle='--', label=f'Modelo (R²={pred["r_cuadrado"]:.2f})')

    # Puntos de prediccion
    x_pred_puntos = range(len(meses_hist), len(todos_meses))
    ax.scatter(x_pred_puntos, valores_pred, color='#ef4444', s=60,
               zorder=5, label='Prediccion')

    # Zona de prediccion sombreada
    ax.axvspan(len(meses_hist) - 0.5, len(todos_meses) - 0.5,
               alpha=0.08, color='#ef4444')

    ax.set_title('Prediccion de Ventas (Regresion Lineal)', fontsize=14,
                 fontweight='bold', pad=15)
    ax.set_xlabel('Mes', fontsize=11)
    ax.set_ylabel('Total ($)', fontsize=11)
    ax.set_xticks(range(len(todos_meses)))
    ax.set_xticklabels(todos_meses, rotation=45, ha='right', fontsize=7)
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    fig.tight_layout()
    return _fig_a_bytes(fig)


def _fig_a_bytes(fig):
    """Convierte una figura matplotlib a bytes PNG."""
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    buf.seek(0)
    plt.close(fig)
    return buf.getvalue()


def _grafico_vacio(mensaje):
    """Genera un grafico en blanco con un mensaje."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.text(0.5, 0.5, mensaje, ha='center', va='center',
            fontsize=14, color='#9ca3af')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    fig.tight_layout()
    return _fig_a_bytes(fig)


# ============================================================================
# RUTAS - AUTENTICACION
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Iniciar sesion."""
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        db = Session()
        usuario = db.query(Usuario).filter_by(email=email).first()

        if usuario and check_password_hash(usuario.password_hash, password):
            session['usuario_id'] = usuario.id
            flash(f'Bienvenido, {usuario.nombre}!', 'success')
            db.close()
            return redirect(url_for('index'))

        db.close()
        flash('Email o contrasena incorrectos.', 'danger')

    return render_template('auth/login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registrar nuevo usuario."""
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirmar = request.form.get('confirmar', '')

        if not nombre or not email or not password:
            flash('Todos los campos son obligatorios.', 'danger')
            return render_template('auth/registro.html')

        if password != confirmar:
            flash('Las contrasenas no coinciden.', 'danger')
            return render_template('auth/registro.html')

        db = Session()
        if db.query(Usuario).filter_by(email=email).first():
            flash('Ya existe una cuenta con ese email.', 'danger')
            db.close()
            return render_template('auth/registro.html')

        usuario = Usuario(
            nombre=nombre,
            email=email,
            password_hash=generate_password_hash(password),
            rol='usuario',
        )
        db.add(usuario)
        db.commit()
        session['usuario_id'] = usuario.id
        db.close()

        flash('Cuenta creada exitosamente!', 'success')
        return redirect(url_for('index'))

    return render_template('auth/registro.html')


@app.route('/logout')
def logout():
    """Cerrar sesion."""
    session.clear()
    flash('Sesion cerrada.', 'info')
    return redirect(url_for('login'))


# ============================================================================
# RUTAS - DASHBOARD PRINCIPAL
# ============================================================================

@app.route('/')
@login_requerido
def index():
    """
    Dashboard principal con KPIs y graficos.

    Esta es la pagina mas importante de la aplicacion. Muestra:
    1. Tarjetas con KPIs principales
    2. Graficos embebidos como <img src="/chart/...">
    3. Resumen rapido de datos
    """
    df = obtener_dataframe()
    kpis = calcular_kpis(df)

    # Obtener lista de categorias y regiones para los filtros rapidos
    db = Session()
    categorias = [r[0] for r in db.query(Venta.categoria).distinct().all()]
    regiones = [r[0] for r in db.query(Venta.region).distinct().all()]
    db.close()

    return render_template('index.html',
                           kpis=kpis,
                           categorias=categorias,
                           regiones=regiones,
                           total_registros=len(df))


# ============================================================================
# RUTAS - GRAFICOS (ENDPOINTS DE IMAGENES PNG)
# ============================================================================
# Cada ruta genera un grafico con matplotlib y lo devuelve como imagen PNG.
# En los templates se usan como: <img src="/chart/mensual">
#
# El header Content-Type: image/png le dice al navegador que es una imagen.
# ============================================================================

@app.route('/chart/mensual')
@login_requerido
def chart_mensual():
    """Grafico de ventas mensuales."""
    filtros = _extraer_filtros_query()
    df = obtener_dataframe(filtros)
    png = generar_grafico_ventas_mensual(df)
    return Response(png, mimetype='image/png')


@app.route('/chart/categoria')
@login_requerido
def chart_categoria():
    """Grafico de ventas por categoria."""
    filtros = _extraer_filtros_query()
    df = obtener_dataframe(filtros)
    png = generar_grafico_por_categoria(df)
    return Response(png, mimetype='image/png')


@app.route('/chart/region')
@login_requerido
def chart_region():
    """Grafico de ventas por region."""
    filtros = _extraer_filtros_query()
    df = obtener_dataframe(filtros)
    png = generar_grafico_por_region(df)
    return Response(png, mimetype='image/png')


@app.route('/chart/top_productos')
@login_requerido
def chart_top_productos():
    """Grafico de top productos."""
    filtros = _extraer_filtros_query()
    df = obtener_dataframe(filtros)
    png = generar_grafico_top_productos(df)
    return Response(png, mimetype='image/png')


@app.route('/chart/top_clientes')
@login_requerido
def chart_top_clientes():
    """Grafico de top clientes."""
    filtros = _extraer_filtros_query()
    df = obtener_dataframe(filtros)
    png = generar_grafico_top_clientes(df)
    return Response(png, mimetype='image/png')


@app.route('/chart/prediccion')
@login_requerido
def chart_prediccion():
    """Grafico de prediccion."""
    meses = request.args.get('meses', 3, type=int)
    df = obtener_dataframe()
    png = generar_grafico_prediccion(df, meses)
    return Response(png, mimetype='image/png')


def _extraer_filtros_query():
    """Extrae filtros de los parametros de query string."""
    filtros = {}
    if request.args.get('fecha_inicio'):
        filtros['fecha_inicio'] = request.args['fecha_inicio']
    if request.args.get('fecha_fin'):
        filtros['fecha_fin'] = request.args['fecha_fin']
    if request.args.get('categoria'):
        filtros['categoria'] = request.args['categoria']
    if request.args.get('region'):
        filtros['region'] = request.args['region']
    return filtros if filtros else None


# ============================================================================
# RUTAS - ANALISIS Y FILTROS
# ============================================================================

@app.route('/analisis/filtros', methods=['GET', 'POST'])
@login_requerido
def analisis_filtros():
    """
    Pagina de filtros avanzados.
    Permite al usuario filtrar datos por fecha, categoria y region,
    y ver los resultados con estadisticas y graficos filtrados.
    """
    db = Session()
    categorias = [r[0] for r in db.query(Venta.categoria).distinct().all()]
    regiones = [r[0] for r in db.query(Venta.region).distinct().all()]
    db.close()

    filtros = {}
    resultados = None
    kpis = None
    estadisticas = None
    query_params = ''

    if request.method == 'POST' or request.args.get('aplicar'):
        # Obtener filtros del formulario o query string
        if request.method == 'POST':
            filtros = {
                'fecha_inicio': request.form.get('fecha_inicio', ''),
                'fecha_fin': request.form.get('fecha_fin', ''),
                'categoria': request.form.get('categoria', ''),
                'region': request.form.get('region', ''),
            }
        else:
            filtros = {
                'fecha_inicio': request.args.get('fecha_inicio', ''),
                'fecha_fin': request.args.get('fecha_fin', ''),
                'categoria': request.args.get('categoria', ''),
                'region': request.args.get('region', ''),
            }

        # Limpiar filtros vacios
        filtros_limpios = {k: v for k, v in filtros.items() if v}

        df = obtener_dataframe(filtros_limpios if filtros_limpios else None)
        kpis = calcular_kpis(df)
        estadisticas = calcular_estadisticas(df)

        # Construir query params para los graficos
        params = []
        for k, v in filtros.items():
            if v:
                params.append(f'{k}={v}')
        query_params = '&'.join(params)

        # Primeras 50 filas como tabla
        if not df.empty:
            resultados = df.head(50).to_dict('records')
            for r in resultados:
                r['fecha'] = r['fecha'].strftime('%d/%m/%Y')
                r['total'] = f"${r['total']:,.2f}"
                r['precio_unitario'] = f"${r['precio_unitario']:,.2f}"

    return render_template('analisis/filtros.html',
                           categorias=categorias,
                           regiones=regiones,
                           filtros=filtros,
                           resultados=resultados,
                           kpis=kpis,
                           estadisticas=estadisticas,
                           query_params=query_params)


@app.route('/analisis/prediccion')
@login_requerido
def analisis_prediccion():
    """
    Pagina de prediccion de ventas usando regresion lineal.
    Muestra el grafico de prediccion y las metricas del modelo.
    """
    meses = request.args.get('meses', 3, type=int)
    if meses < 1:
        meses = 1
    if meses > 12:
        meses = 12

    df = obtener_dataframe()
    prediccion = calcular_prediccion(df, meses)

    return render_template('analisis/prediccion.html',
                           prediccion=prediccion,
                           meses=meses)


# ============================================================================
# RUTAS - EXPORTAR CSV
# ============================================================================

@app.route('/exportar/csv')
@login_requerido
def exportar_csv():
    """
    Exporta datos de ventas a un archivo CSV descargable.

    Usa pandas DataFrame.to_csv() para generar el contenido CSV.
    Los headers HTTP Content-Disposition y Content-Type le dicen
    al navegador que debe descargar el archivo.
    """
    filtros = _extraer_filtros_query()
    df = obtener_dataframe(filtros)

    if df.empty:
        flash('No hay datos para exportar.', 'warning')
        return redirect(url_for('analisis_filtros'))

    # Formatear fecha para el CSV
    df_export = df.copy()
    df_export['fecha'] = df_export['fecha'].dt.strftime('%Y-%m-%d')

    # Generar CSV en memoria
    csv_content = df_export.to_csv(index=False)

    # Crear respuesta con headers de descarga
    response = make_response(csv_content)
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    fecha_hoy = datetime.now().strftime('%Y%m%d_%H%M%S')
    response.headers['Content-Disposition'] = f'attachment; filename=ventas_{fecha_hoy}.csv'

    return response


# ============================================================================
# RUTAS - REPORTES
# ============================================================================

@app.route('/reportes')
@login_requerido
def reportes_lista():
    """Lista de reportes generados."""
    db = Session()
    reportes = db.query(Reporte).order_by(Reporte.fecha_generacion.desc()).all()
    db.close()
    return render_template('reportes/lista.html', reportes=reportes)


@app.route('/reportes/<int:id>')
@login_requerido
def reporte_detalle(id):
    """Detalle de un reporte guardado."""
    db = Session()
    reporte = db.query(Reporte).get(id)
    db.close()

    if not reporte:
        flash('Reporte no encontrado.', 'danger')
        return redirect(url_for('reportes_lista'))

    # Recalcular datos del reporte
    filtros = reporte.parametros
    df = obtener_dataframe(filtros if filtros else None)
    kpis = calcular_kpis(df)
    estadisticas = calcular_estadisticas(df)

    # Construir query params para graficos
    params = []
    for k, v in (filtros or {}).items():
        if v:
            params.append(f'{k}={v}')
    query_params = '&'.join(params)

    return render_template('reportes/detalle.html',
                           reporte=reporte,
                           kpis=kpis,
                           estadisticas=estadisticas,
                           query_params=query_params)


@app.route('/reportes/generar', methods=['POST'])
@login_requerido
def generar_reporte():
    """Genera y guarda un nuevo reporte."""
    titulo = request.form.get('titulo', '').strip()
    tipo = request.form.get('tipo', 'general')

    if not titulo:
        titulo = f'Reporte {tipo.capitalize()} - {datetime.now().strftime("%d/%m/%Y %H:%M")}'

    # Recoger filtros actuales
    filtros = {
        'fecha_inicio': request.form.get('fecha_inicio', ''),
        'fecha_fin': request.form.get('fecha_fin', ''),
        'categoria': request.form.get('categoria', ''),
        'region': request.form.get('region', ''),
    }
    filtros_limpios = {k: v for k, v in filtros.items() if v}

    db = Session()
    reporte = Reporte(
        titulo=titulo,
        tipo=tipo,
        parametros_json=json.dumps(filtros_limpios),
    )
    db.add(reporte)
    db.commit()
    reporte_id = reporte.id
    db.close()

    flash(f'Reporte "{titulo}" generado exitosamente.', 'success')
    return redirect(url_for('reporte_detalle', id=reporte_id))


# ============================================================================
# RUTA - ERROR 404
# ============================================================================

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('error.html',
                           codigo=404,
                           mensaje='Pagina no encontrada'), 404


@app.errorhandler(500)
def error_interno(e):
    return render_template('error.html',
                           codigo=500,
                           mensaje='Error interno del servidor'), 500


# ============================================================================
# INICIAR LA APLICACION
# ============================================================================

if __name__ == '__main__':
    # Generar datos de ejemplo en la primera ejecucion
    generar_datos_ejemplo()

    print('=' * 60)
    print('  DASHBOARD DE ANALISIS DE VENTAS')
    print('  Semana 11: Ciencia de Datos con Python')
    print('=' * 60)
    print(f'  URL: http://localhost:5013')
    print(f'  Admin: admin@ejemplo.com / admin123')
    print('=' * 60)

    app.run(debug=True, port=5013)
