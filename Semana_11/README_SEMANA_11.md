# ============================================================================
# SEMANA 11: Ciencia de Datos con Python
# ============================================================================

## Objetivo

La Semana 11 introduce los **fundamentos de ciencia de datos** aplicados a un
contexto de backend. El estudiante aprendera a usar las bibliotecas mas
importantes del ecosistema de datos de Python (pandas, numpy, matplotlib, scipy)
para analizar, visualizar y predecir datos desde una aplicacion Flask.

| Semana  | Concepto                          | Aplicado en el proyecto                 |
|---------|-----------------------------------|-----------------------------------------|
| 1-3     | Variables, funciones, logica      | Logica de negocio, calculos estadisticos|
| 4-5     | Estructuras de datos, POO         | Modelos SQLAlchemy, DataFrames pandas   |
| 6-7     | Modulos, archivos, SQL           | Queries, exportacion CSV, joins         |
| 8       | CRUD con Flask                    | Gestion de reportes y ventas            |
| 9       | Autenticacion y seguridad        | Login, sesiones, roles                  |
| 10      | Proyecto integrador               | Integracion de todos los conceptos      |
| **11**  | **Ciencia de datos**             | **Analisis, graficos, predicciones**    |

---

## Conceptos Clave de la Semana

### Tabla de Conceptos

| Concepto             | Que es                                              | Ejemplo en el proyecto                            |
|----------------------|-----------------------------------------------------|---------------------------------------------------|
| **pandas**           | Biblioteca para manipular datos tabulares            | `df = pd.DataFrame(...)`, filtros, agrupaciones   |
| **DataFrame**        | Tabla de datos con filas y columnas                  | Convertir ventas de SQLAlchemy a DataFrame         |
| **Series**           | Una columna de un DataFrame                          | `df['total']` → Serie con los totales              |
| **numpy**            | Biblioteca para calculo numerico eficiente           | `np.mean()`, `np.std()`, arrays numericos          |
| **matplotlib**       | Biblioteca para crear graficos                       | Graficos de barras, lineas, pastel                |
| **Media (mean)**     | Promedio de un conjunto de datos                     | Ticket promedio de ventas                          |
| **Mediana (median)** | Valor central al ordenar los datos                   | Mediana de ventas por region                       |
| **Desv. estandar**   | Que tan dispersos estan los datos                    | Variabilidad en las ventas mensuales               |
| **Correlacion**      | Relacion lineal entre dos variables                  | Correlacion cantidad-total                         |
| **Regresion lineal** | Modelo para predecir valores futuros                 | Prediccion de ventas para los proximos meses       |
| **groupby()**        | Agrupar datos por una columna y calcular algo        | Ventas por categoria, por region                   |
| **pivot_table()**    | Tabla cruzada (filas x columnas)                     | Ventas por mes y categoria                         |
| **value_counts()**   | Contar frecuencias de valores unicos                 | Productos mas vendidos                             |
| **describe()**       | Resumen estadistico automatico                       | Media, min, max, cuartiles de todas las columnas   |
| **iloc / loc**       | Acceder a filas/columnas por posicion o nombre       | Seleccionar top 10 productos                       |
| **merge()**          | Combinar dos DataFrames (como SQL JOIN)              | Unir ventas con informacion de productos           |
| **resample()**       | Re-agrupar serie temporal por periodo                | Ventas diarias → mensuales                         |
| **BytesIO**          | Buffer en memoria para archivos                      | Guardar graficos matplotlib sin archivo fisico     |
| **scipy.stats**      | Funciones estadisticas avanzadas                     | Regresion lineal con `linregress()`                |
| **PIL / Pillow**     | Biblioteca para lectura y manipulacion de imagenes   | Abrir, redimensionar, convertir imagenes           |
| **ndimage (scipy)**  | Filtros y operaciones sobre imagenes como arrays     | Sobel, gaussiano, deteccion de bordes              |
| **K-Means**          | Algoritmo de clustering para agrupar datos           | Extraer paleta de colores dominantes               |

---

## Proyectos de la Semana

### Proyecto 1: Dashboard de Analisis de Ventas

**Carpeta:** `01_analisis_ventas/`

**Ejecutar:** `python app.py` → http://localhost:5013

**Credenciales:** admin@ejemplo.com / admin123

Una aplicacion web Flask que analiza datos de ventas usando pandas, genera
graficos con matplotlib y ofrece predicciones con regresion lineal.

**Funcionalidades:**
1. Dashboard con KPIs - Total ventas, ticket promedio, top productos, tendencias
2. Graficos - Ventas por mes, por categoria, por region, top clientes
3. Filtros avanzados - Por rango de fechas, categoria, region
4. Exportar CSV - Descargar datos filtrados en formato CSV
5. Estadisticas - Media, mediana, desviacion estandar, correlaciones
6. Prediccion - Regresion lineal simple para pronostico de ventas

---

### Proyecto 2: Analisis de Imagen con Ciencia de Datos

**Carpeta:** `02_vision_analisis/`

**Ejecutar:** `python app.py` → http://localhost:5014

**Credenciales:** admin@ejemplo.com / admin123

