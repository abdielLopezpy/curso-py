# ============================================================================
# SEMANA 11 - PROYECTO 2: ANALISIS DE IMAGEN CON CIENCIA DE DATOS
# ============================================================================
# Aplicacion web Flask que permite subir imagenes y aplicar tecnicas de
# ciencia de datos para analizarlas: histogramas de color, deteccion de
# bordes, segmentacion por clustering (K-Means), comparacion de imagenes
# y extraccion de paletas de color.
#
# Conceptos aplicados:
# - numpy: manipulacion de matrices de pixeles, operaciones vectorizadas
# - pandas: tablas de estadisticas de imagen, resumen de canales RGB
# - matplotlib: histogramas, graficos de distribucion de color
# - scipy: filtros (gaussian, sobel), distancias entre imagenes
# - PIL (Pillow): lectura/escritura de imagenes, transformaciones basicas
# - sklearn (KMeans): segmentacion y extraccion de paleta de color
# - opencv (cv2): captura de camara en tiempo real y streaming MJPEG
#
# COMO EJECUTAR:
# 1. pip install flask pillow numpy pandas matplotlib scipy scikit-learn opencv-python
# 2. python app.py
# 3. Abre: http://localhost:5014
#
# CREDENCIALES:
# - Admin: admin@ejemplo.com / admin123
# ============================================================================

import os
import json
import uuid
from datetime import datetime
from functools import wraps
from io import BytesIO

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from PIL import Image, ImageFilter, ImageOps
from scipy import ndimage
from scipy.spatial.distance import cosine
import cv2
import threading
import base64

from flask import (
    Flask, render_template_string, request, redirect, url_for,
    session, flash, Response, send_file, jsonify
)

# ============================================================================
# CONFIGURACION
# ============================================================================

app = Flask(__name__)
app.secret_key = 'vision-analisis-semana11-secreto'

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}

# ============================================================================
# USUARIOS SIMPLES (sin BD para mantener el foco en vision)
# ============================================================================

