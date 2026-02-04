# Guía Completa de HTML y CSS - Fundamentos para el Desarrollo Web

**Semana 8 - Preparación para el Motor de Plantillas**

---

## Índice

1. [¿Por qué necesitas HTML y CSS?](#1-por-qué-necesitas-html-y-css)
2. [HTML - El Esqueleto de la Web](#2-html---el-esqueleto-de-la-web)
3. [CSS - El Estilo de la Web](#3-css---el-estilo-de-la-web)
4. [Conectando HTML y CSS](#4-conectando-html-y-css)
5. [Componentes Web Comunes](#5-componentes-web-comunes)
6. [CSS Avanzado - Layout y Responsive](#6-css-avanzado---layout-y-responsive)
7. [Integración con Flask y Jinja2](#7-integración-con-flask-y-jinja2)
8. [Proyecto Práctico](#8-proyecto-práctico)
9. [Recursos y Siguientes Pasos](#9-recursos-y-siguientes-pasos)

---

## 1. ¿Por qué necesitas HTML y CSS?

### La Anatomía de una Página Web

Imagina una página web como una casa:

```
HTML = La estructura (paredes, habitaciones, puertas)
CSS  = La decoración (colores, muebles, estilo)
JavaScript = La funcionalidad (luces, electrodomésticos)
```

### En el contexto de Flask

Cuando trabajas con Flask + Jinja2:

1. **Python (Flask)** genera los datos
2. **HTML** estructura cómo se muestran
3. **CSS** define cómo se ven
4. **Jinja2** conecta Python con HTML

```python
# Python (Flask) - Los datos
productos = [
    {"nombre": "Laptop", "precio": 1200},
    {"nombre": "Mouse", "precio": 25}
]

# HTML + Jinja2 - La estructura
<h1>Productos</h1>
<ul>
    {% for producto in productos %}
        <li>{{ producto.nombre }} - ${{ producto.precio }}</li>
    {% endfor %}
</ul>

# CSS - El estilo
h1 { color: blue; }
li { background-color: lightgray; }
```

---

## 2. HTML - El Esqueleto de la Web

### 2.1 Estructura Básica

Todo documento HTML tiene esta estructura:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <!-- Información sobre la página (no visible) -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Primera Página</title>
</head>
<body>
    <!-- Contenido visible de la página -->
    <h1>¡Hola Mundo!</h1>
    <p>Esta es mi primera página web.</p>
</body>
</html>
```

### 2.2 Elementos HTML Fundamentales

#### Texto y Títulos

```html
<!-- Títulos (del más importante al menos importante) -->
<h1>Título Principal</h1>
<h2>Título Secundario</h2>
<h3>Subtítulo</h3>
<h4>Subtítulo Menor</h4>
<h5>Título Pequeño</h5>
<h6>Título Muy Pequeño</h6>

<!-- Párrafos -->
<p>Este es un párrafo normal.</p>
<p>Este es <strong>texto en negrita</strong> y <em>texto en cursiva</em>.</p>

<!-- Texto preformateado -->
<pre>
    Este texto
    mantiene los espacios
        y saltos de línea
</pre>

<!-- Citas -->
<blockquote>
    "La programación es el arte de decirle a otro humano lo que quieres que haga la computadora."
</blockquote>
```

#### Listas

```html
<!-- Lista no ordenada (con viñetas) -->
<ul>
    <li>Elemento 1</li>
    <li>Elemento 2</li>
    <li>Elemento 3</li>
</ul>

<!-- Lista ordenada (con números) -->
<ol>
    <li>Primer paso</li>
    <li>Segundo paso</li>
    <li>Tercer paso</li>
</ol>

<!-- Lista de definiciones -->
<dl>
    <dt>HTML</dt>
    <dd>Lenguaje de marcado para páginas web</dd>
    
    <dt>CSS</dt>
    <dd>Lenguaje para estilizar páginas web</dd>
</dl>
```

#### Enlaces e Imágenes

```html
<!-- Enlaces -->
<a href="https://www.google.com">Enlace a Google</a>
<a href="mailto:correo@ejemplo.com">Enviar email</a>
<a href="tel:+123456789">Llamar por teléfono</a>

<!-- Enlace a otra página de tu sitio -->
<a href="/productos">Ver productos</a>

<!-- Imágenes -->
<img src="mi-imagen.jpg" alt="Descripción de la imagen">
<img src="/static/images/logo.png" alt="Logo de mi empresa">

<!-- Imagen con enlace -->
<a href="/productos">
    <img src="banner-productos.jpg" alt="Ver nuestros productos">
</a>
```

#### Contenedores y Estructura

```html
<!-- Div - Contenedor genérico en bloque -->
<div>
    <h2>Una sección</h2>
    <p>Contenido de la sección</p>
</div>

<!-- Span - Contenedor genérico en línea -->
<p>Este texto tiene una <span>palabra especial</span> marcada.</p>

<!-- Elementos semánticos (HTML5) -->
<header>
    <h1>Título del sitio</h1>
    <nav>
        <ul>
            <li><a href="/">Inicio</a></li>
            <li><a href="/productos">Productos</a></li>
        </ul>
    </nav>
</header>

<main>
    <article>
        <h2>Título del artículo</h2>
        <p>Contenido principal...</p>
    </article>
    
    <aside>
        <h3>Información relacionada</h3>
        <p>Contenido lateral...</p>
    </aside>
</main>

<footer>
    <p>&copy; 2024 Mi Empresa</p>
</footer>
```

### 2.3 Formularios HTML

Los formularios son esenciales en aplicaciones web:

```html
<form action="/crear-producto" method="POST">
    
    <!-- Campo de texto -->
    <div>
        <label for="nombre">Nombre del producto:</label>
        <input type="text" id="nombre" name="nombre" required>
    </div>
    
    <!-- Campo numérico -->
    <div>
        <label for="precio">Precio:</label>
        <input type="number" id="precio" name="precio" step="0.01" min="0" required>
    </div>
    
    <!-- Campo de selección -->
    <div>
        <label for="categoria">Categoría:</label>
        <select id="categoria" name="categoria_id">
            <option value="">Selecciona una categoría</option>
            <option value="1">Electrónicos</option>
            <option value="2">Ropa</option>
        </select>
    </div>
    
    <!-- Área de texto -->
    <div>
        <label for="descripcion">Descripción:</label>
        <textarea id="descripcion" name="descripcion" rows="4"></textarea>
    </div>
    
    <!-- Checkbox -->
    <div>
        <input type="checkbox" id="disponible" name="disponible" checked>
        <label for="disponible">Producto disponible</label>
    </div>
    
    <!-- Radio buttons -->
    <div>
        <input type="radio" id="nuevo" name="estado" value="nuevo">
        <label for="nuevo">Nuevo</label>
        
        <input type="radio" id="usado" name="estado" value="usado">
        <label for="usado">Usado</label>
    </div>
    
    <!-- Botones -->
    <div>
        <button type="submit">Guardar producto</button>
        <button type="reset">Limpiar formulario</button>
        <a href="/productos">Cancelar</a>
    </div>
    
</form>
```

### 2.4 Tablas HTML

Para mostrar datos estructurados:

```html
<table>
    <caption>Lista de Productos</caption>
    
    <thead>
        <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Precio</th>
            <th>Stock</th>
            <th>Acciones</th>
        </tr>
    </thead>
    
    <tbody>
        <tr>
            <td>1</td>
            <td>Laptop Gaming</td>
            <td>$1,299.99</td>
            <td>15</td>
            <td>
                <a href="/producto/1">Ver</a>
                <a href="/producto/1/editar">Editar</a>
            </td>
        </tr>
        
        <tr>
            <td>2</td>
            <td>Mouse Inalámbrico</td>
            <td>$29.99</td>
            <td>50</td>
            <td>
                <a href="/producto/2">Ver</a>
                <a href="/producto/2/editar">Editar</a>
            </td>
        </tr>
    </tbody>
    
    <tfoot>
        <tr>
            <td colspan="3">Total de productos:</td>
            <td>65</td>
            <td></td>
        </tr>
    </tfoot>
</table>
```

### 2.5 Atributos Importantes

```html
<!-- Atributos comunes -->
<div id="mi-contenedor" class="caja destacada" data-info="extra">
    Contenido
</div>

<!-- id: identificador único -->
<!-- class: clases CSS (pueden repetirse) -->
<!-- data-*: datos personalizados -->

<!-- Atributos de accesibilidad -->
<img src="imagen.jpg" alt="Descripción para lectores de pantalla">
<input type="text" aria-label="Nombre del usuario" placeholder="Ingresa tu nombre">

<!-- Atributos de formulario -->
<input type="email" name="email" required autocomplete="email">
<input type="password" name="password" minlength="8" maxlength="50">
```

---

## 3. CSS - El Estilo de la Web

### 3.1 Sintaxis Básica de CSS

```css
/* Comentario en CSS */

/* Estructura básica */
selector {
    propiedad: valor;
    otra-propiedad: otro-valor;
}

/* Ejemplo */
h1 {
    color: blue;
    font-size: 24px;
    text-align: center;
}
```

### 3.2 Tipos de Selectores

#### Selectores Básicos

```css
/* Por elemento */
p {
    color: black;
}

/* Por ID (único) */
#mi-titulo {
    font-size: 32px;
}

/* Por clase (reutilizable) */
.destacado {
    background-color: yellow;
}

/* Selector universal */
* {
    margin: 0;
    padding: 0;
}
```

#### Selectores Combinados

```css
/* Descendiente: div dentro de header */
header div {
    padding: 10px;
}

/* Hijo directo: div hijo inmediato de header */
header > div {
    border: 1px solid gray;
}

/* Hermano adyacente: p inmediatamente después de h2 */
h2 + p {
    margin-top: 0;
}

/* Hermanos generales: todos los p después de h2 */
h2 ~ p {
    color: gray;
}
```

#### Pseudoclases y Pseudoelementos

```css
/* Estados de enlace */
a:link { color: blue; }
a:visited { color: purple; }
a:hover { color: red; }
a:active { color: orange; }

/* Otros estados */
input:focus {
    border-color: blue;
    outline: none;
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Pseudoelementos */
p::first-line {
    font-weight: bold;
}

p::first-letter {
    font-size: 200%;
    float: left;
}

/* Contenido generado */
.precio::before {
    content: "$";
}

.nuevo::after {
    content: " ¡Nuevo!";
    color: red;
}
```

#### Selectores de Atributo

```css
/* Elemento con atributo */
input[required] {
    border-color: red;
}

/* Atributo con valor exacto */
input[type="email"] {
    background-image: url('email-icon.png');
}

/* Atributo que contiene valor */
a[href*="google"] {
    color: #4285f4;
}

/* Atributo que empieza con valor */
a[href^="https://"] {
    font-weight: bold;
}

/* Atributo que termina con valor */
a[href$=".pdf"] {
    color: red;
}
```

### 3.3 Propiedades de Texto y Fuente

```css
.texto-ejemplo {
    /* Familia de fuente */
    font-family: 'Arial', sans-serif;
    
    /* Tamaño */
    font-size: 16px;        /* Píxeles absolutos */
    font-size: 1.2em;       /* Relativo al padre */
    font-size: 1.2rem;      /* Relativo a la raíz */
    
    /* Peso (grosor) */
    font-weight: normal;    /* o bold, 100-900 */
    
    /* Estilo */
    font-style: italic;     /* o normal, oblique */
    
    /* Color */
    color: #333333;         /* Hexadecimal */
    color: rgb(51, 51, 51); /* RGB */
    color: rgba(51, 51, 51, 0.8); /* RGB con transparencia */
    
    /* Alineación */
    text-align: left;       /* left, center, right, justify */
    
    /* Decoración */
    text-decoration: none;  /* none, underline, line-through */
    
    /* Transformación */
    text-transform: uppercase; /* uppercase, lowercase, capitalize */
    
    /* Espaciado */
    letter-spacing: 1px;    /* Entre letras */
    word-spacing: 2px;      /* Entre palabras */
    line-height: 1.5;       /* Altura de línea */
    
    /* Sangría */
    text-indent: 20px;
}
```

### 3.4 Modelo de Caja (Box Model)

```css
.caja-ejemplo {
    /* Contenido */
    width: 300px;
    height: 200px;
    
    /* Relleno interior (padding) */
    padding: 20px;              /* Todos los lados */
    padding: 10px 20px;         /* Vertical | Horizontal */
    padding: 5px 10px 15px 20px; /* Arriba | Derecha | Abajo | Izquierda */
    
    /* Borde */
    border: 2px solid #ccc;     /* Ancho | Estilo | Color */
    border-width: 1px;
    border-style: solid;        /* solid, dashed, dotted, double */
    border-color: #333;
    border-radius: 10px;        /* Esquinas redondeadas */
    
    /* Margen exterior */
    margin: 20px;
    margin: 10px auto;          /* Centrar horizontalmente */
    
    /* Fondo */
    background-color: #f8f9fa;
    background-image: url('patron.png');
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
    
    /* Sombra */
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
```

### 3.5 Posicionamiento y Layout

#### Display

```css
/* Tipos de display */
.bloque {
    display: block;         /* Ocupa todo el ancho disponible */
}

.en-linea {
    display: inline;        /* Solo ocupa el espacio necesario */
}

.en-linea-bloque {
    display: inline-block;  /* Híbrido: en línea pero acepta width/height */
}

.oculto {
    display: none;          /* No se muestra ni ocupa espacio */
}

/* Flexbox - Layout moderno */
.contenedor-flex {
    display: flex;
    flex-direction: row;    /* row, column, row-reverse, column-reverse */
    justify-content: center; /* flex-start, flex-end, center, space-between, space-around */
    align-items: center;    /* flex-start, flex-end, center, stretch */
    flex-wrap: wrap;        /* nowrap, wrap, wrap-reverse */
    gap: 20px;              /* Espacio entre elementos */
}

.elemento-flex {
    flex: 1;                /* Crecer y encogerse igualmente */
    flex-grow: 1;           /* Capacidad de crecer */
    flex-shrink: 1;         /* Capacidad de encogerse */
    flex-basis: auto;       /* Tamaño base */
}

/* Grid - Layout avanzado */
.contenedor-grid {
    display: grid;
    grid-template-columns: 1fr 2fr 1fr; /* Tres columnas */
    grid-template-rows: auto 1fr auto;  /* Tres filas */
    grid-gap: 20px;
    height: 100vh;
}

.elemento-grid {
    grid-column: 1 / 3;     /* Ocupar columnas 1 y 2 */
    grid-row: 2;            /* Ocupar fila 2 */
}
```

#### Posicionamiento

```css
.posicion-relativa {
    position: relative;
    top: 10px;
    left: 20px;
}

.posicion-absoluta {
    position: absolute;
    top: 50px;
    right: 30px;
}

.posicion-fija {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 1000;
}

.posicion-pegajosa {
    position: sticky;
    top: 0;
}
```

### 3.6 Responsive Design - Diseño Adaptable

```css
/* Unidades flexibles */
.responsive {
    width: 100%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 5%;
}

/* Media queries - Consultas de medios */
/* Móviles pequeños */
@media (max-width: 480px) {
    .contenedor {
        padding: 10px;
        font-size: 14px;
    }
    
    .grid-3 {
        grid-template-columns: 1fr; /* Una sola columna */
    }
}

/* Tablets */
@media (min-width: 481px) and (max-width: 768px) {
    .contenedor {
        padding: 20px;
    }
    
    .grid-3 {
        grid-template-columns: 1fr 1fr; /* Dos columnas */
    }
}

/* Escritorio */
@media (min-width: 769px) {
    .contenedor {
        padding: 40px;
    }
    
    .grid-3 {
        grid-template-columns: 1fr 1fr 1fr; /* Tres columnas */
    }
}

/* Impresión */
@media print {
    .no-imprimir {
        display: none;
    }
    
    body {
        font-size: 12pt;
        color: black;
        background: white;
    }
}
```

---

## 4. Conectando HTML y CSS

### 4.1 Tres Formas de Aplicar CSS

#### CSS Externo (Recomendado)

```html
<!-- En el <head> del HTML -->
<link rel="stylesheet" href="/static/css/styles.css">
```

```css
/* En el archivo styles.css */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}
```

#### CSS Interno

```html
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        
        .destacado {
            color: red;
        }
    </style>
</head>
<body>
    <p class="destacado">Texto destacado</p>
</body>
</html>
```

#### CSS en Línea (No recomendado para producción)

```html
<p style="color: red; font-weight: bold;">Texto con estilo en línea</p>
```

### 4.2 Especificidad CSS

El CSS sigue reglas de prioridad:

```css
/* Especificidad: 1 punto */
p {
    color: black;
}

/* Especificidad: 10 puntos */
.mi-clase {
    color: blue;
}

/* Especificidad: 100 puntos */
#mi-id {
    color: red;
}

/* Especificidad: 1000 puntos (evitar) */
/* <p style="color: green;"> */

/* Forzar con !important (último recurso) */
p {
    color: purple !important;
}
```

---

## 5. Componentes Web Comunes

### 5.1 Navegación

```html
<!-- HTML -->
<nav class="navbar">
    <a href="/" class="navbar-brand">Mi Sitio</a>
    <ul class="navbar-menu">
        <li><a href="/" class="navbar-link active">Inicio</a></li>
        <li><a href="/productos" class="navbar-link">Productos</a></li>
        <li><a href="/contacto" class="navbar-link">Contacto</a></li>
    </ul>
</nav>
```

```css
/* CSS */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 2rem;
    background-color: #2c3e50;
    color: white;
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: bold;
    text-decoration: none;
    color: white;
}

.navbar-menu {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 2rem;
}

.navbar-link {
    text-decoration: none;
    color: #ecf0f1;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    transition: background-color 0.3s ease;
}

.navbar-link:hover,
.navbar-link.active {
    background-color: #34495e;
    color: white;
}

/* Responsive */
@media (max-width: 768px) {
    .navbar {
        flex-direction: column;
        gap: 1rem;
    }
    
    .navbar-menu {
        flex-direction: column;
        width: 100%;
        text-align: center;
    }
}
```

### 5.2 Tarjetas (Cards)

```html
<!-- HTML -->
<div class="card">
    <div class="card-header">
        <h3 class="card-title">Laptop Gaming</h3>
        <span class="badge badge-success">Nuevo</span>
    </div>
    <div class="card-body">
        <p class="card-text">Laptop de alta performance para gaming y trabajo profesional.</p>
        <div class="card-meta">
            <span class="price">$1,299.99</span>
            <span class="stock">Stock: 15</span>
        </div>
    </div>
    <div class="card-footer">
        <button class="btn btn-primary">Ver detalles</button>
        <button class="btn btn-secondary">Agregar al carrito</button>
    </div>
</div>
```

```css
/* CSS */
.card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease;
}

.card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    background-color: #f8f9fa;
    border-bottom: 1px solid #e0e0e0;
}

.card-title {
    margin: 0;
    font-size: 1.2rem;
    color: #2c3e50;
}

.card-body {
    padding: 1rem;
}

.card-text {
    color: #6c757d;
    margin-bottom: 1rem;
}

.card-meta {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.price {
    font-size: 1.25rem;
    font-weight: bold;
    color: #27ae60;
}

.stock {
    color: #6c757d;
    font-size: 0.9rem;
}

.card-footer {
    padding: 1rem;
    background-color: #f8f9fa;
    border-top: 1px solid #e0e0e0;
    display: flex;
    gap: 0.5rem;
}

.badge {
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: bold;
    text-transform: uppercase;
}

.badge-success {
    background-color: #27ae60;
    color: white;
}
```

### 5.3 Botones

```html
<!-- HTML -->
<button class="btn btn-primary">Primario</button>
<button class="btn btn-secondary">Secundario</button>
<button class="btn btn-success">Éxito</button>
<button class="btn btn-danger">Peligro</button>
<button class="btn btn-warning">Advertencia</button>

<!-- Tamaños -->
<button class="btn btn-primary btn-sm">Pequeño</button>
<button class="btn btn-primary">Normal</button>
<button class="btn btn-primary btn-lg">Grande</button>

<!-- Estados -->
<button class="btn btn-primary" disabled>Deshabilitado</button>
```

```css
/* CSS */
.btn {
    display: inline-block;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    text-align: center;
    text-decoration: none;
    vertical-align: middle;
    cursor: pointer;
    border: 1px solid transparent;
    border-radius: 0.375rem;
    transition: all 0.15s ease-in-out;
}

.btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.btn:active {
    transform: translateY(0);
}

.btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

/* Colores */
.btn-primary {
    background-color: #007bff;
    border-color: #007bff;
    color: white;
}

.btn-primary:hover {
    background-color: #0056b3;
    border-color: #004085;
}

.btn-success {
    background-color: #28a745;
    border-color: #28a745;
    color: white;
}

.btn-danger {
    background-color: #dc3545;
    border-color: #dc3545;
    color: white;
}

/* Tamaños */
.btn-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.875rem;
}

.btn-lg {
    padding: 0.75rem 1.5rem;
    font-size: 1.125rem;
}
```

### 5.4 Formularios Estilizados

```html
<!-- HTML -->
<form class="form">
    <div class="form-group">
        <label for="nombre" class="form-label">Nombre *</label>
        <input type="text" id="nombre" name="nombre" class="form-control" required>
        <small class="form-help">Ingresa tu nombre completo</small>
    </div>
    
    <div class="form-group">
        <label for="email" class="form-label">Email *</label>
        <input type="email" id="email" name="email" class="form-control" required>
    </div>
    
    <div class="form-group">
        <label for="mensaje" class="form-label">Mensaje</label>
        <textarea id="mensaje" name="mensaje" class="form-control" rows="4"></textarea>
    </div>
    
    <div class="form-actions">
        <button type="submit" class="btn btn-primary">Enviar</button>
        <button type="reset" class="btn btn-secondary">Limpiar</button>
    </div>
</form>
```

```css
/* CSS */
.form {
    max-width: 500px;
    margin: 0 auto;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #2c3e50;
}

.form-control {
    width: 100%;
    padding: 0.75rem;
    font-size: 1rem;
    border: 1px solid #ced4da;
    border-radius: 0.375rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.form-control:hover {
    border-color: #86b7fe;
}

.form-control:focus {
    border-color: #86b7fe;
    outline: 0;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.form-control::placeholder {
    color: #6c757d;
    opacity: 1;
}

.form-help {
    font-size: 0.875rem;
    color: #6c757d;
    margin-top: 0.25rem;
}

.form-actions {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
}

/* Estados de validación */
.form-control.is-valid {
    border-color: #198754;
}

.form-control.is-invalid {
    border-color: #dc3545;
}

.form-feedback {
    font-size: 0.875rem;
    margin-top: 0.25rem;
}

.form-feedback.valid-feedback {
    color: #198754;
}

.form-feedback.invalid-feedback {
    color: #dc3545;
}
```

---

## 6. CSS Avanzado - Layout y Responsive

### 6.1 Variables CSS (Custom Properties)

```css
/* Definir variables globales */
:root {
    --color-primary: #007bff;
    --color-success: #28a745;
    --color-danger: #dc3545;
    --font-family: 'Arial', sans-serif;
    --border-radius: 0.375rem;
    --box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    --transition: all 0.15s ease-in-out;
}

/* Usar variables */
.btn-primary {
    background-color: var(--color-primary);
    border-radius: var(--border-radius);
    transition: var(--transition);
}

/* Variables locales */
.card {
    --card-padding: 1rem;
    --card-bg: #ffffff;
    
    padding: var(--card-padding);
    background-color: var(--card-bg);
}

/* Responsive variables */
@media (min-width: 768px) {
    :root {
        --card-padding: 2rem;
    }
}
```

### 6.2 Flexbox Avanzado

```css
/* Layout clásico con flexbox */
.page-layout {
    display: flex;
    min-height: 100vh;
    flex-direction: column;
}

.header {
    flex-shrink: 0; /* No se encoge */
}

.main-content {
    display: flex;
    flex: 1; /* Ocupa todo el espacio disponible */
}

.sidebar {
    flex-basis: 250px;
    flex-shrink: 0;
}

.content {
    flex: 1;
    padding: 2rem;
}

.footer {
    flex-shrink: 0;
}

/* Grid de tarjetas responsivo */
.cards-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    margin: -0.75rem; /* Compensar el gap */
}

.card {
    flex: 1 1 calc(33.333% - 1rem); /* Crecer, encogerse, base */
    min-width: 280px;
}

@media (max-width: 768px) {
    .card {
        flex: 1 1 100%;
    }
}
```

### 6.3 CSS Grid Avanzado

```css
/* Layout completo con Grid */
.app-layout {
    display: grid;
    grid-template-areas: 
        "header header"
        "sidebar main"
        "footer footer";
    grid-template-columns: 250px 1fr;
    grid-template-rows: auto 1fr auto;
    min-height: 100vh;
    gap: 0;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }

/* Responsive */
@media (max-width: 768px) {
    .app-layout {
        grid-template-areas: 
            "header"
            "main"
            "footer";
        grid-template-columns: 1fr;
    }
    
    .sidebar {
        display: none; /* Ocultar en móvil */
    }
}

/* Grid de productos */
.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    padding: 2rem;
}

/* Grid complejo */
.dashboard-grid {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    grid-auto-rows: minmax(200px, auto);
    gap: 1rem;
}

.widget-large {
    grid-column: span 8;
    grid-row: span 2;
}

.widget-medium {
    grid-column: span 4;
}

.widget-small {
    grid-column: span 3;
}
```

### 6.4 Animaciones y Transiciones

```css
/* Transiciones básicas */
.smooth-transition {
    transition: all 0.3s ease-in-out;
}

.hover-effect:hover {
    transform: translateY(-5px) scale(1.05);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

/* Animaciones con keyframes */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
}

.pulse {
    animation: pulse 2s infinite;
}

/* Loading spinner */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid var(--color-primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
```

---

## 7. Integración con Flask y Jinja2

### 7.1 Estructura de Archivos en Flask

```
tu-proyecto/
├── app.py
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       └── logo.png
└── templates/
    ├── base.html
    ├── index.html
    └── productos/
        ├── lista.html
        └── detalle.html
```

### 7.2 Plantilla Base con HTML y CSS

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mi Tienda{% endblock %}</title>
    
    <!-- CSS externo -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    
    <!-- CSS específico de página -->
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navegación -->
    <nav class="navbar">
        <a href="{{ url_for('index') }}" class="navbar-brand">Mi Tienda</a>
        <div class="navbar-menu">
            <a href="{{ url_for('index') }}" 
               class="navbar-link {{ 'active' if request.endpoint == 'index' }}">
               Inicio
            </a>
            <a href="{{ url_for('productos') }}" 
               class="navbar-link {{ 'active' if request.endpoint == 'productos' }}">
               Productos
            </a>
        </div>
    </nav>

    <!-- Contenido principal -->
    <main class="container">
        <!-- Mensajes flash con estilos -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} fade-in">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <!-- Contenido de la página -->
        {% block content %}{% endblock %}
    </main>

    <!-- Footer -->
    <footer class="footer">
        <p>&copy; {{ moment().year }} Mi Tienda. Todos los derechos reservados.</p>
    </footer>

    <!-- JavaScript -->
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 7.3 Lista de Productos con Estilos

```html
<!-- templates/productos/lista.html -->
{% extends "base.html" %}

{% block title %}Productos - {{ super() }}{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Catálogo de Productos</h1>
    <a href="{{ url_for('crear_producto') }}" class="btn btn-primary">
        + Nuevo Producto
    </a>
</div>

{% if productos %}
    <div class="products-grid">
        {% for producto in productos %}
            <div class="card card-hover">
                <div class="card-header">
                    <h3 class="card-title">{{ producto.nombre }}</h3>
                    {% if producto.stock > 0 %}
                        <span class="badge badge-success">Disponible</span>
                    {% else %}
                        <span class="badge badge-danger">Agotado</span>
                    {% endif %}
                </div>
                
                <div class="card-body">
                    <p class="card-text">{{ producto.descripcion or "Sin descripción" }}</p>
                    
                    <div class="card-meta">
                        <span class="price">${{ "%.2f"|format(producto.precio) }}</span>
                        <span class="stock">Stock: {{ producto.stock }}</span>
                    </div>
                    
                    {% if producto.categoria %}
                        <div class="card-category">
                            <small class="text-muted">
                                Categoría: {{ producto.categoria.nombre }}
                            </small>
                        </div>
                    {% endif %}
                </div>
                
                <div class="card-footer">
                    <a href="{{ url_for('ver_producto', id=producto.id) }}" 
                       class="btn btn-primary btn-sm">
                       Ver detalles
                    </a>
                    <a href="{{ url_for('editar_producto', id=producto.id) }}" 
                       class="btn btn-secondary btn-sm">
                       Editar
                    </a>
                </div>
            </div>
        {% endfor %}
    </div>
{% else %}
    <div class="empty-state">
        <p>No hay productos registrados aún.</p>
        <a href="{{ url_for('crear_producto') }}" class="btn btn-primary">
            Crear el primer producto
        </a>
    </div>
{% endif %}
{% endblock %}
```

### 7.4 Formulario Estilizado con Validación

```html
<!-- templates/productos/formulario.html -->
{% extends "base.html" %}

{% block title %}
    {{ "Editar" if producto else "Nuevo" }} Producto - {{ super() }}
{% endblock %}

{% block content %}
<div class="page-header">
    <h1>{{ "Editar" if producto else "Nuevo" }} Producto</h1>
</div>

<form class="form" method="POST" novalidate>
    {{ form.hidden_tag() if form }} <!-- CSRF token si usas Flask-WTF -->
    
    <div class="form-group">
        <label for="nombre" class="form-label">Nombre del producto *</label>
        <input type="text" 
               id="nombre" 
               name="nombre" 
               class="form-control {{ 'is-invalid' if form and form.nombre.errors else '' }}"
               value="{{ producto.nombre if producto else '' }}"
               required>
        {% if form and form.nombre.errors %}
            <div class="form-feedback invalid-feedback">
                {{ form.nombre.errors[0] }}
            </div>
        {% endif %}
    </div>
    
    <div class="grid-2">
        <div class="form-group">
            <label for="precio" class="form-label">Precio *</label>
            <input type="number" 
                   id="precio" 
                   name="precio" 
                   class="form-control"
                   value="{{ producto.precio if producto else '' }}"
                   step="0.01" 
                   min="0" 
                   required>
        </div>
        
        <div class="form-group">
            <label for="stock" class="form-label">Stock</label>
            <input type="number" 
                   id="stock" 
                   name="stock" 
                   class="form-control"
                   value="{{ producto.stock if producto else '0' }}"
                   min="0">
        </div>
    </div>
    
    <div class="form-group">
        <label for="categoria_id" class="form-label">Categoría</label>
        <select id="categoria_id" name="categoria_id" class="form-control">
            <option value="">Selecciona una categoría</option>
            {% for categoria in categorias %}
                <option value="{{ categoria.id }}" 
                        {{ 'selected' if producto and producto.categoria_id == categoria.id }}>
                    {{ categoria.nombre }}
                </option>
            {% endfor %}
        </select>
    </div>
    
    <div class="form-group">
        <label for="descripcion" class="form-label">Descripción</label>
        <textarea id="descripcion" 
                  name="descripcion" 
                  class="form-control" 
                  rows="4"
                  placeholder="Describe las características del producto...">{{ producto.descripcion if producto else '' }}</textarea>
    </div>
    
    <div class="form-actions">
        <button type="submit" class="btn btn-primary">
            {{ "Actualizar" if producto else "Crear" }} Producto
        </button>
        <a href="{{ url_for('listar_productos') }}" class="btn btn-secondary">
            Cancelar
        </a>
    </div>
</form>
{% endblock %}

{% block extra_js %}
<script>
// JavaScript para validación en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.form');
    const nombreInput = document.getElementById('nombre');
    const precioInput = document.getElementById('precio');
    
    // Validar nombre
    nombreInput.addEventListener('blur', function() {
        if (this.value.length < 3) {
            this.classList.add('is-invalid');
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        }
    });
    
    // Validar precio
    precioInput.addEventListener('blur', function() {
        const precio = parseFloat(this.value);
        if (isNaN(precio) || precio <= 0) {
            this.classList.add('is-invalid');
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        }
    });
    
    // Validación antes de enviar
    form.addEventListener('submit', function(e) {
        let valid = true;
        
        if (nombreInput.value.length < 3) {
            nombreInput.classList.add('is-invalid');
            valid = false;
        }
        
        if (parseFloat(precioInput.value) <= 0) {
            precioInput.classList.add('is-invalid');
            valid = false;
        }
        
        if (!valid) {
            e.preventDefault();
            alert('Por favor corrige los errores del formulario');
        }
    });
});
</script>
{% endblock %}
```

### 7.5 Tabla Responsiva con Filtros

```html
<!-- templates/productos/tabla.html -->
{% extends "base.html" %}

{% block content %}
<div class="page-header">
    <h1>Administrar Productos</h1>
    <div class="page-actions">
        <input type="text" 
               id="filtro-busqueda" 
               class="form-control" 
               placeholder="Buscar productos..."
               style="width: 300px;">
        <select id="filtro-categoria" class="form-control" style="width: 200px;">
            <option value="">Todas las categorías</option>
            {% for categoria in categorias %}
                <option value="{{ categoria.id }}">{{ categoria.nombre }}</option>
            {% endfor %}
        </select>
    </div>
</div>

<div class="table-responsive">
    <table class="table" id="tabla-productos">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Categoría</th>
                <th>Precio</th>
                <th>Stock</th>
                <th>Estado</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            {% for producto in productos %}
                <tr data-categoria="{{ producto.categoria_id or '' }}">
                    <td>{{ producto.id }}</td>
                    <td>
                        <strong>{{ producto.nombre }}</strong>
                        {% if producto.descripcion %}
                            <br><small class="text-muted">{{ producto.descripcion[:50] }}...</small>
                        {% endif %}
                    </td>
                    <td>
                        {% if producto.categoria %}
                            <span class="badge badge-info">{{ producto.categoria.nombre }}</span>
                        {% else %}
                            <span class="text-muted">Sin categoría</span>
                        {% endif %}
                    </td>
                    <td class="price">${{ "%.2f"|format(producto.precio) }}</td>
                    <td>
                        {% if producto.stock > 10 %}
                            <span class="badge badge-success">{{ producto.stock }}</span>
                        {% elif producto.stock > 0 %}
                            <span class="badge badge-warning">{{ producto.stock }}</span>
                        {% else %}
                            <span class="badge badge-danger">{{ producto.stock }}</span>
                        {% endif %}
                    </td>
                    <td>
                        {% if producto.stock > 0 %}
                            <span class="badge badge-success">Disponible</span>
                        {% else %}
                            <span class="badge badge-danger">Agotado</span>
                        {% endif %}
                    </td>
                    <td>
                        <div class="btn-group">
                            <a href="{{ url_for('ver_producto', id=producto.id) }}" 
                               class="btn btn-sm btn-primary">Ver</a>
                            <a href="{{ url_for('editar_producto', id=producto.id) }}" 
                               class="btn btn-sm btn-secondary">Editar</a>
                            <form method="POST" 
                                  action="{{ url_for('eliminar_producto', id=producto.id) }}" 
                                  style="display: inline;"
                                  onsubmit="return confirm('¿Estás seguro de eliminar este producto?')">
                                <button type="submit" class="btn btn-sm btn-danger">Eliminar</button>
                            </form>
                        </div>
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

{% if not productos %}
    <div class="empty-state">
        <p>No hay productos para mostrar.</p>
    </div>
{% endif %}
{% endblock %}

{% block extra_js %}
<script>
// JavaScript para filtros
document.addEventListener('DOMContentLoaded', function() {
    const filtroBusqueda = document.getElementById('filtro-busqueda');
    const filtroCategoria = document.getElementById('filtro-categoria');
    const tabla = document.getElementById('tabla-productos');
    const filas = tabla.querySelectorAll('tbody tr');
    
    function filtrarTabla() {
        const textoBusqueda = filtroBusqueda.value.toLowerCase();
        const categoriaSeleccionada = filtroCategoria.value;
        
        filas.forEach(fila => {
            const nombre = fila.cells[1].textContent.toLowerCase();
            const categoria = fila.getAttribute('data-categoria');
            
            const coincideTexto = nombre.includes(textoBusqueda);
            const coincideCategoria = !categoriaSeleccionada || categoria === categoriaSeleccionada;
            
            if (coincideTexto && coincideCategoria) {
                fila.style.display = '';
            } else {
                fila.style.display = 'none';
            }
        });
    }
    
    filtroBusqueda.addEventListener('input', filtrarTabla);
    filtroCategoria.addEventListener('change', filtrarTabla);
});
</script>
{% endblock %}
```

---

## 8. Proyecto Práctico

### 8.1 Objetivo del Proyecto

Crear una **tienda online básica** que demuestre todos los conceptos aprendidos:

- ✅ Estructura HTML semántica
- ✅ Estilos CSS modernos y responsivos
- ✅ Integración con Flask y Jinja2
- ✅ Formularios funcionales
- ✅ Navegación intuitiva

### 8.2 Funcionalidades a Implementar

1. **Página de inicio** con productos destacados
2. **Catálogo de productos** con filtros
3. **Detalle de producto** individual
4. **Formulario de contacto**
5. **Panel administrativo** básico

### 8.3 Estructura del Proyecto

```
mi-tienda/
├── app.py
├── models.py
├── static/
│   ├── css/
│   │   ├── styles.css
│   │   └── admin.css
│   ├── js/
│   │   └── main.js
│   └── images/
│       ├── logo.png
│       └── productos/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── contacto.html
│   ├── productos/
│   │   ├── catalogo.html
│   │   ├── detalle.html
│   │   └── admin.html
│   └── includes/
│       ├── navbar.html
│       └── footer.html
└── requirements.txt
```

### 8.4 Página de Inicio Ejemplo

```html
<!-- templates/index.html -->
{% extends "base.html" %}

{% block title %}Inicio - Tienda Online{% endblock %}

{% block extra_css %}
<style>
.hero {
    background: linear-gradient(135deg, var(--color-primary), var(--color-success));
    color: white;
    padding: 4rem 0;
    text-align: center;
    margin-bottom: 3rem;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.featured-products {
    margin: 3rem 0;
}

.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    margin: 3rem 0;
}
</style>
{% endblock %}

{% block content %}
<!-- Hero Section -->
<section class="hero">
    <div class="container">
        <h1>Bienvenido a Nuestra Tienda</h1>
        <p>Los mejores productos al mejor precio</p>
        <a href="{{ url_for('catalogo') }}" class="btn btn-lg" style="background: white; color: var(--color-primary);">
            Ver Catálogo
        </a>
    </div>
</section>

<!-- Estadísticas -->
<section class="stats">
    <div class="stat-card">
        <div class="stat-number">{{ total_productos }}</div>
        <div class="stat-label">Productos</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{{ total_categorias }}</div>
        <div class="stat-label">Categorías</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">{{ productos_disponibles }}</div>
        <div class="stat-label">Disponibles</div>
    </div>
    <div class="stat-card">
        <div class="stat-number">4.8/5</div>
        <div class="stat-label">Calificación</div>
    </div>
</section>

<!-- Productos Destacados -->
<section class="featured-products">
    <h2>Productos Destacados</h2>
    <div class="products-grid">
        {% for producto in productos_destacados %}
            <div class="card card-hover">
                <div class="card-header">
                    <h3 class="card-title">{{ producto.nombre }}</h3>
                    {% if loop.first %}
                        <span class="badge badge-warning">Más Popular</span>
                    {% endif %}
                </div>
                <div class="card-body">
                    <p class="card-text">{{ producto.descripcion[:100] }}...</p>
                    <div class="card-meta">
                        <span class="price">${{ "%.2f"|format(producto.precio) }}</span>
                        <span class="stock">Stock: {{ producto.stock }}</span>
                    </div>
                </div>
                <div class="card-footer">
                    <a href="{{ url_for('detalle_producto', id=producto.id) }}" 
                       class="btn btn-primary">Ver Detalles</a>
                </div>
            </div>
        {% endfor %}
    </div>
</section>

<!-- Call to Action -->
<section style="text-align: center; padding: 3rem 0; background: #f8f9fa; margin-top: 3rem;">
    <h2>¿Tienes preguntas?</h2>
    <p>Estamos aquí para ayudarte</p>
    <a href="{{ url_for('contacto') }}" class="btn btn-primary btn-lg">Contáctanos</a>
</section>
{% endblock %}
```

### 8.5 Ejercicios Prácticos

#### Ejercicio 1: Crear un Componente de Producto

```html
<!-- Crear templates/components/producto_card.html -->
<div class="producto-card" data-id="{{ producto.id }}">
    <div class="producto-imagen">
        {% if producto.imagen %}
            <img src="{{ url_for('static', filename='images/productos/' + producto.imagen) }}" 
                 alt="{{ producto.nombre }}">
        {% else %}
            <div class="sin-imagen">Sin imagen</div>
        {% endif %}
    </div>
    
    <div class="producto-info">
        <h3>{{ producto.nombre }}</h3>
        <p class="precio">${{ "%.2f"|format(producto.precio) }}</p>
        
        {% if mostrar_descripcion %}
            <p class="descripcion">{{ producto.descripcion }}</p>
        {% endif %}
        
        <div class="producto-acciones">
            <button class="btn btn-primary" onclick="verDetalle({{ producto.id }})">
                Ver Detalles
            </button>
            {% if modo_admin %}
                <button class="btn btn-secondary" onclick="editarProducto({{ producto.id }})">
                    Editar
                </button>
            {% endif %}
        </div>
    </div>
</div>
```

#### Ejercicio 2: Sistema de Filtros Avanzado

```javascript
// static/js/filtros.js
class FiltroProductos {
    constructor() {
        this.productos = [];
        this.filtros = {
            categoria: '',
            precioMin: 0,
            precioMax: Infinity,
            disponible: null,
            busqueda: ''
        };
        
        this.init();
    }
    
    init() {
        // Cargar productos desde el DOM
        this.cargarProductos();
        
        // Configurar event listeners
        document.getElementById('filtro-categoria').addEventListener('change', (e) => {
            this.filtros.categoria = e.target.value;
            this.aplicarFiltros();
        });
        
        document.getElementById('filtro-busqueda').addEventListener('input', (e) => {
            this.filtros.busqueda = e.target.value.toLowerCase();
            this.aplicarFiltros();
        });
        
        // ... más filtros
    }
    
    cargarProductos() {
        const elementos = document.querySelectorAll('.producto-card');
        this.productos = Array.from(elementos).map(el => ({
            elemento: el,
            id: el.dataset.id,
            nombre: el.querySelector('h3').textContent.toLowerCase(),
            precio: parseFloat(el.querySelector('.precio').textContent.replace('$', '')),
            categoria: el.dataset.categoria || '',
            disponible: !el.classList.contains('agotado')
        }));
    }
    
    aplicarFiltros() {
        this.productos.forEach(producto => {
            let mostrar = true;
            
            // Filtro por categoría
            if (this.filtros.categoria && producto.categoria !== this.filtros.categoria) {
                mostrar = false;
            }
            
            // Filtro por precio
            if (producto.precio < this.filtros.precioMin || producto.precio > this.filtros.precioMax) {
                mostrar = false;
            }
            
            // Filtro por disponibilidad
            if (this.filtros.disponible !== null && producto.disponible !== this.filtros.disponible) {
                mostrar = false;
            }
            
            // Filtro por búsqueda
            if (this.filtros.busqueda && !producto.nombre.includes(this.filtros.busqueda)) {
                mostrar = false;
            }
            
            // Mostrar u ocultar elemento
            producto.elemento.style.display = mostrar ? 'block' : 'none';
        });
        
        this.actualizarContadores();
    }
    
    actualizarContadores() {
        const visibles = this.productos.filter(p => p.elemento.style.display !== 'none');
        document.getElementById('contador-productos').textContent = 
            `Mostrando ${visibles.length} de ${this.productos.length} productos`;
    }
}

// Inicializar cuando cargue la página
document.addEventListener('DOMContentLoaded', function() {
    new FiltroProductos();
});
```

#### Ejercicio 3: Modal de Detalles del Producto

```html
<!-- Modal HTML -->
<div id="modal-producto" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h2 id="modal-titulo">Título del Producto</h2>
            <button class="modal-close" onclick="cerrarModal()">&times;</button>
        </div>
        <div class="modal-body">
            <div class="producto-detalle">
                <div class="producto-imagen-grande">
                    <img id="modal-imagen" src="" alt="">
                </div>
                <div class="producto-info-detalle">
                    <p id="modal-descripcion"></p>
                    <div class="producto-specs">
                        <div class="spec">
                            <strong>Precio:</strong> 
                            <span id="modal-precio"></span>
                        </div>
                        <div class="spec">
                            <strong>Stock:</strong> 
                            <span id="modal-stock"></span>
                        </div>
                        <div class="spec">
                            <strong>Categoría:</strong> 
                            <span id="modal-categoria"></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary" onclick="cerrarModal()">Cerrar</button>
            <button class="btn btn-primary">Agregar al Carrito</button>
        </div>
    </div>
</div>
```

```css
/* CSS para el Modal */
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    animation: fadeIn 0.3s ease;
}

.modal-content {
    background-color: white;
    margin: 5% auto;
    border-radius: 8px;
    width: 90%;
    max-width: 800px;
    max-height: 90vh;
    overflow-y: auto;
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from {
        transform: translateY(-50px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
    border-bottom: 1px solid #e0e0e0;
}

.modal-close {
    background: none;
    border: none;
    font-size: 2rem;
    cursor: pointer;
    color: #6c757d;
}

.modal-body {
    padding: 2rem;
}

.producto-detalle {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
}

.producto-imagen-grande img {
    width: 100%;
    border-radius: 8px;
}

.producto-specs {
    margin-top: 1rem;
}

.spec {
    margin-bottom: 0.5rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f0f0f0;
}

.modal-footer {
    padding: 1.5rem;
    border-top: 1px solid #e0e0e0;
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
}

@media (max-width: 768px) {
    .producto-detalle {
        grid-template-columns: 1fr;
    }
    
    .modal-content {
        margin: 2% auto;
        width: 95%;
    }
}
```

### 8.6 Mejores Prácticas

#### Organización del CSS

```css
/* 1. Variables y reset */
:root {
    --color-primary: #007bff;
    /* ... más variables */
}

* {
    box-sizing: border-box;
}

/* 2. Elementos base */
body, html {
    /* ... */
}

/* 3. Componentes */
.btn { /* ... */ }
.card { /* ... */ }
.modal { /* ... */ }

/* 4. Layout */
.container { /* ... */ }
.grid-2 { /* ... */ }

/* 5. Utilities */
.text-center { /* ... */ }
.mb-3 { /* ... */ }

/* 6. Media queries al final */
@media (max-width: 768px) {
    /* ... */
}
```

#### Nomenclatura CSS (BEM)

```css
/* Block Element Modifier */
.producto-card { /* Block */ }
.producto-card__imagen { /* Element */ }
.producto-card__titulo { /* Element */ }
.producto-card--destacado { /* Modifier */ }
.producto-card--agotado { /* Modifier */ }
```

#### Accesibilidad

```html
<!-- Siempre incluir alt en imágenes -->
<img src="producto.jpg" alt="Laptop Gaming RGB con pantalla 15 pulgadas">

<!-- Usar etiquetas semánticas -->
<main>
    <section aria-labelledby="productos-titulo">
        <h2 id="productos-titulo">Nuestros Productos</h2>
        <!-- contenido -->
    </section>
</main>

<!-- Navegación por teclado -->
<button class="btn" tabindex="0" aria-label="Agregar producto al carrito">
    Agregar al Carrito
</button>

<!-- Estados para lectores de pantalla -->
<div aria-live="polite" id="mensaje-estado">
    Producto agregado al carrito
</div>
```

---

## 9. Recursos y Siguientes Pasos

### 9.1 Recursos de Aprendizaje

#### Documentación Oficial
- [MDN Web Docs - HTML](https://developer.mozilla.org/es/docs/Web/HTML)
- [MDN Web Docs - CSS](https://developer.mozilla.org/es/docs/Web/CSS)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

#### Herramientas Online
- [CodePen](https://codepen.io/) - Para experimentar con HTML/CSS
- [CSS Grid Generator](https://grid.layoutit.com/)
- [Flexbox Froggy](https://flexboxfroggy.com/) - Juego para aprender Flexbox
- [CSS Grid Garden](https://cssgridgarden.com/) - Juego para aprender Grid

#### Frameworks CSS (para más adelante)
- [Bootstrap](https://getbootstrap.com/) - Framework completo
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first
- [Bulma](https://bulma.io/) - Modular CSS framework

### 9.2 Proyecto Final Sugerido

Crear una **aplicación web completa** que incluya:

1. **Frontend**: HTML, CSS, JavaScript básico
2. **Backend**: Flask + SQLAlchemy + Neon
3. **Base de datos**: Al menos 3 entidades relacionadas
4. **Funcionalidades**:
   - CRUD completo
   - Autenticación básica
   - Búsqueda y filtros
   - Diseño responsivo
   - Validación de formularios

### 9.3 Checklist de Conocimientos

#### HTML ✅
- [ ] Estructura básica de documentos HTML
- [ ] Elementos semánticos (header, nav, main, section, article, footer)
- [ ] Formularios completos con validación
- [ ] Tablas para datos estructurados
- [ ] Enlaces e imágenes
- [ ] Atributos de accesibilidad

#### CSS ✅
- [ ] Selectores básicos y avanzados
- [ ] Modelo de caja (box model)
- [ ] Flexbox para layouts flexibles
- [ ] CSS Grid para layouts complejos
- [ ] Responsive design con media queries
- [ ] Variables CSS (custom properties)
- [ ] Animaciones y transiciones
- [ ] Metodologías como BEM

#### Integración con Flask ✅
- [ ] Estructura de archivos estática
- [ ] Plantillas con herencia
- [ ] Variables y filtros de Jinja2
- [ ] Formularios con Flask
- [ ] Mensajes flash estilizados
- [ ] URLs dinámicas

### 9.4 Próximos Pasos

1. **JavaScript**: Para interactividad avanzada
2. **APIs REST**: Consumir y crear APIs
3. **Autenticación**: Login y registro de usuarios
4. **Bases de datos avanzadas**: Consultas complejas, índices
5. **Despliegue**: Poner tu aplicación en producción
6. **Testing**: Pruebas automatizadas

---

## Resumen Final

### Lo que has aprendido:

1. **HTML** es la **estructura** de tus páginas web
2. **CSS** es el **estilo y diseño** visual
3. **Jinja2** **conecta** Python con HTML
4. **Flask** organiza todo en una aplicación web

### La relación completa:

```python
# Python (Flask)
@app.route('/productos')
def listar_productos():
    productos = session.query(Producto).all()
    return render_template('productos.html', productos=productos)
```

```html
<!-- HTML + Jinja2 -->
<div class="products-grid">
    {% for producto in productos %}
        <div class="card">
            <h3>{{ producto.nombre }}</h3>
            <p class="price">${{ producto.precio }}</p>
        </div>
    {% endfor %}
</div>
```

```css
/* CSS */
.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
}

.card {
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.price {
    font-size: 1.5rem;
    color: var(--color-success);
    font-weight: bold;
}
```

### ¡Ahora tienes las herramientas para crear aplicaciones web completas!

**Recuerda**: La práctica hace al maestro. Experimenta, rompe cosas, arregla cosas, y sobre todo... ¡diviértete programando!

---

*"El diseño no es solo cómo se ve o cómo se siente. El diseño es cómo funciona."* - Steve Jobs

**¡Feliz programación! 🚀**