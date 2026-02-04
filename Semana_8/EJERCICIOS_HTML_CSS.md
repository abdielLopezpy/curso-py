# Ejercicios Prácticos - HTML y CSS
**Semana 8 - Curso de Python**

---

## 📋 Índice de Ejercicios

### Nivel Básico
1. [Mi Primera Página Web](#ejercicio-1-mi-primera-página-web)
2. [Formulario de Registro](#ejercicio-2-formulario-de-registro)
3. [Tarjetas de Productos](#ejercicio-3-tarjetas-de-productos)

### Nivel Intermedio
4. [Layout con CSS Grid](#ejercicio-4-layout-con-css-grid)
5. [Navegación Responsiva](#ejercicio-5-navegación-responsiva)
6. [Modal Interactivo](#ejercicio-6-modal-interactivo)

### Nivel Avanzado
7. [Tienda Online Completa](#ejercicio-7-tienda-online-completa)
8. [Dashboard Administrativo](#ejercicio-8-dashboard-administrativo)
9. [Integración con Flask](#ejercicio-9-integración-con-flask)

---

## Ejercicio 1: Mi Primera Página Web

**Objetivo**: Crear una página HTML básica con estructura semántica y estilos CSS.

### Instrucciones:
Crea un archivo `mi_pagina.html` que incluya:

- Estructura HTML5 completa
- Header con tu nombre
- Navegación con 3 enlaces
- Sección principal con información sobre ti
- Lista de tus habilidades
- Footer con copyright

### Código Base:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Página Personal</title>
    <style>
        /* TU CÓDIGO CSS AQUÍ */
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }
        
        /* Agrega más estilos... */
    </style>
</head>
<body>
    <!-- TU CÓDIGO HTML AQUÍ -->
    <header>
        <h1>¡Tu nombre aquí!</h1>
    </header>
    
    <!-- Completa el resto... -->
</body>
</html>
```

### ✅ Criterios de Evaluación:
- [ ] Estructura HTML5 correcta
- [ ] Al menos 3 elementos semánticos (`header`, `nav`, `main`, `section`, `footer`)
- [ ] CSS básico aplicado (colores, fuentes, espaciado)
- [ ] Lista ordenada o no ordenada
- [ ] Enlaces funcionales

---

## Ejercicio 2: Formulario de Registro

**Objetivo**: Crear un formulario completo con validación HTML y estilos CSS.

### Instrucciones:
Crea `formulario_registro.html` con un formulario que incluya:

- Campo de nombre (requerido)
- Email (requerido, tipo email)
- Contraseña (requerido, mínimo 8 caracteres)
- Confirmación de contraseña
- Fecha de nacimiento
- Género (radio buttons)
- Intereses (checkboxes)
- Botones de enviar y limpiar

### Plantilla Inicial:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulario de Registro</title>
    <style>
        :root {
            --color-primary: #007bff;
            --color-success: #28a745;
            --color-danger: #dc3545;
            --border-radius: 8px;
        }

        * {
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f8f9fa;
            margin: 0;
            padding: 20px;
        }

        .form-container {
            max-width: 500px;
            margin: 0 auto;
            background: white;
            padding: 2rem;
            border-radius: var(--border-radius);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 600;
            color: #333;
        }

        .form-control {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid #e9ecef;
            border-radius: var(--border-radius);
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        .form-control:focus {
            outline: none;
            border-color: var(--color-primary);
            box-shadow: 0 0 0 3px rgba(0,123,255,0.1);
        }

        /* Agrega más estilos... */
    </style>
</head>
<body>
    <div class="form-container">
        <h1>Registro de Usuario</h1>
        <form id="registroForm">
            <!-- TU CÓDIGO AQUÍ -->
            <div class="form-group">
                <label for="nombre" class="form-label">Nombre completo *</label>
                <input type="text" id="nombre" name="nombre" class="form-control" required>
            </div>

            <!-- Completa los demás campos... -->

            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Registrarse</button>
                <button type="reset" class="btn btn-secondary">Limpiar</button>
            </div>
        </form>
    </div>

    <script>
        // Agrega validación JavaScript aquí
        document.getElementById('registroForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Formulario enviado! (simulado)');
        });
    </script>
</body>
</html>
```

### ✅ Criterios de Evaluación:
- [ ] Todos los tipos de input utilizados correctamente
- [ ] Validación HTML implementada (required, minlength, pattern)
- [ ] Radio buttons y checkboxes funcionando
- [ ] Estilos CSS aplicados (focus, hover, etc.)
- [ ] JavaScript básico para validación

---

## Ejercicio 3: Tarjetas de Productos

**Objetivo**: Crear un grid de tarjetas de productos responsivo.

### Instrucciones:
Crea `catalogo_productos.html` con:

- Grid responsivo de 1-4 columnas según el tamaño de pantalla
- Al menos 6 tarjetas de productos
- Cada tarjeta con imagen, título, precio, descripción y botón
- Efectos hover
- Badges de estado (nuevo, oferta, agotado)

### Datos de Ejemplo:
```javascript
const productos = [
    {
        id: 1,
        nombre: "Laptop Gaming",
        precio: 1299.99,
        descripcion: "Laptop de alta performance",
        imagen: "laptop.jpg",
        estado: "nuevo"
    },
    {
        id: 2,
        nombre: "Mouse Gamer",
        precio: 59.99,
        descripcion: "Mouse RGB ergonómico",
        imagen: "mouse.jpg",
        estado: "oferta"
    }
    // Agrega más productos...
];
```

### ✅ Criterios de Evaluación:
- [ ] CSS Grid implementado correctamente
- [ ] Diseño responsivo (mobile, tablet, desktop)
- [ ] Efectos hover en las tarjetas
- [ ] Badges con diferentes colores según el estado
- [ ] Al menos 3 media queries

---

## Ejercicio 4: Layout con CSS Grid

**Objetivo**: Crear un layout complejo usando CSS Grid.

### Instrucciones:
Crea `layout_grid.html` con:

- Header que ocupe todo el ancho
- Sidebar izquierdo fijo
- Área de contenido principal
- Área lateral derecha (widgets)
- Footer que ocupe todo el ancho

### Plantilla:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Layout con CSS Grid</title>
    <style>
        .page-layout {
            display: grid;
            grid-template-areas: 
                "header header header"
                "sidebar main widgets"
                "footer footer footer";
            grid-template-columns: 250px 1fr 200px;
            grid-template-rows: auto 1fr auto;
            min-height: 100vh;
            gap: 20px;
            padding: 20px;
        }

        .header { 
            grid-area: header; 
            background: #007bff;
            color: white;
            padding: 1rem;
            text-align: center;
        }

        .sidebar { 
            grid-area: sidebar; 
            background: #f8f9fa;
            padding: 1rem;
        }

        .main { 
            grid-area: main; 
            background: white;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .widgets { 
            grid-area: widgets; 
            background: #e9ecef;
            padding: 1rem;
        }

        .footer { 
            grid-area: footer; 
            background: #343a40;
            color: white;
            padding: 1rem;
            text-align: center;
        }

        /* Responsivo */
        @media (max-width: 768px) {
            /* COMPLETA AQUÍ: Hacer que en móvil sea una sola columna */
        }
    </style>
</head>
<body>
    <div class="page-layout">
        <header class="header">
            <h1>Mi Aplicación Web</h1>
        </header>
        
        <aside class="sidebar">
            <h3>Navegación</h3>
            <ul>
                <li><a href="#inicio">Inicio</a></li>
                <li><a href="#productos">Productos</a></li>
                <li><a href="#contacto">Contacto</a></li>
            </ul>
        </aside>
        
        <main class="main">
            <h2>Contenido Principal</h2>
            <p>Aquí va el contenido principal de la aplicación...</p>
            <!-- Agrega más contenido -->
        </main>
        
        <aside class="widgets">
            <h4>Widgets</h4>
            <!-- Agrega widgets aquí -->
        </aside>
        
        <footer class="footer">
            <p>&copy; 2024 Mi Empresa</p>
        </footer>
    </div>
</body>
</html>
```

### ✅ Criterios de Evaluación:
- [ ] Grid areas definidas correctamente
- [ ] Layout responsivo implementado
- [ ] Sidebar con navegación funcional
- [ ] Widgets en el área lateral
- [ ] Footer sticky

---

## Ejercicio 5: Navegación Responsiva

**Objetivo**: Crear una barra de navegación que se adapte a dispositivos móviles.

### Instrucciones:
Crea `navegacion_responsiva.html` con:

- Logo/marca en la izquierda
- Menu horizontal en desktop
- Hamburger menu en móvil
- Animaciones suaves
- Submenús desplegables

### JavaScript Necesario:
```javascript
function toggleMenu() {
    const menu = document.getElementById('navMenu');
    const hamburger = document.getElementById('hamburger');
    
    menu.classList.toggle('active');
    hamburger.classList.toggle('active');
}

// Cerrar menú al hacer click fuera
document.addEventListener('click', function(e) {
    const nav = document.getElementById('navbar');
    if (!nav.contains(e.target)) {
        document.getElementById('navMenu').classList.remove('active');
        document.getElementById('hamburger').classList.remove('active');
    }
});
```

### ✅ Criterios de Evaluación:
- [ ] Navegación horizontal en desktop
- [ ] Hamburger menu funcional en móvil
- [ ] Animaciones CSS para transiciones
- [ ] JavaScript para toggle del menú
- [ ] Submenús (al menos uno)

---

## Ejercicio 6: Modal Interactivo

**Objetivo**: Crear un modal/popup reutilizable con CSS y JavaScript.

### Instrucciones:
Crea `modal_interactivo.html` que incluya:

- Botón para abrir modal
- Modal con header, body y footer
- Backdrop semi-transparente
- Animaciones de entrada y salida
- Cierre con ESC, click en X, o click fuera

### Código Base:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modal Interactivo</title>
    <style>
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }

        .modal-overlay.active {
            opacity: 1;
            visibility: visible;
        }

        .modal-content {
            background: white;
            border-radius: 8px;
            max-width: 500px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            transform: translateY(-50px) scale(0.9);
            transition: all 0.3s ease;
        }

        .modal-overlay.active .modal-content {
            transform: translateY(0) scale(1);
        }

        /* Completa los estilos... */
    </style>
</head>
<body>
    <!-- Botón para abrir modal -->
    <button onclick="openModal()" class="btn btn-primary">Abrir Modal</button>

    <!-- Modal -->
    <div class="modal-overlay" id="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Título del Modal</h3>
                <button class="modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body">
                <p>Contenido del modal...</p>
                <!-- Agrega un formulario aquí -->
            </div>
            <div class="modal-footer">
                <button onclick="closeModal()" class="btn btn-secondary">Cerrar</button>
                <button onclick="closeModal()" class="btn btn-primary">Guardar</button>
            </div>
        </div>
    </div>

    <script>
        function openModal() {
            // COMPLETA: Abrir modal
        }

        function closeModal() {
            // COMPLETA: Cerrar modal
        }

        // COMPLETA: Cerrar con ESC
        // COMPLETA: Cerrar al hacer click en overlay
    </script>
</body>
</html>
```

### ✅ Criterios de Evaluación:
- [ ] Modal se abre y cierra correctamente
- [ ] Animaciones suaves implementadas
- [ ] Múltiples formas de cerrar (ESC, X, click fuera)
- [ ] Bloqueo del scroll del body cuando está abierto
- [ ] Formulario funcional dentro del modal

---

## Ejercicio 7: Tienda Online Completa

**Objetivo**: Crear una tienda online completa con HTML, CSS y JavaScript.

### Instrucciones:
Crea una tienda online con múltiples páginas:

1. **index.html** - Página principal
2. **productos.html** - Catálogo con filtros  
3. **producto.html** - Detalle del producto
4. **carrito.html** - Carrito de compras
5. **contacto.html** - Formulario de contacto

### Funcionalidades Requeridas:

#### Página Principal:
- Hero section con call-to-action
- Productos destacados
- Categorías principales
- Footer informativo

#### Catálogo:
- Grid responsivo de productos
- Filtros por categoría y precio
- Búsqueda por nombre
- Paginación (simulada)

#### Detalle del Producto:
- Galería de imágenes (simulada)
- Información completa
- Botón "Agregar al carrito"
- Productos relacionados

#### Carrito:
- Lista de productos agregados
- Cálculo de totales
- Formulario de checkout básico

### Archivo CSS Global (`styles.css`):
```css
:root {
    --color-primary: #007bff;
    --color-secondary: #6c757d;
    --color-success: #28a745;
    --color-danger: #dc3545;
    --color-warning: #ffc107;
    --color-info: #17a2b8;
    --color-light: #f8f9fa;
    --color-dark: #343a40;
    
    --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --border-radius: 0.375rem;
    --box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    --transition: all 0.15s ease-in-out;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: var(--font-family);
    line-height: 1.6;
    color: var(--color-dark);
    background-color: var(--color-light);
}

/* Componentes reutilizables */
.btn {
    display: inline-block;
    font-weight: 400;
    text-align: center;
    text-decoration: none;
    vertical-align: middle;
    cursor: pointer;
    border: 1px solid transparent;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    border-radius: var(--border-radius);
    transition: var(--transition);
}

.btn-primary {
    color: #fff;
    background-color: var(--color-primary);
    border-color: var(--color-primary);
}

.btn-primary:hover {
    background-color: #0056b3;
    border-color: #004085;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
}

.row {
    display: flex;
    flex-wrap: wrap;
    margin: -0.5rem;
}

.col {
    flex: 1;
    padding: 0.5rem;
}

/* Agrega más componentes... */
```

### JavaScript Global (`main.js`):
```javascript
// Simulación de base de datos de productos
let productos = [
    {
        id: 1,
        nombre: "Laptop Gaming RGB",
        precio: 1299.99,
        categoria: "laptops",
        imagen: "laptop1.jpg",
        descripcion: "Laptop de alta performance con RGB",
        stock: 15
    },
    {
        id: 2,
        nombre: "Mouse Gaming",
        precio: 79.99,
        categoria: "accesorios",
        imagen: "mouse1.jpg", 
        descripcion: "Mouse ergonómico con 7 botones",
        stock: 30
    }
    // Agrega más productos...
];

// Carrito de compras
let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

// Funciones principales
function agregarAlCarrito(productId) {
    const producto = productos.find(p => p.id === productId);
    if (producto) {
        const existente = carrito.find(item => item.id === productId);
        if (existente) {
            existente.cantidad += 1;
        } else {
            carrito.push({...producto, cantidad: 1});
        }
        localStorage.setItem('carrito', JSON.stringify(carrito));
        actualizarContadorCarrito();
        mostrarNotificacion('Producto agregado al carrito');
    }
}

function actualizarContadorCarrito() {
    const contador = document.getElementById('carrito-contador');
    if (contador) {
        const totalItems = carrito.reduce((sum, item) => sum + item.cantidad, 0);
        contador.textContent = totalItems;
        contador.style.display = totalItems > 0 ? 'inline' : 'none';
    }
}

function mostrarNotificacion(mensaje) {
    // Implementar sistema de notificaciones
    alert(mensaje); // Versión simple
}

// Filtros de productos
function filtrarProductos() {
    const categoria = document.getElementById('filtro-categoria')?.value || '';
    const precioMax = document.getElementById('filtro-precio')?.value || Infinity;
    const busqueda = document.getElementById('busqueda')?.value.toLowerCase() || '';
    
    let productosFiltrados = productos.filter(producto => {
        const matchCategoria = !categoria || producto.categoria === categoria;
        const matchPrecio = producto.precio <= precioMax;
        const matchBusqueda = !busqueda || producto.nombre.toLowerCase().includes(busqueda);
        
        return matchCategoria && matchPrecio && matchBusqueda;
    });
    
    renderizarProductos(productosFiltrados);
}

function renderizarProductos(productosArray) {
    const contenedor = document.getElementById('productos-grid');
    if (!contenedor) return;
    
    contenedor.innerHTML = '';
    
    productosArray.forEach(producto => {
        const productCard = crearTarjetaProducto(producto);
        contenedor.appendChild(productCard);
    });
}

function crearTarjetaProducto(producto) {
    const card = document.createElement('div');
    card.className = 'product-card';
    card.innerHTML = `
        <div class="product-image">
            <img src="images/${producto.imagen}" alt="${producto.nombre}" loading="lazy">
        </div>
        <div class="product-info">
            <h3 class="product-title">${producto.nombre}</h3>
            <p class="product-price">$${producto.precio.toFixed(2)}</p>
            <p class="product-description">${producto.descripcion}</p>
            <div class="product-actions">
                <button onclick="agregarAlCarrito(${producto.id})" class="btn btn-primary">
                    Agregar al Carrito
                </button>
                <a href="producto.html?id=${producto.id}" class="btn btn-outline">
                    Ver Detalles
                </a>
            </div>
        </div>
    `;
    return card;
}

// Inicializar cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    actualizarContadorCarrito();
    
    // Si estamos en la página de productos, renderizar todos
    if (document.getElementById('productos-grid')) {
        renderizarProductos(productos);
    }
    
    // Configurar event listeners para filtros
    const filtros = ['filtro-categoria', 'filtro-precio', 'busqueda'];
    filtros.forEach(filtroId => {
        const elemento = document.getElementById(filtroId);
        if (elemento) {
            elemento.addEventListener('change', filtrarProductos);
            elemento.addEventListener('input', filtrarProductos);
        }
    });
});
```

### ✅ Criterios de Evaluación:
- [ ] Múltiples páginas HTML creadas
- [ ] Navegación entre páginas funcional
- [ ] CSS reutilizable y bien organizados
- [ ] JavaScript para carrito de compras
- [ ] LocalStorage para persistir datos
- [ ] Diseño completamente responsivo
- [ ] Formularios con validación
- [ ] Sistema de filtros funcional

---

## Ejercicio 8: Dashboard Administrativo

**Objetivo**: Crear un panel de administración con gráficos y estadísticas.

### Instrucciones:
Crea `dashboard.html` con:

- Sidebar de navegación colapsable
- Cards con estadísticas principales
- Tabla de datos con paginación
- Gráficos simulados con CSS
- Modo oscuro/claro

### Componentes a Incluir:

#### Sidebar:
```html
<aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
        <h3>Admin Panel</h3>
        <button id="sidebar-toggle">≡</button>
    </div>
    <nav class="sidebar-nav">
        <ul>
            <li><a href="#dashboard" class="nav-link active">Dashboard</a></li>
            <li><a href="#usuarios" class="nav-link">Usuarios</a></li>
            <li><a href="#productos" class="nav-link">Productos</a></li>
            <li><a href="#ventas" class="nav-link">Ventas</a></li>
            <li><a href="#configuracion" class="nav-link">Configuración</a></li>
        </ul>
    </nav>
</aside>
```

#### Cards de Estadísticas:
```html
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
            <div class="stat-number">1,234</div>
            <div class="stat-label">Usuarios Activos</div>
        </div>
    </div>
    
    <div class="stat-card">
        <div class="stat-icon">📦</div>
        <div class="stat-content">
            <div class="stat-number">567</div>
            <div class="stat-label">Productos</div>
        </div>
    </div>
    
    <!-- Más cards... -->
</div>
```

#### Gráfico CSS:
```css
.chart {
    display: flex;
    align-items: flex-end;
    height: 200px;
    padding: 20px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.chart-bar {
    flex: 1;
    background: var(--color-primary);
    margin: 0 2px;
    border-radius: 4px 4px 0 0;
    transition: all 0.3s ease;
    position: relative;
}

.chart-bar:hover {
    background: var(--color-secondary);
    transform: scale(1.05);
}

.chart-bar::after {
    content: attr(data-value);
    position: absolute;
    top: -25px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 0.8rem;
    font-weight: bold;
}
```

### ✅ Criterios de Evaluación:
- [ ] Sidebar colapsable funcional
- [ ] Cards de estadísticas responsivas
- [ ] Tabla con ordenamiento y filtros
- [ ] Gráficos creados con CSS puro
- [ ] Toggle de modo oscuro/claro
- [ ] JavaScript para toda la interactividad

---

## Ejercicio 9: Integración con Flask

**Objetivo**: Integrar los conocimientos de HTML/CSS con Flask y Jinja2.

### Instrucciones:
Crea una aplicación Flask que use las páginas creadas en ejercicios anteriores:

1. Convierte las páginas HTML estáticas en plantillas Jinja2
2. Crea rutas Flask para cada página
3. Implementa funcionalidad real de carrito de compras
4. Agrega base de datos con SQLAlchemy
5. Implementa autenticación básica

### Estructura de Archivos:
```
mi_tienda_flask/
├── app.py                  # Aplicación Flask principal
├── models.py               # Modelos SQLAlchemy
├── forms.py                # Formularios con Flask-WTF
├── static/
│   ├── css/
│   │   └── styles.css      # CSS del ejercicio 7
│   ├── js/
│   │   └── main.js         # JavaScript del ejercicio 7
│   └── images/
├── templates/
│   ├── base.html           # Plantilla base
│   ├── index.html          # Página principal
│   ├── productos.html      # Catálogo
│   ├── producto.html       # Detalle
│   ├── carrito.html        # Carrito
│   ├── contacto.html       # Contacto
│   └── auth/
│       ├── login.html      # Login
│       └── register.html   # Registro
└── requirements.txt
```

### Plantilla Base (`templates/base.html`):
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Mi Tienda Flask{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="{{ url_for('index') }}" class="navbar-brand">Mi Tienda</a>
            <ul class="navbar-nav">
                <li><a href="{{ url_for('index') }}" class="{{ 'active' if request.endpoint == 'index' }}">Inicio</a></li>
                <li><a href="{{ url_for('productos') }}" class="{{ 'active' if request.endpoint == 'productos' }}">Productos</a></li>
                <li><a href="{{ url_for('contacto') }}" class="{{ 'active' if request.endpoint == 'contacto' }}">Contacto</a></li>
                <li>
                    <a href="{{ url_for('carrito') }}" class="carrito-link">
                        🛒 Carrito 
                        <span class="carrito-contador" id="carrito-contador">{{ session.get('carrito', [])|length }}</span>
                    </a>
                </li>
                {% if current_user.is_authenticated %}
                    <li><a href="{{ url_for('perfil') }}">Mi Perfil</a></li>
                    <li><a href="{{ url_for('logout') }}">Salir</a></li>
                {% else %}
                    <li><a href="{{ url_for('login') }}">Iniciar Sesión</a></li>
                    <li><a href="{{ url_for('register') }}">Registro</a></li>
                {% endif %}
            </ul>
        </div>
    </nav>

    <main class="main-content">
        <!-- Mensajes Flash -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="alerts">
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 Mi Tienda Flask. Todos los derechos reservados.</p>
        </div>
    </footer>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### Aplicación Flask Principal (`app.py`):
```python
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_super_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tienda.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelos
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text)
    categoria = db.Column(db.String(100))
    stock = db.Column(db.Integer, default=0)
    imagen = db.Column(db.String(200))

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50), default='pendiente')

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rutas principales
@app.route('/')
def index():
    productos_destacados = Producto.query.filter_by(categoria='destacado').limit(4).all()
    return render_template('index.html', productos_destacados=productos_destacados)

@app.route('/productos')
def productos():
    categoria = request.args.get('categoria')
    precio_max = request.args.get('precio_max', type=float)
    busqueda = request.args.get('busqueda')
    
    query = Producto.query
    
    if categoria:
        query = query.filter_by(categoria=categoria)
    if precio_max:
        query = query.filter(Producto.precio <= precio_max)
    if busqueda:
        query = query.filter(Producto.nombre.contains(busqueda))
    
    productos = query.all()
    categorias = db.session.query(Producto.categoria).distinct().all()
    
    return render_template('productos.html', productos=productos, categorias=categorias)

@app.route('/producto/<int:id>')
def producto_detalle(id):
    producto = Producto.query.get_or_404(id)
    relacionados = Producto.query.filter(
        Producto.categoria == producto.categoria,
        Producto.id != id
    ).limit(3).all()
    
    return render_template('producto.html', producto=producto, relacionados=relacionados)

@app.route('/carrito')
def carrito():
    carrito_items = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito_items)
    return render_template('carrito.html', carrito=carrito_items, total=total)

@app.route('/agregar_carrito/<int:producto_id>')
def agregar_carrito(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    carrito = session.get('carrito', [])
    
    # Buscar si el producto ya está en el carrito
    for item in carrito:
        if item['id'] == producto_id:
            item['cantidad'] += 1
            break
    else:
        carrito.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'cantidad': 1
        })
    
    session['carrito'] = carrito
    flash('Producto agregado al carrito', 'success')
    return redirect(url_for('productos'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

### Archivo de Dependencias (`requirements.txt`):
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.3
Flask-WTF==1.1.1
WTForms==3.0.1
```

### ✅ Criterios de Evaluación:
- [ ] Aplicación Flask funcional con todas las rutas
- [ ] Plantillas Jinja2 con herencia correcta
- [ ] Base de datos SQLAlchemy implementada
- [ ] Sistema de carrito de compras funcional
- [ ] Autenticación de usuarios básica
- [ ] Integración completa de HTML/CSS previo
- [ ] Formularios con validación Flask-WTF
- [ ] Manejo de sesiones y cookies
- [ ] Mensajes flash para feedback al usuario
- [ ] Diseño responsivo mantenido

---

## 🎯 Entrega de Ejercicios

### Formato de Entrega:
1. **Crear una carpeta** con tu nombre: `ejercicios_[tu_nombre]`
2. **Organizar por ejercicios**:
   ```
   ejercicios_juan_perez/
   ├── ejercicio_1/
   │   └── mi_pagina.html
   ├── ejercicio_2/
   │   └── formulario_registro.html
   ├── ejercicio_3/
   │   └── catalogo_productos.html
   ├── ...
   ├── ejercicio_7/
   │   ├── index.html
   │   ├── productos.html
   │   ├── styles.css
   │   └── main.js
   └── ejercicio_9/
       ├── app.py
       ├── templates/
       ├── static/
       └── requirements.txt
   ```

### Instrucciones de Evaluación:
- **Ejercicios 1-3**: Nivel básico - obligatorios
- **Ejercicios 4-6**: Nivel intermedio - recomendados  
- **Ejercicios 7-9**: Nivel avanzado - opcionales pero muy valorados

### 📝 Rúbrica de Evaluación:

| Criterio | Excelente (4) | Bueno (3) | Satisfactorio (2) | Insuficiente (1) |
|----------|---------------|-----------|-------------------|------------------|
| **HTML Semántico** | Uso perfecto de elementos semánticos | Buen uso con errores menores | Uso básico correcto | Uso incorrecto o ausente |
| **CSS Responsivo** | Diseño perfecto en todos los dispositivos | Funciona bien en la mayoría | Funciona en desktop y móvil | Solo funciona en desktop |
| **JavaScript** | Código limpio y funcional | Funciona con errores menores | Funcionalidad básica | No funciona correctamente |
| **Creatividad** | Diseño original y atractivo | Buena presentación visual | Diseño estándar pero limpio | Diseño básico |
| **Código Limpio** | Código muy bien estructurado | Código bien organizado | Código aceptable | Código desorganizado |

---

## 🚀 Consejos para el Éxito

### Mejores Prácticas:
1. **Planifica antes de programar**: Haz bocetos de tu diseño
2. **Mobile first**: Diseña primero para móvil, luego desktop
3. **Usa comentarios**: Documenta tu código HTML, CSS y JavaScript
4. **Valida tu código**: Usa validadores online para HTML y CSS
5. **Prueba en múltiples navegadores**: Chrome, Firefox, Safari, Edge

### Herramientas Recomendadas:
- **Editor**: VS Code con extensiones HTML/CSS
- **Navegador**: Chrome DevTools para debugging
- **Validadores**: validator.w3.org para HTML, jigsaw.w3.org para CSS
- **Diseño**: Figma para mockups (opcional)

### Recursos de Apoyo:
- [MDN Web Docs](https://developer.mozilla.org/es/)
- [CSS Tricks](https://css-tricks.com/)
- [Flexbox Froggy](https://flexboxfroggy.com/)
- [Grid Garden](https://cssgridgarden.com/)

---

## 🎉 ¡Feliz Codificación!

Estos ejercicios te ayudarán a dominar HTML y CSS, preparándote para crear aplicaciones web profesionales con Flask. 

**Recuerda**: La práctica hace al maestro. No temas experimentar, romper cosas y aprender de los errores.

> *"El único modo de hacer un gran trabajo es amar lo que haces."* - Steve Jobs

---

**¡Mucho éxito con tus ejercicios! 🌟**