Una aplicacion web Flask que aplica tecnicas de ciencia de datos al analisis
de imagenes: histogramas RGB, filtros con scipy, comparacion estadistica y
extraccion de paletas de color con K-Means.

**Funcionalidades:**
1. **Estadisticas por canal RGB** - Media, mediana, desviacion estandar, cuartiles con pandas
2. **Histogramas de distribucion** - Visualizacion de intensidad por canal con matplotlib
3. **Filtros** - Escala de grises (pesos perceptuales), bordes (Sobel), desenfoque (gaussiano), ecualizacion
4. **Comparacion de imagenes** - MSE, distancia coseno, correlacion por canal
5. **Paleta de colores** - Extraccion de colores dominantes con K-Means (scikit-learn)

**Conceptos de ciencia de datos aplicados:**

| Concepto                | Aplicacion en vision                              |
|-------------------------|---------------------------------------------------|
| numpy arrays            | Matrices de pixeles (alto x ancho x 3 canales)   |
| pandas DataFrame        | Tabla de estadisticas por canal RGB               |
| matplotlib histograma   | Distribucion de intensidad de color               |
| scipy.ndimage           | Filtros Sobel y gaussiano sobre la matriz         |
| scipy.spatial.distance  | Distancia coseno entre histogramas                |
| np.corrcoef             | Correlacion entre canales de dos imagenes         |
| sklearn KMeans          | Clustering de pixeles para paleta de color        |
| np.percentile           | Cuartiles Q1, Q3 e IQR por canal                 |

---

### Proyecto 3: Vision Analisis Desktop (Tkinter)

**Carpeta:** `03_desktop_vision/`

**Ejecutar:** `python app.py`

Misma logica de analisis de imagen que el proyecto web, pero con interfaz
de escritorio usando Tkinter. Demuestra que las mismas tecnicas de ciencia
de datos funcionan independientemente de la interfaz.

**Funcionalidades:**
1. Analisis de imagen con histogramas embebidos (FigureCanvasTkAgg)
2. Filtros y transformaciones con vista lado a lado
3. Comparacion de imagenes con metricas
4. Extraccion de paleta de colores

---

## Dependencias

```bash
pip install flask sqlalchemy werkzeug pandas numpy matplotlib scipy scikit-learn pillow
```

---

## Conceptos Estadisticos Esenciales

### Media (Promedio)
Suma de todos los valores dividida por la cantidad.
```python
media = df['total'].mean()
# En vision: intensidad promedio de un canal
media_rojo = np.mean(imagen[:, :, 0])
```

### Mediana
Valor central cuando los datos estan ordenados. Menos afectada por valores extremos.
```python
mediana = df['total'].median()
```

### Desviacion Estandar
Mide que tan dispersos estan los datos respecto a la media.
```python
desviacion = df['total'].std()
# En vision: contraste de un canal
contraste = np.std(imagen[:, :, 0])
```

### Correlacion
Mide la relacion lineal entre dos variables (-1 a 1).
```python
correlacion = df['cantidad'].corr(df['total'])
# En vision: similitud entre canales de dos imagenes
corr = np.corrcoef(canal1.flatten(), canal2.flatten())[0, 1]
```

### Cuartiles
Dividen los datos en 4 partes iguales.
```python
q1 = df['total'].quantile(0.25)
q3 = df['total'].quantile(0.75)
```

---

## Preguntas de Repaso

1. ¿Que es un DataFrame y en que se diferencia de una lista de diccionarios?
2. ¿Para que sirve `groupby()` en pandas?
3. ¿Cual es la diferencia entre `mean()` y `median()`? ¿Cuando conviene usar cada una?
4. ¿Por que usamos `matplotlib.use('Agg')` en un servidor Flask?
5. ¿Que indica un coeficiente de correlacion de 0.95?
6. ¿Que es una regresion lineal y para que la usamos aqui?
7. ¿Como se convierte una query de SQLAlchemy a un DataFrame de pandas?
8. ¿Que hace `BytesIO` y por que lo usamos para generar graficos?
9. ¿Que diferencia hay entre `iloc` y `loc`?
10. ¿Como se exportan datos de un DataFrame a CSV?
11. ¿Por que una imagen es un array de numpy con 3 dimensiones?
12. ¿Que mide la distancia coseno entre dos histogramas de imagen?
13. ¿Como funciona K-Means para extraer una paleta de colores?
14. ¿Que es un filtro Sobel y por que detecta bordes?
15. ¿Que ventaja tiene scipy.ndimage sobre aplicar filtros manualmente?

---

## Notas del Instructor

- Esta semana marca la transicion de "construir aplicaciones CRUD" a "analizar
  datos generados por esas aplicaciones".
- Los estudiantes deben entender que la ciencia de datos en backend se usa para:
  - Dashboards administrativos con metricas de negocio
  - Reportes automatizados
  - Predicciones simples para toma de decisiones
  - Analisis de imagen como caso practico de numpy/scipy
  - Deteccion de patrones en datos de usuarios/ventas
- El analisis de imagen demuestra que numpy, pandas y matplotlib no solo sirven
  para datos tabulares: una imagen es simplemente una matriz numerica.
- No se espera que dominen machine learning avanzado, sino que comprendan las
  herramientas basicas y como integrarlas en una aplicacion web.
