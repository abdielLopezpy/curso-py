# ============================================================================
# EXAMEN - SEMANA 11: Ciencia de Datos con Python
# ============================================================================

**Nombre del estudiante:** _______________________________________________

**Fecha:** _______________________________________________

---

## Instrucciones

- Responda cada pregunta en el espacio indicado.
- Sea claro y especifico. Cuando diga "muestra un ejemplo", escriba codigo Python.
- Duracion estimada: 60 minutos.

---

## PARTE A: pandas - Fundamentos (30 pts)

### Pregunta 1 (3 pts)
¿Que es pandas y para que se usa en Python? ¿Cual es la diferencia principal entre un DataFrame y una Serie?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 2 (3 pts)
¿Como se crea un DataFrame a partir de una lista de diccionarios? Escribe un ejemplo con al menos 3 filas y 3 columnas.

**Tu respuesta:**
```python
(escribe aqui)


```

---

### Pregunta 3 (3 pts)
Explica que hace el siguiente codigo y que resultado produce:
```python
df.groupby('categoria')['total'].sum().sort_values(ascending=False)
```

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 4 (3 pts)
¿Cual es la diferencia entre `df.loc[0:5]` y `df.iloc[0:5]`? ¿En que situaciones usarias cada uno?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 5 (3 pts)
¿Que hace `df.describe()`? Lista al menos 5 estadisticas que devuelve y explica cada una brevemente.

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 6 (3 pts)
¿Como se filtran las filas de un DataFrame donde la columna 'precio' sea mayor a 100 y la columna 'categoria' sea igual a 'Electronica'? Escribe el codigo.

**Tu respuesta:**
```python
(escribe aqui)


```

---

### Pregunta 7 (3 pts)
¿Que es `value_counts()` y para que sirve? Da un ejemplo de su uso con datos de ventas.

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 8 (3 pts)
Explica que hace el metodo `merge()` en pandas. ¿A que operacion de SQL es equivalente? Escribe un ejemplo.

**Tu respuesta:**
```python
(escribe aqui)


```

---

### Pregunta 9 (3 pts)
¿Como se convierte una columna de texto con fechas a tipo datetime en pandas? ¿Por que es importante hacerlo?

**Tu respuesta:**
```python
(escribe aqui)


```

---

### Pregunta 10 (3 pts)
¿Que es una pivot_table? ¿En que se diferencia de groupby? Escribe un ejemplo que muestre ventas por mes y categoria.

**Tu respuesta:**
```python
(escribe aqui)


```

---

## PARTE B: numpy y Estadistica (20 pts)

### Pregunta 11 (4 pts)
¿Que es numpy y por que es mas eficiente que las listas nativas de Python para calculos numericos?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 12 (4 pts)
Explica la diferencia entre **media** y **mediana**. Si tienes las ventas [100, 150, 200, 5000, 180], ¿cual seria la media y cual la mediana? ¿Cual representa mejor los datos y por que?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 13 (4 pts)
¿Que es la desviacion estandar? Si un conjunto de datos tiene desviacion estandar de 5 y otro de 500, ¿que nos dice eso sobre cada conjunto?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 14 (4 pts)
¿Que es la correlacion entre dos variables? Si la correlacion entre "cantidad" y "total" es 0.95, ¿que significa? ¿Y si fuera -0.80?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 15 (4 pts)
¿Que son los cuartiles (Q1, Q2, Q3)? ¿Como se relacionan con los percentiles? ¿Para que sirve el rango intercuartilico (IQR)?

**Tu respuesta:**
```
(escribe aqui)


```

---

## PARTE C: matplotlib y Visualizacion (20 pts)

### Pregunta 16 (4 pts)
¿Por que se usa `matplotlib.use('Agg')` en una aplicacion Flask? ¿Que pasaria si no lo usamos?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 17 (4 pts)
Escribe el codigo completo para crear un grafico de barras con matplotlib que muestre las ventas de 5 productos. Incluye titulo, etiquetas de ejes y colores.

**Tu respuesta:**
```python
(escribe aqui)


```

---

### Pregunta 18 (4 pts)
¿Que es BytesIO y como se usa para servir graficos como imagenes PNG en Flask? Escribe el codigo de una ruta Flask que devuelva un grafico.

