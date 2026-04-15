# ============================================================================
# SEMANA 11 - PROYECTO 3: VISION ANALISIS DESKTOP (Tkinter)
# ============================================================================
# Aplicacion de escritorio para analisis de imagen con ciencia de datos.
# Misma logica que el proyecto web pero con interfaz Tkinter.
#
# Conceptos aplicados:
# - numpy: manipulacion de matrices de pixeles
# - pandas: tablas de estadisticas por canal RGB
# - matplotlib: histogramas embebidos en Tkinter (FigureCanvasTkAgg)
# - scipy: filtros Sobel, gaussiano
# - PIL: lectura/escritura de imagenes
# - opencv (cv2): captura de camara en tiempo real
# - Tkinter: interfaz grafica de escritorio
#
# COMO EJECUTAR:
# 1. pip install pillow numpy pandas matplotlib scipy scikit-learn opencv-python
# 2. python app.py
# ============================================================================

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from io import BytesIO

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from PIL import Image, ImageTk
from scipy import ndimage
from scipy.spatial.distance import cosine
import cv2

# ============================================================================
# FUNCIONES DE ANALISIS (mismas que el proyecto web)
# ============================================================================

def imagen_a_array(filepath):
    img = Image.open(filepath).convert('RGB')
    return np.array(img)

def estadisticas_imagen(arr):
    canales = {'Rojo': arr[:, :, 0], 'Verde': arr[:, :, 1], 'Azul': arr[:, :, 2]}
    stats = []
    for nombre, canal in canales.items():
        stats.append({
            'Canal': nombre,
            'Media': round(float(np.mean(canal)), 2),
            'Mediana': float(np.median(canal)),
            'Desv_Std': round(float(np.std(canal)), 2),
            'Min': int(np.min(canal)),
            'Max': int(np.max(canal)),
            'Q1': float(np.percentile(canal, 25)),
            'Q3': float(np.percentile(canal, 75)),
        })
    return pd.DataFrame(stats)

