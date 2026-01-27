# Guía Completa de Jinja2 - Motor de Plantillas

Jinja2 es el motor de plantillas que usa Flask para generar HTML dinámico.
Esta guía te enseña todo lo que necesitas saber para crear tus propias plantillas.

---

## Índice

1. [Conceptos Básicos](#1-conceptos-básicos)
2. [Variables](#2-variables)
3. [Filtros](#3-filtros)
4. [Estructuras de Control](#4-estructuras-de-control)
5. [Herencia de Plantillas](#5-herencia-de-plantillas)
6. [Macros (Componentes Reutilizables)](#6-macros-componentes-reutilizables)
7. [Incluir Plantillas](#7-incluir-plantillas)
8. [Mensajes Flash](#8-mensajes-flash)
9. [Formularios](#9-formularios)
10. [Ejemplos Prácticos](#10-ejemplos-prácticos)

---

## 1. Conceptos Básicos

### ¿Qué es una plantilla?

Una plantilla es un archivo HTML con "huecos" que se rellenan con datos de Python.

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   Python (app_flask.py)              HTML (plantilla.html)      │
│   ─────────────────────              ────────────────────       │
│                                                                 │
│   @app.route('/producto')            <h1>{{ producto.nombre }}</h1>
│   def ver_producto():                <p>Precio: ${{ producto.precio }}</p>
│       producto = Producto(...)  ───► <p>Stock: {{ producto.stock }}</p>
│       return render_template(                                   │
│           'producto.html',                                      │
│           producto=producto                                     │
│       )                                                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Sintaxis Básica

Jinja2 usa tres tipos de delimitadores:

| Sintaxis | Uso | Ejemplo |
|----------|-----|---------|
| `{{ ... }}` | Mostrar variables | `{{ usuario.nombre }}` |
| `{% ... %}` | Lógica (if, for) | `{% if usuario %}...{% endif %}` |
| `{# ... #}` | Comentarios | `{# Esto no se ve #}` |

---

## 2. Variables

### Mostrar variables simples

```html
<!-- Variable simple -->
<p>Hola, {{ nombre }}</p>

<!-- Atributo de objeto -->
<p>Email: {{ usuario.email }}</p>

<!-- Acceso a diccionario -->
<p>Valor: {{ datos['clave'] }}</p>
<p>Valor: {{ datos.clave }}</p>

<!-- Acceso a lista por índice -->
<p>Primero: {{ lista[0] }}</p>
```

### Valores por defecto

```html
<!-- Si la variable no existe, muestra el valor por defecto -->
<p>{{ nombre | default('Anónimo') }}</p>

<!-- También puedes usar 'or' -->
<p>{{ descripcion or 'Sin descripción' }}</p>
```

### Variables especiales de Flask

```html
<!-- URL de la ruta actual -->
<p>Estás en: {{ request.path }}</p>

<!-- Método HTTP -->
<p>Método: {{ request.method }}</p>

<!-- Generar URL de una ruta -->
<a href="{{ url_for('index') }}">Inicio</a>
<a href="{{ url_for('ver_producto', id=5) }}">Ver Producto 5</a>

<!-- Archivos estáticos (CSS, JS, imágenes) -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
<img src="{{ url_for('static', filename='img/logo.png') }}">
```

---

## 3. Filtros

Los filtros modifican el valor de las variables. Se aplican con `|`.

### Filtros de texto

```html
<!-- Mayúsculas -->
<p>{{ nombre | upper }}</p>  <!-- JUAN -->

<!-- Minúsculas -->
<p>{{ nombre | lower }}</p>  <!-- juan -->

<!-- Capitalizar -->
<p>{{ nombre | capitalize }}</p>  <!-- Juan -->

<!-- Título (primera letra de cada palabra) -->
<p>{{ "hola mundo" | title }}</p>  <!-- Hola Mundo -->

<!-- Recortar espacios -->
<p>{{ "  texto  " | trim }}</p>  <!-- texto -->

<!-- Truncar texto (útil para descripciones largas) -->
<p>{{ descripcion | truncate(100) }}</p>

<!-- Reemplazar -->
<p>{{ texto | replace('viejo', 'nuevo') }}</p>
```

### Filtros numéricos

```html
<!-- Redondear -->
<p>{{ 3.7 | round }}</p>  <!-- 4 -->
<p>{{ 3.14159 | round(2) }}</p>  <!-- 3.14 -->

<!-- Valor absoluto -->
<p>{{ -5 | abs }}</p>  <!-- 5 -->

<!-- Formato de número (separador de miles) -->
<p>{{ 1234567 | format('d') }}</p>
```

### Formato de moneda y fechas

```html
<!-- Precio con formato -->
<p>${{ producto.precio | round(2) }}</p>

<!-- Fecha formateada -->
<p>{{ fecha | default('') }}</p>

<!-- Formato personalizado (si fecha es datetime) -->
<p>{{ fecha.strftime('%d/%m/%Y') if fecha else 'N/A' }}</p>
<p>{{ fecha.strftime('%d/%m/%Y %H:%M') if fecha else 'N/A' }}</p>
```

### Filtros de lista

```html
<!-- Longitud -->
<p>Total: {{ productos | length }}</p>

<!-- Primero y último -->
<p>Primero: {{ lista | first }}</p>
<p>Último: {{ lista | last }}</p>

<!-- Ordenar -->
{% for p in productos | sort(attribute='nombre') %}
    {{ p.nombre }}
{% endfor %}

<!-- Unir lista en texto -->
<p>{{ ['a', 'b', 'c'] | join(', ') }}</p>  <!-- a, b, c -->
```

### Filtros de seguridad

```html
<!-- Escapar HTML (previene XSS) - por defecto está activo -->
<p>{{ texto_usuario }}</p>

<!-- Marcar como HTML seguro (¡cuidado! solo con contenido confiable) -->
<p>{{ contenido_html | safe }}</p>
```

---

## 4. Estructuras de Control

### Condicionales (if/elif/else)

```html
<!-- If simple -->
{% if usuario %}
    <p>Hola, {{ usuario.nombre }}</p>
{% endif %}

<!-- If/else -->
{% if productos %}
    <ul>
        {% for p in productos %}
            <li>{{ p.nombre }}</li>
        {% endfor %}
    </ul>
{% else %}
    <p>No hay productos</p>
{% endif %}

<!-- If/elif/else -->
{% if producto.stock > 10 %}
    <span class="badge badge-success">En stock</span>
{% elif producto.stock > 0 %}
    <span class="badge badge-warning">Últimas unidades</span>
{% else %}
    <span class="badge badge-danger">Sin stock</span>
{% endif %}
```

### Operadores de comparación

```html
{% if precio == 0 %}...{% endif %}
{% if precio != 0 %}...{% endif %}
{% if precio > 100 %}...{% endif %}
{% if precio >= 100 %}...{% endif %}
{% if precio < 100 %}...{% endif %}
{% if precio <= 100 %}...{% endif %}
```

### Operadores lógicos

```html
{% if usuario and usuario.activo %}
    <p>Usuario activo</p>
{% endif %}

{% if not usuario %}
    <p>No hay usuario</p>
{% endif %}

{% if precio < 50 or en_oferta %}
    <span class="badge badge-success">Oferta</span>
{% endif %}
```

### Verificar existencia

```html
<!-- Verificar si variable existe -->
{% if nombre is defined %}
    <p>{{ nombre }}</p>
{% endif %}

<!-- Verificar si es None -->
{% if producto is none %}
    <p>No existe</p>
{% endif %}

<!-- Verificar si lista está vacía -->
{% if productos %}
    <!-- Tiene elementos -->
{% endif %}
```

### Bucles (for)

```html
<!-- Bucle simple -->
<ul>
{% for producto in productos %}
    <li>{{ producto.nombre }}</li>
{% endfor %}
</ul>

<!-- Con else si la lista está vacía -->
{% for producto in productos %}
    <li>{{ producto.nombre }}</li>
{% else %}
    <li>No hay productos</li>
{% endfor %}
```

### Variables especiales del loop

```html
{% for producto in productos %}
    <!-- Índice (empieza en 0) -->
    <p>Índice: {{ loop.index0 }}</p>

    <!-- Número (empieza en 1) -->
    <p>Número: {{ loop.index }}</p>

    <!-- ¿Es el primero? -->
    {% if loop.first %}
        <p>Este es el primero</p>
    {% endif %}

    <!-- ¿Es el último? -->
    {% if loop.last %}
        <p>Este es el último</p>
    {% endif %}

    <!-- Total de elementos -->
    <p>Total: {{ loop.length }}</p>

    <!-- Elementos restantes -->
    <p>Faltan: {{ loop.revindex }}</p>
{% endfor %}
```

### Ejemplo práctico: tabla con filas alternadas

```html
<table class="table table-striped">
    <thead>
        <tr>
            <th>#</th>
            <th>Nombre</th>
            <th>Precio</th>
        </tr>
    </thead>
    <tbody>
        {% for producto in productos %}
        <tr class="{{ 'par' if loop.index is even else 'impar' }}">
            <td>{{ loop.index }}</td>
            <td>{{ producto.nombre }}</td>
            <td>${{ producto.precio | round(2) }}</td>
        </tr>
        {% else %}
        <tr>
            <td colspan="3" class="text-center">No hay productos</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

---

## 5. Herencia de Plantillas

La herencia permite crear una plantilla base y extenderla en otras plantillas.

### Plantilla base (base.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Mi App{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <!-- Navegación (igual en todas las páginas) -->
    <nav class="navbar">
        <a href="{{ url_for('index') }}" class="navbar-brand">Mi App</a>
        <div class="navbar-menu">
            <a href="{{ url_for('listar_productos') }}">Productos</a>
        </div>
    </nav>

    <!-- Contenido (cambia en cada página) -->
    <div class="container">
        {% block content %}{% endblock %}
    </div>

    <!-- Footer (igual en todas las páginas) -->
    <footer class="footer">
        <p>Mi Aplicación - 2024</p>
    </footer>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Plantilla hija (productos/lista.html)

```html
{% extends "base.html" %}

{% block title %}Productos - Mi App{% endblock %}

{% block content %}
<h1>Lista de Productos</h1>

<ul>
{% for producto in productos %}
    <li>{{ producto.nombre }}</li>
{% endfor %}
</ul>
{% endblock %}
```

### Usar contenido del bloque padre

```html
{% extends "base.html" %}

{% block title %}
    Productos - {{ super() }}
{% endblock %}
{# Resultado: "Productos - Mi App" #}
```

---

## 6. Macros (Componentes Reutilizables)

Los macros son como funciones: defines una vez, usas muchas veces.

### Definir macros (macros.html)

```html
{# ============================================================
   MACRO: Campo de formulario
   ============================================================
   Uso: {{ campo_texto('nombre', 'Nombre del producto', required=true) }}
   ============================================================ #}
{% macro campo_texto(name, label, value='', required=false, type='text') %}
<div class="form-group">
    <label for="{{ name }}" class="form-label">
        {{ label }}{% if required %} *{% endif %}
    </label>
    <input type="{{ type }}"
           id="{{ name }}"
           name="{{ name }}"
           value="{{ value }}"
           class="form-control"
           {% if required %}required{% endif %}>
</div>
{% endmacro %}


{# ============================================================
   MACRO: Campo textarea
   ============================================================ #}
{% macro campo_textarea(name, label, value='', rows=4) %}
<div class="form-group">
    <label for="{{ name }}" class="form-label">{{ label }}</label>
    <textarea id="{{ name }}"
              name="{{ name }}"
              class="form-control"
              rows="{{ rows }}">{{ value }}</textarea>
</div>
{% endmacro %}


{# ============================================================
   MACRO: Campo select
   ============================================================
   Uso: {{ campo_select('categoria', 'Categoría', categorias, 'id', 'nombre', producto.categoria_id) }}
   ============================================================ #}
{% macro campo_select(name, label, options, value_field, text_field, selected_value=None) %}
<div class="form-group">
    <label for="{{ name }}" class="form-label">{{ label }}</label>
    <select id="{{ name }}" name="{{ name }}" class="form-control">
        <option value="">-- Seleccionar --</option>
        {% for option in options %}
        <option value="{{ option[value_field] }}"
                {% if option[value_field] == selected_value %}selected{% endif %}>
            {{ option[text_field] }}
        </option>
        {% endfor %}
    </select>
</div>
{% endmacro %}


{# ============================================================
   MACRO: Botón de acción
   ============================================================ #}
{% macro boton(texto, tipo='primary', url=None, submit=false) %}
{% if url %}
    <a href="{{ url }}" class="btn btn-{{ tipo }}">{{ texto }}</a>
{% else %}
    <button type="{{ 'submit' if submit else 'button' }}" class="btn btn-{{ tipo }}">
        {{ texto }}
    </button>
{% endif %}
{% endmacro %}


{# ============================================================
   MACRO: Badge de estado
   ============================================================ #}
{% macro badge_estado(activo) %}
{% if activo %}
    <span class="badge badge-success">Activo</span>
{% else %}
    <span class="badge badge-danger">Inactivo</span>
{% endif %}
{% endmacro %}


{# ============================================================
   MACRO: Badge de stock
   ============================================================ #}
{% macro badge_stock(cantidad) %}
{% if cantidad > 10 %}
    <span class="badge badge-success">{{ cantidad }}</span>
{% elif cantidad > 0 %}
    <span class="badge badge-warning">{{ cantidad }}</span>
{% else %}
    <span class="badge badge-danger">Sin stock</span>
{% endif %}
{% endmacro %}


{# ============================================================
   MACRO: Acciones de tabla (Editar, Eliminar)
   ============================================================ #}
{% macro acciones_tabla(editar_url, eliminar_url, confirmar_mensaje='¿Está seguro?') %}
<div class="btn-group">
    <a href="{{ editar_url }}" class="btn btn-primary btn-sm">Editar</a>
    <form action="{{ eliminar_url }}" method="POST" style="display: inline;"
          onsubmit="return confirm('{{ confirmar_mensaje }}');">
        <button type="submit" class="btn btn-danger btn-sm">Eliminar</button>
    </form>
</div>
{% endmacro %}
```

### Usar macros en otras plantillas

```html
{% extends "base.html" %}

{# Importar los macros #}
{% from "macros.html" import campo_texto, campo_textarea, campo_select, boton %}

{% block content %}
<h1>Nuevo Producto</h1>

<form method="POST" class="card card-simple">
    {{ campo_texto('nombre', 'Nombre', required=true) }}
    {{ campo_textarea('descripcion', 'Descripción') }}
    {{ campo_texto('precio', 'Precio', type='number') }}
    {{ campo_select('categoria_id', 'Categoría', categorias, 'id', 'nombre') }}

    <div class="form-actions">
        {{ boton('Guardar', 'success', submit=true) }}
        {{ boton('Cancelar', 'secondary', url=url_for('listar_productos')) }}
    </div>
</form>
{% endblock %}
```

---

## 7. Incluir Plantillas

Puedes dividir tu HTML en partes reutilizables.

### Archivo parcial (_navbar.html)

```html
{# Los archivos parciales empiezan con _ por convención #}
<nav class="navbar">
    <a href="{{ url_for('index') }}" class="navbar-brand">Mi App</a>
    <div class="navbar-menu">
        <a href="{{ url_for('listar_productos') }}">Productos</a>
        <a href="{{ url_for('listar_categorias') }}">Categorías</a>
    </div>
</nav>
```

### Incluir en otra plantilla

```html
<!DOCTYPE html>
<html>
<head>...</head>
<body>
    {% include '_navbar.html' %}

    <div class="container">
        {% block content %}{% endblock %}
    </div>

    {% include '_footer.html' %}
</body>
</html>
```

### Include con variables

```html
{# Pasar variables al include #}
{% include '_producto_card.html' with context %}

{# O sin el contexto actual #}
{% include '_producto_card.html' without context %}

{# Con variables específicas #}
{% set producto_actual = producto %}
{% include '_producto_card.html' %}
```

---

## 8. Mensajes Flash

Flask tiene un sistema de mensajes "flash" para notificaciones.

### En Python (app_flask.py)

```python
from flask import flash, redirect, url_for

@app.route('/producto/crear', methods=['POST'])
def crear_producto():
    # ... crear producto ...
    flash('Producto creado exitosamente', 'success')
    return redirect(url_for('listar_productos'))

@app.route('/producto/eliminar/<int:id>')
def eliminar_producto(id):
    # ... eliminar ...
    flash('Producto eliminado', 'danger')
    return redirect(url_for('listar_productos'))
```

### En la plantilla (base.html)

```html
{# Mostrar mensajes flash #}
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert alert-{{ category }}">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

### Categorías comunes

| Categoría | Uso | Color |
|-----------|-----|-------|
| `success` | Operación exitosa | Verde |
| `danger` | Error | Rojo |
| `warning` | Advertencia | Amarillo |
| `info` | Información | Azul |

---

## 9. Formularios

### Formulario completo

```html
<form method="POST" action="{{ url_for('crear_producto') }}" class="form">
    {# Token CSRF (si usas Flask-WTF) #}
    {# {{ form.csrf_token }} #}

    <div class="form-group">
        <label for="nombre" class="form-label">Nombre *</label>
        <input type="text"
               id="nombre"
               name="nombre"
               class="form-control"
               value="{{ producto.nombre if producto else '' }}"
               placeholder="Nombre del producto"
               required>
    </div>

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
        <label for="categoria_id" class="form-label">Categoría</label>
        <select id="categoria_id" name="categoria_id" class="form-control">
            <option value="">-- Sin categoría --</option>
            {% for cat in categorias %}
            <option value="{{ cat.id }}"
                    {% if producto and producto.categoria_id == cat.id %}selected{% endif %}>
                {{ cat.nombre }}
            </option>
            {% endfor %}
        </select>
    </div>

    <div class="form-group">
        <label class="form-check">
            <input type="checkbox"
                   name="activo"
                   {% if not producto or producto.activo %}checked{% endif %}>
            Producto activo
        </label>
    </div>

    <div class="form-actions">
        <button type="submit" class="btn btn-success">
            {% if producto %}Guardar cambios{% else %}Crear producto{% endif %}
        </button>
        <a href="{{ url_for('listar_productos') }}" class="btn btn-secondary">
            Cancelar
        </a>
    </div>
</form>
```

---

## 10. Ejemplos Prácticos

### Página de lista con tabla

```html
{% extends "base.html" %}
{% from "macros.html" import badge_stock, badge_estado, acciones_tabla %}

{% block title %}Productos{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Productos</h1>
    <a href="{{ url_for('crear_producto') }}" class="btn btn-success">+ Nuevo</a>
</div>

{% if productos %}
<div class="table-responsive">
    <table class="table table-hover">
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
            <tr>
                <td>{{ producto.id }}</td>
                <td>
                    <a href="{{ url_for('ver_producto', id=producto.id) }}">
                        {{ producto.nombre }}
                    </a>
                </td>
                <td>{{ producto.categoria.nombre if producto.categoria else '-' }}</td>
                <td>${{ producto.precio | round(2) }}</td>
                <td>{{ badge_stock(producto.stock) }}</td>
                <td>{{ badge_estado(producto.activo) }}</td>
                <td>
                    {{ acciones_tabla(
                        url_for('editar_producto', id=producto.id),
                        url_for('eliminar_producto', id=producto.id),
                        '¿Eliminar este producto?'
                    ) }}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% else %}
<div class="card empty-state">
    <p>No hay productos registrados</p>
    <a href="{{ url_for('crear_producto') }}" class="btn btn-success">
        Crear primer producto
    </a>
</div>
{% endif %}
{% endblock %}
```

### Página de detalle

```html
{% extends "base.html" %}

{% block title %}{{ producto.nombre }}{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <h1 class="card-title">{{ producto.nombre }}</h1>
        {% if producto.activo %}
            <span class="badge badge-success">Activo</span>
        {% else %}
            <span class="badge badge-danger">Inactivo</span>
        {% endif %}
    </div>

    <div class="card-body">
        <div class="grid-2">
            <div>
                <p><strong>Descripción:</strong></p>
                <p>{{ producto.descripcion or 'Sin descripción' }}</p>
            </div>
            <div>
                <p><strong>Precio:</strong> ${{ producto.precio | round(2) }}</p>
                <p><strong>Stock:</strong> {{ producto.stock }} unidades</p>
                <p><strong>Categoría:</strong>
                    {% if producto.categoria %}
                        <a href="{{ url_for('ver_categoria', id=producto.categoria.id) }}">
                            {{ producto.categoria.nombre }}
                        </a>
                    {% else %}
                        Sin categoría
                    {% endif %}
                </p>
            </div>
        </div>
    </div>

    <div class="card-footer">
        <div class="btn-group">
            <a href="{{ url_for('editar_producto', id=producto.id) }}"
               class="btn btn-primary">Editar</a>
            <form action="{{ url_for('eliminar_producto', id=producto.id) }}"
                  method="POST" style="display: inline;"
                  onsubmit="return confirm('¿Eliminar?');">
                <button type="submit" class="btn btn-danger">Eliminar</button>
            </form>
            <a href="{{ url_for('listar_productos') }}"
               class="btn btn-secondary">Volver</a>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Resumen de Sintaxis

| Qué hacer | Sintaxis |
|-----------|----------|
| Mostrar variable | `{{ variable }}` |
| If/else | `{% if %}...{% else %}...{% endif %}` |
| For loop | `{% for x in lista %}...{% endfor %}` |
| Herencia | `{% extends "base.html" %}` |
| Bloque | `{% block nombre %}...{% endblock %}` |
| Include | `{% include "_parcial.html" %}` |
| Macro | `{% macro nombre() %}...{% endmacro %}` |
| Importar | `{% from "macros.html" import nombre %}` |
| Comentario | `{# Comentario #}` |
| Filtro | `{{ variable \| filtro }}` |
| URL | `{{ url_for('ruta', param=valor) }}` |
| Static | `{{ url_for('static', filename='...') }}` |

---

**¡Ahora estás listo para crear plantillas increíbles!**