**Tu respuesta:**
```python
(escribe aqui)


```

---

### Pregunta 19 (4 pts)
¿Cual es la diferencia entre un grafico de barras, uno de lineas y uno de pastel? ¿En que situacion usarias cada uno para analizar datos de ventas?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 20 (4 pts)
¿Que es `plt.subplots()` y como se usa para crear multiples graficos en una sola figura? Escribe un ejemplo con 2 graficos lado a lado.

**Tu respuesta:**
```python
(escribe aqui)


```

---

## PARTE D: Analisis de Imagen con Ciencia de Datos (15 pts)

### Pregunta 21 (3 pts)
¿Por que una imagen digital es un array de numpy con 3 dimensiones (alto x ancho x canales)? ¿Que representa cada valor numerico en el array?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 22 (3 pts)
Explica como se calcula la media y desviacion estandar de un canal de color (ej. canal Rojo). ¿Que nos dice una desviacion estandar alta vs baja sobre la imagen?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 23 (3 pts)
¿Que es un filtro Sobel y como detecta bordes en una imagen? ¿Por que se usa `scipy.ndimage.sobel()` en lugar de hacerlo manualmente?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 24 (3 pts)
Explica como funciona K-Means para extraer una paleta de colores dominantes de una imagen. ¿Por que se usa una muestra de pixeles en lugar de todos?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 25 (3 pts)
¿Como se comparan dos imagenes usando distancia coseno entre histogramas? ¿Que indica una similitud de 95% vs una de 30%?

**Tu respuesta:**
```
(escribe aqui)


```

---

## PARTE E: Integracion con Flask (15 pts)

### Pregunta 26 (3 pts)
¿Como se convierten los resultados de una query SQLAlchemy a un DataFrame de pandas? Escribe el codigo.

**Tu respuesta:**
```python
(escribe aqui)


```

---

### Pregunta 27 (3 pts)
¿Por que es importante usar `plt.close(fig)` despues de generar un grafico en una aplicacion web? ¿Que problema causa no hacerlo?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 28 (3 pts)
Explica como se implementa la exportacion a CSV desde Flask. ¿Que headers HTTP son necesarios para que el navegador descargue el archivo?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 29 (3 pts)
¿Que es un KPI (Key Performance Indicator)? Lista 4 KPIs que tendria un dashboard de ventas y como se calcularian con pandas.

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 30 (3 pts)
¿Como se sirve una imagen procesada (ej. con filtro aplicado) directamente desde Flask sin guardarla en disco? Escribe el codigo usando BytesIO.

**Tu respuesta:**
```python
(escribe aqui)


```

---

## PARTE F: Preguntas de Analisis (Bonus - 10 pts)

### Pregunta 31 (3 pts)
Si la media de ventas es $500 pero la mediana es $150, ¿que nos dice eso sobre la distribucion de las ventas? ¿Que tipo de sesgo tienen los datos?

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 32 (3 pts)
Tienes dos imagenes y quieres determinar si son "similares". Explica al menos 3 metricas que podrias usar y que mide cada una.

**Tu respuesta:**
```
(escribe aqui)


```

---

### Pregunta 33 (4 pts)
Tienes un DataFrame con 10,000 ventas. El gerente quiere saber: "¿Cual es el mejor dia de la semana para ventas?" Escribe el codigo completo en pandas para responder esta pregunta, incluyendo la creacion de un grafico.

**Tu respuesta:**
```python
(escribe aqui)


```

---

## Tabla de Calificacion

| Parte | Tema                                    | Puntos | Obtenidos |
|-------|-----------------------------------------|--------|-----------|
| A     | pandas - Fundamentos                    | 30     |           |
| B     | numpy y Estadistica                     | 20     |           |
| C     | matplotlib y Visualizacion              | 20     |           |
| D     | Analisis de Imagen con Ciencia de Datos | 15     |           |
| E     | Integracion con Flask                    | 15     |           |
| F     | Analisis (Bonus)                        | 10     |           |
| **Total** |                                     | **110**|           |

**Nota final (sobre 100):** ___________