def aplicar_escala_grises(arr):
    return np.dot(arr[:, :, :3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)

def aplicar_deteccion_bordes(arr):
    gris = aplicar_escala_grises(arr).astype(float)
    sobel_x = ndimage.sobel(gris, axis=1)
    sobel_y = ndimage.sobel(gris, axis=0)
    bordes = np.hypot(sobel_x, sobel_y)
    bordes = (bordes / bordes.max() * 255).astype(np.uint8)
    return bordes

def aplicar_desenfoque(arr, sigma=3):
    resultado = np.zeros_like(arr)
    for i in range(3):
        resultado[:, :, i] = ndimage.gaussian_filter(arr[:, :, i], sigma=sigma)
    return resultado

def aplicar_ecualizacion(arr):
    resultado = np.zeros_like(arr)
    for i in range(3):
        canal = arr[:, :, i]
        hist, _ = np.histogram(canal.flatten(), 256, [0, 256])
        cdf = hist.cumsum()
        cdf_norm = (cdf - cdf.min()) * 255 / (cdf.max() - cdf.min())
        resultado[:, :, i] = cdf_norm[canal].astype(np.uint8)
    return resultado

def extraer_paleta_color(arr, n_colores=6):
    try:
        from sklearn.cluster import KMeans
    except ImportError:
        pixeles = arr.reshape(-1, 3)
        indices = np.random.choice(len(pixeles), min(n_colores, len(pixeles)), replace=False)
        return pixeles[indices]

    pixeles = arr.reshape(-1, 3).astype(float)
    if len(pixeles) > 10000:
        indices = np.random.choice(len(pixeles), 10000, replace=False)
        muestra = pixeles[indices]
    else:
        muestra = pixeles
    kmeans = KMeans(n_clusters=n_colores, random_state=42, n_init=10)
    kmeans.fit(muestra)
    return kmeans.cluster_centers_.astype(int)

def comparar_imagenes(arr1, arr2):
    size = (min(arr1.shape[1], arr2.shape[1]), min(arr1.shape[0], arr2.shape[0]))
    a1 = np.array(Image.fromarray(arr1).resize(size)).astype(float)
    a2 = np.array(Image.fromarray(arr2).resize(size)).astype(float)
    mse = float(np.mean((a1 - a2) ** 2))
    hist1 = np.histogram(a1.flatten(), bins=64, range=(0, 256))[0].astype(float)
    hist2 = np.histogram(a2.flatten(), bins=64, range=(0, 256))[0].astype(float)
    dist_cos = float(cosine(hist1, hist2))
    similitud = round((1 - dist_cos) * 100, 2)
    correlaciones = {}
    for i, nombre in enumerate(['Rojo', 'Verde', 'Azul']):
        corr = float(np.corrcoef(a1[:, :, i].flatten(), a2[:, :, i].flatten())[0, 1])
        correlaciones[nombre] = round(corr, 4)
    return {'mse': round(mse, 2), 'similitud': similitud, 'correlaciones': correlaciones}

# ============================================================================
# APLICACION TKINTER
# ============================================================================

class VisionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Vision Analisis Desktop - Semana 11')
        self.geometry('1100x750')
        self.configure(bg='#1a1a2e')

        self.current_arr = None
        self.current_path = None
        self.compare_arr = None

        self._crear_ui()

    def _crear_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#1a1a2e')
        style.configure('TNotebook.Tab', background='#16213e', foreground='white',
                        padding=[12, 6], font=('Segoe UI', 10))
        style.map('TNotebook.Tab', background=[('selected', '#0f3460')])
        style.configure('TFrame', background='#1a1a2e')
        style.configure('TLabel', background='#1a1a2e', foreground='white',
                        font=('Segoe UI', 10))
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'),
                        foreground='#e94560')
        style.configure('TButton', font=('Segoe UI', 10), padding=6)

        # Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        self.tab_camara = ttk.Frame(self.notebook)
        self.tab_analisis = ttk.Frame(self.notebook)
        self.tab_filtros = ttk.Frame(self.notebook)
        self.tab_comparar = ttk.Frame(self.notebook)
        self.tab_paleta = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_camara, text='  Camara  ')
        self.notebook.add(self.tab_analisis, text='  Analisis  ')
        self.notebook.add(self.tab_filtros, text='  Filtros  ')
        self.notebook.add(self.tab_comparar, text='  Comparar  ')
        self.notebook.add(self.tab_paleta, text='  Paleta  ')

        self._crear_tab_camara()
        self._crear_tab_analisis()
        self._crear_tab_filtros()
        self._crear_tab_comparar()
        self._crear_tab_paleta()

    # ----- TAB CAMARA EN TIEMPO REAL -----
    def _crear_tab_camara(self):
        frame = self.tab_camara
        self.cam_cap = None
        self.cam_running = False
        self.cam_filtro = tk.StringVar(value='normal')

        top = ttk.Frame(frame)
        top.pack(fill='x', padx=10, pady=5)
        ttk.Label(top, text='Camara en Tiempo Real', style='Header.TLabel').pack(side='left')

        controls = ttk.Frame(frame)
        controls.pack(fill='x', padx=10)
        ttk.Button(controls, text='Iniciar', command=self._cam_start).pack(side='left', padx=3)
        ttk.Button(controls, text='Detener', command=self._cam_stop).pack(side='left', padx=3)
        ttk.Button(controls, text='Capturar Foto', command=self._cam_snapshot).pack(side='left', padx=3)

        filtros = [('Normal', 'normal'), ('Grises', 'grises'), ('Bordes', 'bordes'),
                   ('Desenfoque', 'desenfoque'), ('Ecualizar', 'ecualizar')]
        for texto, valor in filtros:
            ttk.Radiobutton(controls, text=texto, variable=self.cam_filtro,
                           value=valor).pack(side='left', padx=4)

        self.lbl_cam_video = ttk.Label(frame, text='Presiona Iniciar para activar la camara')
        self.lbl_cam_video.pack(pady=10)

        self.lbl_cam_stats = ttk.Label(frame, text='', font=('Consolas', 9), justify='left')
        self.lbl_cam_stats.pack(padx=10, pady=5)

        self.fig_cam = Figure(figsize=(9, 2.5), facecolor='#1a1a2e')
        self.canvas_cam = FigureCanvasTkAgg(self.fig_cam, frame)
        self.canvas_cam.get_tk_widget().pack(fill='x', padx=10, pady=5)

    def _cam_start(self):
        if self.cam_running:
            return
        self.cam_cap = cv2.VideoCapture(0)
        if not self.cam_cap.isOpened():
            messagebox.showerror('Error', 'No se pudo abrir la camara')
            return
        self.cam_running = True
        self._cam_update()

    def _cam_stop(self):
        self.cam_running = False
        if self.cam_cap:
            self.cam_cap.release()
            self.cam_cap = None
        self.lbl_cam_video.configure(image='', text='Camara detenida')

    def _cam_update(self):
        if not self.cam_running or not self.cam_cap:
            return
        ret, frame = self.cam_cap.read()
        if not ret:
            self.after(30, self._cam_update)
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Estadisticas en tiempo real
        stats_lines = []
        for i, nombre in enumerate(['Rojo', 'Verde', 'Azul']):
            canal = frame_rgb[:, :, i]
            stats_lines.append(f'{nombre}: media={np.mean(canal):.1f}  std={np.std(canal):.1f}')
        self.lbl_cam_stats.configure(text='  |  '.join(stats_lines))

        # Aplicar filtro
        filtro = self.cam_filtro.get()
        if filtro == 'grises':
            res = aplicar_escala_grises(frame_rgb)
            display = np.stack([res]*3, axis=2)
        elif filtro == 'bordes':
            res = aplicar_deteccion_bordes(frame_rgb)
            display = np.stack([res]*3, axis=2)
        elif filtro == 'desenfoque':
            display = aplicar_desenfoque(frame_rgb, sigma=5)
        elif filtro == 'ecualizar':
            display = aplicar_ecualizacion(frame_rgb)
        else:
            display = frame_rgb

        # Mostrar en label
        img = Image.fromarray(display)
        img.thumbnail((640, 480))
        photo = ImageTk.PhotoImage(img)
        self.lbl_cam_video.configure(image=photo, text='')
        self.lbl_cam_video.image = photo

        # Actualizar histograma cada 10 frames
        if not hasattr(self, '_cam_frame_count'):
            self._cam_frame_count = 0
        self._cam_frame_count += 1
        if self._cam_frame_count % 10 == 0:
            self._cam_update_histogram(frame_rgb)

        self.after(30, self._cam_update)

    def _cam_update_histogram(self, arr):
        self.fig_cam.clear()
        colores = ['#ff4444', '#44ff44', '#4444ff']
        nombres = ['Rojo', 'Verde', 'Azul']
        for i in range(3):
            ax = self.fig_cam.add_subplot(1, 3, i + 1)
            datos = arr[:, :, i].flatten()
            ax.hist(datos, bins=32, color=colores[i], alpha=0.8, edgecolor='none')
            ax.set_title(nombres[i], color='white', fontsize=9)
            ax.set_facecolor('#16213e')
            ax.tick_params(colors='white', labelsize=6)
            ax.set_xlim(0, 255)
            for spine in ax.spines.values():
                spine.set_color('#333')
        self.fig_cam.tight_layout()
        self.canvas_cam.draw()

    def _cam_snapshot(self):
        if not self.cam_running or not self.cam_cap:
            messagebox.showwarning('Aviso', 'Inicia la camara primero')
            return
        ret, frame = self.cam_cap.read()
        if not ret:
            return
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Guardar y abrir en tab de analisis
        self.current_arr = frame_rgb
        self.current_path = 'camara'
        self._mostrar_preview(frame_rgb, self.lbl_preview, max_size=300)
        self._mostrar_estadisticas()
        self._mostrar_histograma()
        self.notebook.select(self.tab_analisis)
        messagebox.showinfo('Captura', 'Foto capturada y enviada a la pestana Analisis')

    # ----- TAB ANALISIS -----
    def _crear_tab_analisis(self):
        frame = self.tab_analisis

        top = ttk.Frame(frame)
        top.pack(fill='x', padx=10, pady=5)
        ttk.Label(top, text='Analisis de Imagen', style='Header.TLabel').pack(side='left')
        ttk.Button(top, text='Abrir Imagen', command=self._abrir_imagen).pack(side='right')

        content = ttk.Frame(frame)
        content.pack(fill='both', expand=True, padx=10, pady=5)

        # Imagen preview
        self.lbl_preview = ttk.Label(content, text='Abre una imagen para comenzar')
        self.lbl_preview.pack(pady=10)

        # Stats
        self.lbl_stats = ttk.Label(content, text='', justify='left', font=('Consolas', 9))
        self.lbl_stats.pack(pady=5)

        # Histograma
        self.fig_hist = Figure(figsize=(9, 3), facecolor='#1a1a2e')
        self.canvas_hist = FigureCanvasTkAgg(self.fig_hist, content)
        self.canvas_hist.get_tk_widget().pack(fill='x', pady=5)

    def _abrir_imagen(self):
        path = filedialog.askopenfilename(
            filetypes=[('Imagenes', '*.png *.jpg *.jpeg *.bmp *.gif')])
        if not path:
            return
        self.current_path = path
        self.current_arr = imagen_a_array(path)
        self._mostrar_preview(self.current_arr, self.lbl_preview, max_size=300)
        self._mostrar_estadisticas()
        self._mostrar_histograma()

    def _mostrar_preview(self, arr, label, max_size=300):
        img = Image.fromarray(arr if len(arr.shape) == 3 else np.stack([arr]*3, axis=2))
        img.thumbnail((max_size, max_size))
        photo = ImageTk.PhotoImage(img)
        label.configure(image=photo, text='')
        label.image = photo

    def _mostrar_estadisticas(self):
        if self.current_arr is None:
            return
        df = estadisticas_imagen(self.current_arr)
        h, w = self.current_arr.shape[:2]
        texto = f'Dimensiones: {w}x{h} ({w*h:,} pixeles)\n\n{df.to_string(index=False)}'
        self.lbl_stats.configure(text=texto)

    def _mostrar_histograma(self):
        if self.current_arr is None:
            return
        self.fig_hist.clear()
        colores = ['#ff4444', '#44ff44', '#4444ff']
        nombres = ['Rojo', 'Verde', 'Azul']
        for i in range(3):
            ax = self.fig_hist.add_subplot(1, 3, i + 1)
            datos = self.current_arr[:, :, i].flatten()
            ax.hist(datos, bins=64, color=colores[i], alpha=0.8, edgecolor='none')
            ax.set_title(nombres[i], color='white', fontsize=10)
            ax.set_facecolor('#16213e')
            ax.tick_params(colors='white', labelsize=7)
            ax.set_xlim(0, 255)
            for spine in ax.spines.values():
                spine.set_color('#333')
        self.fig_hist.tight_layout()
        self.canvas_hist.draw()

    # ----- TAB FILTROS -----
    def _crear_tab_filtros(self):
        frame = self.tab_filtros

        top = ttk.Frame(frame)
        top.pack(fill='x', padx=10, pady=5)
        ttk.Label(top, text='Filtros y Transformaciones', style='Header.TLabel').pack(side='left')

        controls = ttk.Frame(frame)
        controls.pack(fill='x', padx=10)
        ttk.Button(controls, text='Abrir Imagen', command=self._filtro_abrir).pack(side='left', padx=3)

        self.filtro_var = tk.StringVar(value='grises')
        filtros = [('Escala de Grises', 'grises'), ('Bordes (Sobel)', 'bordes'),
                   ('Desenfoque', 'desenfoque'), ('Ecualizar', 'ecualizar')]
        for texto, valor in filtros:
            ttk.Radiobutton(controls, text=texto, variable=self.filtro_var,
                           value=valor).pack(side='left', padx=5)
        ttk.Button(controls, text='Aplicar', command=self._aplicar_filtro).pack(side='right', padx=3)

        content = ttk.Frame(frame)
        content.pack(fill='both', expand=True, padx=10, pady=5)

        left = ttk.Frame(content)
        left.pack(side='left', fill='both', expand=True)
        ttk.Label(left, text='Original').pack()
        self.lbl_filtro_orig = ttk.Label(left, text='')
        self.lbl_filtro_orig.pack(pady=5)

        right = ttk.Frame(content)
        right.pack(side='right', fill='both', expand=True)
        ttk.Label(right, text='Resultado').pack()
        self.lbl_filtro_res = ttk.Label(right, text='')
        self.lbl_filtro_res.pack(pady=5)

        self.lbl_filtro_stats = ttk.Label(frame, text='', font=('Consolas', 9), justify='left')
        self.lbl_filtro_stats.pack(padx=10, pady=5)

        self.filtro_arr = None

    def _filtro_abrir(self):
        path = filedialog.askopenfilename(
            filetypes=[('Imagenes', '*.png *.jpg *.jpeg *.bmp *.gif')])
        if not path:
            return
        self.filtro_arr = imagen_a_array(path)
        self._mostrar_preview(self.filtro_arr, self.lbl_filtro_orig, max_size=280)
        self.lbl_filtro_res.configure(image='', text='Selecciona un filtro y presiona Aplicar')

    def _aplicar_filtro(self):
        if self.filtro_arr is None:
            messagebox.showwarning('Aviso', 'Primero abre una imagen')
            return
        filtro = self.filtro_var.get()
        if filtro == 'grises':
            res = aplicar_escala_grises(self.filtro_arr)
        elif filtro == 'bordes':
            res = aplicar_deteccion_bordes(self.filtro_arr)
        elif filtro == 'desenfoque':
            res = aplicar_desenfoque(self.filtro_arr)
        elif filtro == 'ecualizar':
            res = aplicar_ecualizacion(self.filtro_arr)
        else:
            res = self.filtro_arr

        self._mostrar_preview(res, self.lbl_filtro_res, max_size=280)

        if len(res.shape) == 3:
            df = estadisticas_imagen(res)
        else:
            df = pd.DataFrame([{
                'Canal': 'Gris', 'Media': round(float(np.mean(res)), 2),
                'Mediana': float(np.median(res)),
                'Desv_Std': round(float(np.std(res)), 2),
                'Min': int(np.min(res)), 'Max': int(np.max(res)),
            }])
        self.lbl_filtro_stats.configure(text=f'Estadisticas resultado:\n{df.to_string(index=False)}')

    # ----- TAB COMPARAR -----
    def _crear_tab_comparar(self):
        frame = self.tab_comparar

        top = ttk.Frame(frame)
        top.pack(fill='x', padx=10, pady=5)
        ttk.Label(top, text='Comparar Imagenes', style='Header.TLabel').pack(side='left')

        controls = ttk.Frame(frame)
        controls.pack(fill='x', padx=10)
        ttk.Button(controls, text='Imagen 1', command=lambda: self._cmp_abrir(1)).pack(side='left', padx=3)
        ttk.Button(controls, text='Imagen 2', command=lambda: self._cmp_abrir(2)).pack(side='left', padx=3)
        ttk.Button(controls, text='Comparar', command=self._ejecutar_comparacion).pack(side='right', padx=3)

        content = ttk.Frame(frame)
        content.pack(fill='both', expand=True, padx=10, pady=5)

        left = ttk.Frame(content)
        left.pack(side='left', fill='both', expand=True)
        self.lbl_cmp1 = ttk.Label(left, text='Imagen 1')
        self.lbl_cmp1.pack(pady=5)

        right = ttk.Frame(content)
        right.pack(side='right', fill='both', expand=True)
        self.lbl_cmp2 = ttk.Label(right, text='Imagen 2')
        self.lbl_cmp2.pack(pady=5)

        self.lbl_cmp_result = ttk.Label(frame, text='', font=('Consolas', 10), justify='left')
        self.lbl_cmp_result.pack(padx=10, pady=5)

        self.cmp_arr1 = None
        self.cmp_arr2 = None

    def _cmp_abrir(self, num):
        path = filedialog.askopenfilename(
            filetypes=[('Imagenes', '*.png *.jpg *.jpeg *.bmp *.gif')])
        if not path:
            return
        arr = imagen_a_array(path)
        if num == 1:
            self.cmp_arr1 = arr
            self._mostrar_preview(arr, self.lbl_cmp1, max_size=250)
        else:
            self.cmp_arr2 = arr
            self._mostrar_preview(arr, self.lbl_cmp2, max_size=250)

    def _ejecutar_comparacion(self):
        if self.cmp_arr1 is None or self.cmp_arr2 is None:
            messagebox.showwarning('Aviso', 'Carga ambas imagenes primero')
            return
        m = comparar_imagenes(self.cmp_arr1, self.cmp_arr2)
        texto = (
            f"Similitud (coseno): {m['similitud']}%\n"
            f"Error Cuadratico Medio: {m['mse']}\n"
            f"Correlacion Rojo:  {m['correlaciones']['Rojo']}\n"
            f"Correlacion Verde: {m['correlaciones']['Verde']}\n"
            f"Correlacion Azul:  {m['correlaciones']['Azul']}"
        )
        self.lbl_cmp_result.configure(text=texto)

    # ----- TAB PALETA -----
    def _crear_tab_paleta(self):
        frame = self.tab_paleta

        top = ttk.Frame(frame)
        top.pack(fill='x', padx=10, pady=5)
        ttk.Label(top, text='Paleta de Colores (K-Means)', style='Header.TLabel').pack(side='left')

        controls = ttk.Frame(frame)
        controls.pack(fill='x', padx=10)
        ttk.Button(controls, text='Abrir Imagen', command=self._paleta_abrir).pack(side='left', padx=3)

        ttk.Label(controls, text='Colores:').pack(side='left', padx=(10, 3))
        self.paleta_n = tk.IntVar(value=6)
        spin = ttk.Spinbox(controls, from_=2, to=12, textvariable=self.paleta_n, width=4)
        spin.pack(side='left')
        ttk.Button(controls, text='Extraer', command=self._extraer_paleta).pack(side='right', padx=3)

        self.lbl_paleta_img = ttk.Label(frame, text='')
        self.lbl_paleta_img.pack(pady=5)

        self.fig_paleta = Figure(figsize=(9, 2), facecolor='#1a1a2e')
        self.canvas_paleta = FigureCanvasTkAgg(self.fig_paleta, frame)
        self.canvas_paleta.get_tk_widget().pack(fill='x', padx=10, pady=5)

        self.lbl_paleta_stats = ttk.Label(frame, text='', font=('Consolas', 9), justify='left')
        self.lbl_paleta_stats.pack(padx=10, pady=5)

        self.paleta_arr = None

    def _paleta_abrir(self):
        path = filedialog.askopenfilename(
            filetypes=[('Imagenes', '*.png *.jpg *.jpeg *.bmp *.gif')])
        if not path:
            return
        self.paleta_arr = imagen_a_array(path)
        self._mostrar_preview(self.paleta_arr, self.lbl_paleta_img, max_size=250)

    def _extraer_paleta(self):
        if self.paleta_arr is None:
            messagebox.showwarning('Aviso', 'Primero abre una imagen')
            return
        n = self.paleta_n.get()
        paleta = extraer_paleta_color(self.paleta_arr, n_colores=n)

        self.fig_paleta.clear()
        ax = self.fig_paleta.add_subplot(111)
        for i, color in enumerate(paleta):
            color_norm = [c / 255.0 for c in color]
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color_norm))
            hex_c = '#{:02x}{:02x}{:02x}'.format(*color)
            ax.text(i + 0.5, 0.5, hex_c, ha='center', va='center', fontsize=7,
                    fontweight='bold', color='white' if sum(color) < 380 else 'black')
        ax.set_xlim(0, len(paleta))
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Colores Dominantes', color='white', fontsize=11)
        ax.set_facecolor('#1a1a2e')
        self.fig_paleta.tight_layout()
        self.canvas_paleta.draw()

        df = estadisticas_imagen(self.paleta_arr)
        self.lbl_paleta_stats.configure(text=df.to_string(index=False))

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print('=' * 60)
    print('SEMANA 11 - Vision Analisis Desktop')
    print('=' * 60)
    app = VisionApp()

    def on_close():
        app._cam_stop()
        app.destroy()

    app.protocol('WM_DELETE_WINDOW', on_close)
    app.mainloop()