USERS = {
    'admin@ejemplo.com': {
        'password': 'admin123',
        'nombre': 'Administrador'
    }
}

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            flash('Debes iniciar sesion', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============================================================================
# FUNCIONES DE ANALISIS DE IMAGEN (Ciencia de Datos)
# ============================================================================

def imagen_a_array(filepath):
    """Convierte imagen a numpy array RGB."""
    img = Image.open(filepath).convert('RGB')
    return np.array(img)

def estadisticas_imagen(arr):
    """
    Calcula estadisticas por canal (R, G, B) usando numpy y pandas.
    Retorna un DataFrame con media, mediana, std, min, max por canal.
    """
    canales = {'Rojo': arr[:, :, 0], 'Verde': arr[:, :, 1], 'Azul': arr[:, :, 2]}
    stats = []
    for nombre, canal in canales.items():
        stats.append({
            'Canal': nombre,
            'Media': round(float(np.mean(canal)), 2),
            'Mediana': float(np.median(canal)),
            'Desv_Estandar': round(float(np.std(canal)), 2),
            'Min': int(np.min(canal)),
            'Max': int(np.max(canal)),
            'Q1': float(np.percentile(canal, 25)),
            'Q3': float(np.percentile(canal, 75)),
        })
    df = pd.DataFrame(stats)
    df['IQR'] = df['Q3'] - df['Q1']
    return df

def generar_histograma_rgb(arr):
    """Genera histograma de canales R, G, B con matplotlib."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    colores = ['red', 'green', 'blue']
    nombres = ['Rojo', 'Verde', 'Azul']
    for i, (ax, color, nombre) in enumerate(zip(axes, colores, nombres)):
        datos_canal = arr[:, :, i].flatten()
        ax.hist(datos_canal, bins=64, color=color, alpha=0.7, edgecolor='black', linewidth=0.3)
        ax.set_title(f'Canal {nombre}')
        ax.set_xlabel('Intensidad (0-255)')
        ax.set_ylabel('Frecuencia')
        ax.set_xlim(0, 255)
        media = np.mean(datos_canal)
        ax.axvline(media, color='black', linestyle='--', linewidth=1, label=f'Media={media:.0f}')
        ax.legend(fontsize=8)
    fig.suptitle('Distribucion de Intensidad por Canal', fontsize=14, fontweight='bold')
    plt.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close(fig)
    return buf

def aplicar_escala_grises(arr):
    """Convierte a escala de grises usando pesos perceptuales (numpy)."""
    gris = np.dot(arr[:, :, :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
    return gris

def aplicar_deteccion_bordes(arr):
    """Detecta bordes usando filtro Sobel (scipy.ndimage)."""
    gris = aplicar_escala_grises(arr).astype(float)
    sobel_x = ndimage.sobel(gris, axis=1)
    sobel_y = ndimage.sobel(gris, axis=0)
    bordes = np.hypot(sobel_x, sobel_y)
    bordes = (bordes / bordes.max() * 255).astype(np.uint8)
    return bordes

def aplicar_desenfoque(arr, sigma=3):
    """Aplica desenfoque gaussiano (scipy.ndimage)."""
    resultado = np.zeros_like(arr)
    for i in range(3):
        resultado[:, :, i] = ndimage.gaussian_filter(arr[:, :, i], sigma=sigma)
    return resultado

def aplicar_ecualizacion(arr):
    """Ecualiza el histograma para mejorar contraste (numpy)."""
    resultado = np.zeros_like(arr)
    for i in range(3):
        canal = arr[:, :, i]
        hist, bins = np.histogram(canal.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_normalizado = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
        resultado[:, :, i] = cdf_normalizado[canal].astype(np.uint8)
    return resultado

def extraer_paleta_color(arr, n_colores=6):
    """
    Extrae paleta de colores dominantes usando K-Means (scikit-learn).
    Reduce los millones de pixeles a n_colores representativos.
    """
    try:
        from sklearn.cluster import KMeans
    except ImportError:
        # Fallback sin sklearn: muestreo simple
        pixeles = arr.reshape(-1, 3)
        indices = np.random.choice(len(pixeles), min(n_colores, len(pixeles)), replace=False)
        return pixeles[indices]

    pixeles = arr.reshape(-1, 3).astype(float)
    # Muestrear para velocidad
    if len(pixeles) > 10000:
        indices = np.random.choice(len(pixeles), 10000, replace=False)
        muestra = pixeles[indices]
    else:
        muestra = pixeles

    kmeans = KMeans(n_clusters=n_colores, random_state=42, n_init=10)
    kmeans.fit(muestra)
    return kmeans.cluster_centers_.astype(int)

def generar_grafico_paleta(paleta):
    """Genera un grafico visual de la paleta de colores."""
    fig, ax = plt.subplots(1, 1, figsize=(10, 2))
    n = len(paleta)
    for i, color in enumerate(paleta):
        color_norm = [c / 255.0 for c in color]
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color_norm))
        hex_color = '#{:02x}{:02x}{:02x}'.format(*color)
        ax.text(i + 0.5, 0.5, hex_color, ha='center', va='center',
                fontsize=8, fontweight='bold',
                color='white' if sum(color) < 380 else 'black')
    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.set_title('Paleta de Colores Dominantes (K-Means)', fontsize=12, fontweight='bold')
    plt.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close(fig)
    return buf

def comparar_imagenes(arr1, arr2):
    """
    Compara dos imagenes usando multiples metricas de ciencia de datos:
    - Distancia coseno entre histogramas
    - Error cuadratico medio (MSE)
    - Correlacion entre canales
    """
    # Redimensionar a mismo tamano
    size = (min(arr1.shape[1], arr2.shape[1]), min(arr1.shape[0], arr2.shape[0]))
    img1 = Image.fromarray(arr1).resize(size)
    img2 = Image.fromarray(arr2).resize(size)
    a1 = np.array(img1).astype(float)
    a2 = np.array(img2).astype(float)

    # MSE
    mse = float(np.mean((a1 - a2) ** 2))

    # Histogramas y distancia coseno
    hist1 = np.histogram(a1.flatten(), bins=64, range=(0, 256))[0].astype(float)
    hist2 = np.histogram(a2.flatten(), bins=64, range=(0, 256))[0].astype(float)
    dist_coseno = float(cosine(hist1, hist2))
    similitud = round((1 - dist_coseno) * 100, 2)

    # Correlacion por canal
    correlaciones = {}
    for i, nombre in enumerate(['Rojo', 'Verde', 'Azul']):
        c1 = a1[:, :, i].flatten()
        c2 = a2[:, :, i].flatten()
        corr = float(np.corrcoef(c1, c2)[0, 1])
        correlaciones[nombre] = round(corr, 4)

    return {
        'mse': round(mse, 2),
        'similitud_coseno': similitud,
        'correlaciones': correlaciones,
    }

def generar_grafico_comparacion(arr1, arr2):
    """Genera grafico comparativo de histogramas de dos imagenes."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    colores = ['red', 'green', 'blue']
    nombres = ['Rojo', 'Verde', 'Azul']
    for i, (ax, color, nombre) in enumerate(zip(axes, colores, nombres)):
        ax.hist(arr1[:, :, i].flatten(), bins=64, color=color, alpha=0.4,
                label='Imagen 1', edgecolor='black', linewidth=0.2)
        ax.hist(arr2[:, :, i].flatten(), bins=64, color=color, alpha=0.4,
                label='Imagen 2', edgecolor='gray', linewidth=0.2, linestyle='--')
        ax.set_title(f'Canal {nombre}')
        ax.set_xlabel('Intensidad')
        ax.legend(fontsize=8)
    fig.suptitle('Comparacion de Histogramas', fontsize=14, fontweight='bold')
    plt.tight_layout()
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close(fig)
    return buf

# ============================================================================
# CAMARA EN TIEMPO REAL (OpenCV)
# ============================================================================

class CameraStream:
    """
    Captura video de la camara usando OpenCV y aplica filtros en tiempo real.
    Usa un hilo separado para no bloquear el servidor Flask.
    """
    def __init__(self):
        self.cap = None
        self.filtro_actual = 'normal'
        self.lock = threading.Lock()
        self.running = False
        self.last_stats = {}

    def start(self):
        if self.running:
            return
        self.cap = cv2.VideoCapture(0)
        self.running = True

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None

    def set_filtro(self, filtro):
        with self.lock:
            self.filtro_actual = filtro

    def get_frame(self):
        if not self.cap or not self.running:
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None

        # Convertir BGR (OpenCV) a RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Calcular estadisticas en tiempo real con numpy/pandas
        stats = {}
        for i, nombre in enumerate(['Rojo', 'Verde', 'Azul']):
            canal = frame_rgb[:, :, i]
            stats[nombre] = {
                'media': round(float(np.mean(canal)), 1),
                'std': round(float(np.std(canal)), 1),
            }
        self.last_stats = stats

        # Aplicar filtro seleccionado
        with self.lock:
            filtro = self.filtro_actual

        if filtro == 'grises':
            gris = aplicar_escala_grises(frame_rgb)
            frame_out = cv2.cvtColor(gris, cv2.COLOR_GRAY2BGR)
        elif filtro == 'bordes':
            bordes = aplicar_deteccion_bordes(frame_rgb)
            frame_out = cv2.cvtColor(bordes, cv2.COLOR_GRAY2BGR)
        elif filtro == 'desenfoque':
            blur = aplicar_desenfoque(frame_rgb, sigma=5)
            frame_out = cv2.cvtColor(blur, cv2.COLOR_RGB2BGR)
        elif filtro == 'ecualizar':
            ecualizado = aplicar_ecualizacion(frame_rgb)
            frame_out = cv2.cvtColor(ecualizado, cv2.COLOR_RGB2BGR)
        else:
            frame_out = frame  # Ya esta en BGR para cv2

        # Superponer estadisticas en el frame
        y = 25
        for nombre, vals in stats.items():
            texto = f'{nombre}: media={vals["media"]} std={vals["std"]}'
            cv2.putText(frame_out, texto, (10, y), cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, (255, 255, 255), 1, cv2.LINE_AA)
            y += 20

        # Codificar como JPEG
        _, jpeg = cv2.imencode('.jpg', frame_out, [cv2.IMWRITE_JPEG_QUALITY, 80])
        return jpeg.tobytes()

    def generate_mjpeg(self):
        """Generador para streaming MJPEG."""
        while self.running:
            frame = self.get_frame()
            if frame is None:
                continue
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def capture_snapshot(self):
        """Captura un frame como array numpy RGB para analisis."""
        if not self.cap or not self.running:
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

camera = CameraStream()

# ============================================================================
# PLANTILLAS HTML
# ============================================================================

LOGIN_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Login{% endblock %}
{% block content %}
<div style="max-width:400px; margin:3rem auto;">
    <div class="card">
        <h2>Iniciar Sesion</h2>
        <form method="POST">
            <label>Email:</label>
            <input type="email" name="email" required>
            <label>Password:</label>
            <input type="password" name="password" required>
            <br><br>
            <button class="btn btn-primary" type="submit">Entrar</button>
        </form>
    </div>
</div>
{% endblock %}
"""

DASHBOARD_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Dashboard{% endblock %}
{% block content %}
<h1 style="margin-bottom:1rem;">Dashboard de Analisis de Imagen</h1>
<div class="grid-2">
    <div class="card">
        <h2>Subir y Analizar</h2>
        <p>Sube una imagen para obtener estadisticas detalladas de sus canales RGB,
           histogramas de distribucion y metricas calculadas con numpy y pandas.</p>
        <br>
        <a href="{{ url_for('subir') }}" class="btn btn-primary">Subir Imagen</a>
    </div>
    <div class="card">
        <h2>Filtros y Transformaciones</h2>
        <p>Aplica transformaciones: escala de grises, deteccion de bordes (Sobel),
           desenfoque gaussiano y ecualizacion de histograma usando scipy.</p>
        <br>
        <a href="{{ url_for('filtros') }}" class="btn btn-primary">Aplicar Filtros</a>
    </div>
    <div class="card">
        <h2>Comparar Imagenes</h2>
        <p>Compara dos imagenes usando MSE, distancia coseno entre histogramas y
           correlacion por canal. Visualiza diferencias con matplotlib.</p>
        <br>
        <a href="{{ url_for('comparar') }}" class="btn btn-primary">Comparar</a>
    </div>
    <div class="card">
        <h2>Paleta de Color</h2>
        <p>Extrae los colores dominantes de una imagen usando clustering K-Means
           (scikit-learn). Reduce millones de pixeles a una paleta representativa.</p>
        <br>
        <a href="{{ url_for('paleta') }}" class="btn btn-primary">Extraer Paleta</a>
    </div>
</div>

{% if stats_df is not none %}
<div class="card">
    <h2>Ultima Imagen Analizada</h2>
    <div class="grid-2">
        <div>
            <img src="{{ url_for('static', filename='uploads/' + last_image) }}" class="img-preview">
            <p style="margin-top:0.5rem; color:#666;">{{ last_image }} - {{ img_size }}</p>
        </div>
        <div>
            <h3>Estadisticas por Canal (pandas DataFrame)</h3>
            {{ stats_html|safe }}
            <br>
            <img src="{{ url_for('chart_histograma', filename=last_image) }}" class="img-preview">
        </div>
    </div>
</div>
{% endif %}
{% endblock %}
"""

SUBIR_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Subir Imagen{% endblock %}
{% block content %}
<div class="card">
    <h2>Subir Imagen para Analisis</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="imagen" accept="image/*" required>
        <br><br>
        <button class="btn btn-primary" type="submit">Analizar</button>
    </form>
</div>

{% if stats_df is not none %}
<div class="card">
    <h2>Resultados del Analisis</h2>
    <div class="grid-2">
        <div>
            <img src="{{ url_for('static', filename='uploads/' + filename) }}" class="img-preview">
            <p>Dimensiones: {{ dimensiones }}</p>
            <p>Pixeles totales: {{ total_pixeles }}</p>
        </div>
        <div>
            <h3>Estadisticas por Canal RGB</h3>
            {{ stats_html|safe }}
        </div>
    </div>
    <br>
    <h3>Histograma de Distribucion de Color</h3>
    <img src="{{ url_for('chart_histograma', filename=filename) }}" class="img-preview">
</div>
{% endif %}
{% endblock %}
"""

FILTROS_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Filtros{% endblock %}
{% block content %}
<div class="card">
    <h2>Aplicar Filtros y Transformaciones</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>Imagen:</label>
        <input type="file" name="imagen" accept="image/*" required>
        <br>
        <label>Filtro:</label>
        <select name="filtro">
            <option value="grises">Escala de Grises (pesos perceptuales)</option>
            <option value="bordes">Deteccion de Bordes (Sobel)</option>
            <option value="desenfoque">Desenfoque Gaussiano (sigma=3)</option>
            <option value="ecualizar">Ecualizacion de Histograma</option>
        </select>
        <br><br>
        <button class="btn btn-primary" type="submit">Aplicar</button>
    </form>
</div>

{% if resultado %}
<div class="card">
    <h2>Resultado: {{ filtro_nombre }}</h2>
    <div class="grid-2">
        <div>
            <h3>Original</h3>
            <img src="{{ url_for('static', filename='uploads/' + original) }}" class="img-preview">
        </div>
        <div>
            <h3>Procesada</h3>
            <img src="{{ url_for('static', filename='uploads/' + resultado) }}" class="img-preview">
        </div>
    </div>
    <br>
    <h3>Comparacion de Estadisticas</h3>
    <div class="grid-2">
        <div>
            <h4>Original</h4>
            {{ stats_original|safe }}
        </div>
        <div>
            <h4>Procesada</h4>
            {{ stats_resultado|safe }}
        </div>
    </div>
</div>
{% endif %}
{% endblock %}
"""

COMPARAR_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Comparar{% endblock %}
{% block content %}
<div class="card">
    <h2>Comparar Dos Imagenes</h2>
    <form method="POST" enctype="multipart/form-data">
        <div class="grid-2">
            <div>
                <label>Imagen 1:</label>
                <input type="file" name="imagen1" accept="image/*" required>
            </div>
            <div>
                <label>Imagen 2:</label>
                <input type="file" name="imagen2" accept="image/*" required>
            </div>
        </div>
        <br>
        <button class="btn btn-primary" type="submit">Comparar</button>
    </form>
</div>

{% if metricas %}
<div class="card">
    <h2>Resultados de Comparacion</h2>
    <div class="grid-2">
        <div>
            <h3>Imagen 1</h3>
            <img src="{{ url_for('static', filename='uploads/' + img1) }}" class="img-preview">
        </div>
        <div>
            <h3>Imagen 2</h3>
            <img src="{{ url_for('static', filename='uploads/' + img2) }}" class="img-preview">
        </div>
    </div>
    <br>
    <div style="display:flex; gap:1rem; flex-wrap:wrap;">
        <div class="stat-box" style="flex:1;">
            <h3>{{ metricas.similitud_coseno }}%</h3>
            <p>Similitud (coseno)</p>
        </div>
        <div class="stat-box" style="flex:1;">
            <h3>{{ metricas.mse }}</h3>
            <p>Error Cuadratico Medio</p>
        </div>
        {% for canal, valor in metricas.correlaciones.items() %}
        <div class="stat-box" style="flex:1;">
            <h3>{{ valor }}</h3>
            <p>Correlacion {{ canal }}</p>
        </div>
        {% endfor %}
    </div>
    <br>
    <h3>Histogramas Comparativos</h3>
    <img src="{{ url_for('chart_comparacion', img1=img1, img2=img2) }}" class="img-preview">
</div>
{% endif %}
{% endblock %}
"""

PALETA_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Paleta de Color{% endblock %}
{% block content %}
<div class="card">
    <h2>Extraer Paleta de Colores (K-Means)</h2>
    <form method="POST" enctype="multipart/form-data">
        <label>Imagen:</label>
        <input type="file" name="imagen" accept="image/*" required>
        <br>
        <label>Numero de colores:</label>
        <select name="n_colores">
            <option value="4">4</option>
            <option value="6" selected>6</option>
            <option value="8">8</option>
            <option value="10">10</option>
        </select>
        <br><br>
        <button class="btn btn-primary" type="submit">Extraer Paleta</button>
    </form>
</div>

{% if paleta_img %}
<div class="card">
    <h2>Paleta Extraida</h2>
    <img src="{{ url_for('static', filename='uploads/' + filename) }}" class="img-preview"
         style="max-height:300px; object-fit:contain;">
    <br><br>
    <img src="{{ url_for('chart_paleta', filename=filename, n=n_colores) }}" class="img-preview">
    <br>
    <h3>Estadisticas de la Imagen</h3>
    {{ stats_html|safe }}
</div>
{% endif %}
{% endblock %}
"""

CAMARA_TEMPLATE = """
{% extends 'base.html' %}
{% block title %}Camara en Tiempo Real{% endblock %}
{% block content %}
<div class="card">
    <h2>Analisis de Camara en Tiempo Real</h2>
    <p>La camara captura video con OpenCV, aplica filtros con scipy/numpy y
       muestra estadisticas RGB en tiempo real.</p>
    <br>
    <div class="filtros">
        <a href="{{ url_for('camara_view', filtro='normal') }}" class="btn {% if filtro=='normal' %}btn-primary{% else %}btn-secondary{% endif %}">Normal</a>
        <a href="{{ url_for('camara_view', filtro='grises') }}" class="btn {% if filtro=='grises' %}btn-primary{% else %}btn-secondary{% endif %}">Escala de Grises</a>
        <a href="{{ url_for('camara_view', filtro='bordes') }}" class="btn {% if filtro=='bordes' %}btn-primary{% else %}btn-secondary{% endif %}">Bordes (Sobel)</a>
        <a href="{{ url_for('camara_view', filtro='desenfoque') }}" class="btn {% if filtro=='desenfoque' %}btn-primary{% else %}btn-secondary{% endif %}">Desenfoque</a>
        <a href="{{ url_for('camara_view', filtro='ecualizar') }}" class="btn {% if filtro=='ecualizar' %}btn-primary{% else %}btn-secondary{% endif %}">Ecualizar</a>
    </div>
    <div style="text-align:center;">
        <img src="{{ url_for('video_feed') }}" style="max-width:100%; border-radius:8px; border:2px solid #1a237e;">
    </div>
    <br>
    <div class="grid-2">
        <div>
            <a href="{{ url_for('camara_snapshot') }}" class="btn btn-success">Capturar Foto y Analizar</a>
        </div>
        <div>
            <a href="{{ url_for('camara_stop') }}" class="btn btn-secondary">Detener Camara</a>
        </div>
    </div>
</div>

{% if snapshot_stats %}
<div class="card">
    <h2>Analisis de Captura</h2>
    <div class="grid-2">
        <div>
            <img src="{{ url_for('static', filename='uploads/' + snapshot_file) }}" class="img-preview">
        </div>
        <div>
            <h3>Estadisticas (pandas DataFrame)</h3>
            {{ snapshot_stats|safe }}
        </div>
    </div>
    <br>
    <img src="{{ url_for('chart_histograma', filename=snapshot_file) }}" class="img-preview">
</div>
{% endif %}
{% endblock %}
"""

# ============================================================================
# RUTAS DE AUTENTICACION
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        user = USERS.get(email)
        if user and user['password'] == password:
            session['user'] = email
            session['nombre'] = user['nombre']
            flash('Sesion iniciada correctamente', 'success')
            return redirect(url_for('dashboard'))
        flash('Credenciales incorrectas', 'error')
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ============================================================================
# RUTAS PRINCIPALES
# ============================================================================

@app.route('/')
@login_required
def dashboard():
    # Buscar ultima imagen subida
    archivos = [f for f in os.listdir(UPLOAD_FOLDER)
                if f.lower().endswith(tuple(ALLOWED_EXTENSIONS))]
    stats_df = None
    stats_html = ''
    last_image = ''
    img_size = ''

    if archivos:
        archivos.sort(key=lambda x: os.path.getmtime(os.path.join(UPLOAD_FOLDER, x)), reverse=True)
        last_image = archivos[0]
        filepath = os.path.join(UPLOAD_FOLDER, last_image)
        arr = imagen_a_array(filepath)
        stats_df = estadisticas_imagen(arr)
        stats_html = stats_df.to_html(classes='', index=False)
        h, w = arr.shape[:2]
        img_size = f'{w}x{h} px ({w*h:,} pixeles)'

    return render_template_string(DASHBOARD_TEMPLATE,
                                  stats_df=stats_df, stats_html=stats_html,
                                  last_image=last_image, img_size=img_size)

@app.route('/subir', methods=['GET', 'POST'])
@login_required
def subir():
    stats_df = None
    stats_html = ''
    filename = ''
    dimensiones = ''
    total_pixeles = ''

    if request.method == 'POST':
        file = request.files.get('imagen')
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f'{uuid.uuid4().hex[:8]}.{ext}'
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            arr = imagen_a_array(filepath)
            stats_df = estadisticas_imagen(arr)
            stats_html = stats_df.to_html(classes='', index=False)
            h, w = arr.shape[:2]
            dimensiones = f'{w} x {h}'
            total_pixeles = f'{w * h:,}'
            flash('Imagen analizada correctamente', 'success')
        else:
            flash('Formato no permitido. Usa PNG, JPG, BMP o GIF.', 'error')

    return render_template_string(SUBIR_TEMPLATE,
                                  stats_df=stats_df, stats_html=stats_html,
                                  filename=filename, dimensiones=dimensiones,
                                  total_pixeles=total_pixeles)

@app.route('/filtros', methods=['GET', 'POST'])
@login_required
def filtros():
    resultado = ''
    original = ''
    filtro_nombre = ''
    stats_original = ''
    stats_resultado = ''

    if request.method == 'POST':
        file = request.files.get('imagen')
        filtro = request.form.get('filtro', 'grises')

        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            original = f'{uuid.uuid4().hex[:8]}_orig.{ext}'
            filepath_orig = os.path.join(UPLOAD_FOLDER, original)
            file.save(filepath_orig)

            arr = imagen_a_array(filepath_orig)

            nombres_filtro = {
                'grises': 'Escala de Grises',
                'bordes': 'Deteccion de Bordes (Sobel)',
                'desenfoque': 'Desenfoque Gaussiano',
                'ecualizar': 'Ecualizacion de Histograma',
            }
            filtro_nombre = nombres_filtro.get(filtro, filtro)

            if filtro == 'grises':
                res = aplicar_escala_grises(arr)
                img_res = Image.fromarray(res, mode='L')
            elif filtro == 'bordes':
                res = aplicar_deteccion_bordes(arr)
                img_res = Image.fromarray(res, mode='L')
            elif filtro == 'desenfoque':
                res = aplicar_desenfoque(arr)
                img_res = Image.fromarray(res)
            elif filtro == 'ecualizar':
                res = aplicar_ecualizacion(arr)
                img_res = Image.fromarray(res)
            else:
                res = arr
                img_res = Image.fromarray(res)

            resultado = f'{uuid.uuid4().hex[:8]}_filtro.png'
            img_res.save(os.path.join(UPLOAD_FOLDER, resultado))

            # Estadisticas originales
            df_orig = estadisticas_imagen(arr)
            stats_original = df_orig.to_html(classes='', index=False)

            # Estadisticas resultado
            if len(res.shape) == 2:
                # Imagen en escala de grises
                df_res = pd.DataFrame([{
                    'Canal': 'Gris',
                    'Media': round(float(np.mean(res)), 2),
                    'Mediana': float(np.median(res)),
                    'Desv_Estandar': round(float(np.std(res)), 2),
                    'Min': int(np.min(res)),
                    'Max': int(np.max(res)),
                }])
                stats_resultado = df_res.to_html(classes='', index=False)
            else:
                df_res = estadisticas_imagen(res)
                stats_resultado = df_res.to_html(classes='', index=False)

            flash(f'Filtro "{filtro_nombre}" aplicado', 'success')
        else:
            flash('Formato no permitido', 'error')

    return render_template_string(FILTROS_TEMPLATE,
                                  resultado=resultado, original=original,
                                  filtro_nombre=filtro_nombre,
                                  stats_original=stats_original,
                                  stats_resultado=stats_resultado)

@app.route('/comparar', methods=['GET', 'POST'])
@login_required
def comparar():
    metricas = None
    img1 = ''
    img2 = ''

    if request.method == 'POST':
        file1 = request.files.get('imagen1')
        file2 = request.files.get('imagen2')

        if file1 and file2 and allowed_file(file1.filename) and allowed_file(file2.filename):
            ext1 = file1.filename.rsplit('.', 1)[1].lower()
            ext2 = file2.filename.rsplit('.', 1)[1].lower()
            img1 = f'{uuid.uuid4().hex[:8]}_cmp1.{ext1}'
            img2 = f'{uuid.uuid4().hex[:8]}_cmp2.{ext2}'

            file1.save(os.path.join(UPLOAD_FOLDER, img1))
            file2.save(os.path.join(UPLOAD_FOLDER, img2))

            arr1 = imagen_a_array(os.path.join(UPLOAD_FOLDER, img1))
            arr2 = imagen_a_array(os.path.join(UPLOAD_FOLDER, img2))

            metricas = comparar_imagenes(arr1, arr2)
            flash('Comparacion completada', 'success')
        else:
            flash('Sube dos imagenes validas', 'error')

    return render_template_string(COMPARAR_TEMPLATE,
                                  metricas=metricas, img1=img1, img2=img2)

@app.route('/paleta', methods=['GET', 'POST'])
@login_required
def paleta():
    paleta_img = False
    filename = ''
    n_colores = 6
    stats_html = ''

    if request.method == 'POST':
        file = request.files.get('imagen')
        n_colores = int(request.form.get('n_colores', 6))

        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f'{uuid.uuid4().hex[:8]}_paleta.{ext}'
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            arr = imagen_a_array(filepath)
            stats_df = estadisticas_imagen(arr)
            stats_html = stats_df.to_html(classes='', index=False)
            paleta_img = True
            flash('Paleta extraida correctamente', 'success')
        else:
            flash('Formato no permitido', 'error')

    return render_template_string(PALETA_TEMPLATE,
                                  paleta_img=paleta_img, filename=filename,
                                  n_colores=n_colores, stats_html=stats_html)

# ============================================================================
# RUTAS DE CAMARA EN TIEMPO REAL
# ============================================================================

@app.route('/camara')
@login_required
def camara_view():
    filtro = request.args.get('filtro', 'normal')
    camera.set_filtro(filtro)
    camera.start()
    return render_template_string(CAMARA_TEMPLATE,
                                  filtro=filtro, snapshot_stats=None,
                                  snapshot_file='')

@app.route('/video_feed')
@login_required
def video_feed():
    """Streaming MJPEG: cada frame es procesado con numpy/scipy en tiempo real."""
    return Response(camera.generate_mjpeg(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camara/snapshot')
@login_required
def camara_snapshot():
    """Captura un frame de la camara y lo analiza con pandas/numpy."""
    arr = camera.capture_snapshot()
    if arr is None:
        flash('No se pudo capturar. ¿La camara esta activa?', 'error')
        return redirect(url_for('camara_view'))

    filename = f'{uuid.uuid4().hex[:8]}_snapshot.png'
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    Image.fromarray(arr).save(filepath)

    stats_df = estadisticas_imagen(arr)
    stats_html = stats_df.to_html(classes='', index=False)

    filtro = request.args.get('filtro', 'normal')
    return render_template_string(CAMARA_TEMPLATE,
                                  filtro=filtro, snapshot_stats=stats_html,
                                  snapshot_file=filename)

@app.route('/camara/stop')
@login_required
def camara_stop():
    camera.stop()
    flash('Camara detenida', 'success')
    return redirect(url_for('dashboard'))

@app.route('/camara/stats')
@login_required
def camara_stats():
    """API JSON con estadisticas en tiempo real (para AJAX)."""
    return jsonify(camera.last_stats)

# ============================================================================
# RUTAS DE GRAFICOS (generados dinamicamente con matplotlib)
# ============================================================================

@app.route('/chart/histograma/<filename>')
@login_required
def chart_histograma(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return 'Imagen no encontrada', 404
    arr = imagen_a_array(filepath)
    buf = generar_histograma_rgb(arr)
    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/chart/paleta/<filename>')
@login_required
def chart_paleta(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        return 'Imagen no encontrada', 404
    n = int(request.args.get('n', 6))
    arr = imagen_a_array(filepath)
    paleta = extraer_paleta_color(arr, n_colores=n)
    buf = generar_grafico_paleta(paleta)
    return Response(buf.getvalue(), mimetype='image/png')

@app.route('/chart/comparacion')
@login_required
def chart_comparacion():
    img1 = request.args.get('img1', '')
    img2 = request.args.get('img2', '')
    path1 = os.path.join(UPLOAD_FOLDER, img1)
    path2 = os.path.join(UPLOAD_FOLDER, img2)
    if not os.path.exists(path1) or not os.path.exists(path2):
        return 'Imagenes no encontradas', 404
    arr1 = imagen_a_array(path1)
    arr2 = imagen_a_array(path2)
    buf = generar_grafico_comparacion(arr1, arr2)
    return Response(buf.getvalue(), mimetype='image/png')

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print('=' * 60)
    print('SEMANA 11 - Analisis de Imagen con Ciencia de Datos')
    print('http://localhost:5014')
    print('Credenciales: admin@ejemplo.com / admin123')
    print('=' * 60)
    app.run(debug=True, port=5014)
