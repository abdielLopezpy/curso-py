#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación Flask - Ejemplo Práctico de Integración HTML + CSS
=============================================================

Este archivo demuestra cómo integrar HTML y CSS en una aplicación Flask real.
Incluye ejemplos prácticos de:

- Plantillas con herencia
- Formularios con validación
- Datos dinámicos
- Estilos CSS avanzados
- Navegación entre páginas

Para ejecutar:
    python 03_flask_integrado.py

Luego abrir: http://localhost:5000
"""

from flask import Flask, render_template_string, request, redirect, url_for, flash
import os
from datetime import datetime
import random

# ============================================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ============================================================================

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Para mensajes flash

# Datos de ejemplo (simulando base de datos)
productos_db = [
    {
        'id': 1,
        'nombre': 'Laptop Gaming',
        'precio': 1299.99,
        'descripcion': 'Laptop de alta performance para gaming y trabajo profesional',
        'categoria': 'Tecnología',
        'stock': 15,
        'imagen': 'laptop.jpg',
        'destacado': True
    },
    {
        'id': 2,
        'nombre': 'Mouse Inalámbrico',
        'precio': 29.99,
        'descripcion': 'Mouse ergonómico con conectividad Bluetooth',
        'categoria': 'Accesorios',
        'stock': 50,
        'imagen': 'mouse.jpg',
        'destacado': False
    },
    {
        'id': 3,
        'nombre': 'Teclado Mecánico',
        'precio': 89.99,
        'descripcion': 'Teclado mecánico RGB para gamers',
        'categoria': 'Accesorios',
        'stock': 8,
        'imagen': 'teclado.jpg',
        'destacado': True
    },
    {
        'id': 4,
        'nombre': 'Monitor 4K',
        'precio': 399.99,
        'descripcion': 'Monitor 4K de 27 pulgadas para profesionales',
        'categoria': 'Pantallas',
        'stock': 0,
        'imagen': 'monitor.jpg',
        'destacado': False
    }
]

categorias_db = [
    {'id': 1, 'nombre': 'Tecnología', 'descripcion': 'Gadgets y dispositivos'},
    {'id': 2, 'nombre': 'Accesorios', 'descripcion': 'Complementos y accesorios'},
    {'id': 3, 'nombre': 'Pantallas', 'descripcion': 'Monitores y displays'}
]

contactos_db = []  # Para almacenar mensajes de contacto

# ============================================================================
# PLANTILLA BASE
# ============================================================================

template_base = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}TechStore - Tienda de Tecnología{% endblock %}</title>

    <style>
        /* ================================================================
           VARIABLES CSS Y RESET
           ================================================================ */
        :root {
            --color-primary: #3498db;
            --color-secondary: #2c3e50;
            --color-success: #27ae60;
            --color-warning: #f39c12;
            --color-danger: #e74c3c;
            --color-light: #f8f9fa;
            --color-dark: #343a40;
            --color-muted: #6c757d;

            --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            --border-radius: 8px;
            --box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            --transition: all 0.3s ease;
        }

        *, *::before, *::after {
            box-sizing: border-box;
        }

        body {
            font-family: var(--font-family);
            margin: 0;
            padding: 0;
            background-color: var(--color-light);
            line-height: 1.6;
            color: var(--color-dark);
        }

        /* ================================================================
           LAYOUT PRINCIPAL
           ================================================================ */
        .page-container {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* ================================================================
           NAVEGACIÓN
           ================================================================ */
        .navbar {
            background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
            color: white;
            padding: 1rem 0;
            box-shadow: var(--box-shadow);
        }

        .navbar-content {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 1rem;
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
            gap: 2rem;
            margin: 0;
            padding: 0;
        }

        .navbar-menu a {
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: var(--border-radius);
            transition: var(--transition);
        }

        .navbar-menu a:hover,
        .navbar-menu a.active {
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
        }

        /* ================================================================
           CONTENIDO PRINCIPAL
           ================================================================ */
        .main-content {
            flex: 1;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem 1rem;
            width: 100%;
        }

        /* ================================================================
           MENSAJES FLASH
           ================================================================ */
        .alerts {
            margin-bottom: 2rem;
        }

        .alert {
            padding: 1rem;
            border-radius: var(--border-radius);
            margin-bottom: 1rem;
            border-left: 4px solid;
            animation: slideIn 0.3s ease;
        }

        .alert-success {
            background: rgba(39, 174, 96, 0.1);
            color: var(--color-success);
            border-left-color: var(--color-success);
        }

        .alert-danger {
            background: rgba(231, 76, 60, 0.1);
            color: var(--color-danger);
            border-left-color: var(--color-danger);
        }

        .alert-warning {
            background: rgba(243, 156, 18, 0.1);
            color: var(--color-warning);
            border-left-color: var(--color-warning);
        }

        /* ================================================================
           COMPONENTES
           ================================================================ */

        /* Botones */
        .btn {
            display: inline-block;
            padding: 0.75rem 1.5rem;
            background-color: var(--color-primary);
            color: white;
            text-decoration: none;
            border-radius: var(--border-radius);
            border: none;
            cursor: pointer;
            transition: var(--transition);
            font-size: 1rem;
            text-align: center;
        }

        .btn:hover {
            background-color: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
        }

        .btn-success {
            background-color: var(--color-success);
        }

        .btn-success:hover {
            background-color: #229954;
        }

        .btn-danger {
            background-color: var(--color-danger);
        }

        .btn-danger:hover {
            background-color: #c0392b;
        }

        .btn-secondary {
            background-color: var(--color-muted);
        }

        .btn-secondary:hover {
            background-color: #5a6268;
        }

        /* Cards */
        .card {
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            overflow: hidden;
            transition: var(--transition);
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }

        .card-header {
            padding: 1.5rem;
            background: var(--color-light);
            border-bottom: 1px solid #dee2e6;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .card-title {
            margin: 0;
            font-size: 1.25rem;
            color: var(--color-secondary);
        }

        .card-body {
            padding: 1.5rem;
        }

        .card-footer {
            padding: 1rem 1.5rem;
            background: var(--color-light);
            border-top: 1px solid #dee2e6;
            display: flex;
            gap: 0.5rem;
            justify-content: flex-end;
        }

        /* Grid de productos */
        .products-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }

        /* Formularios */
        .form {
            background: white;
            padding: 2rem;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
            color: var(--color-secondary);
        }

        .form-control {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid #dee2e6;
            border-radius: var(--border-radius);
            font-size: 1rem;
            transition: var(--transition);
        }

        .form-control:focus {
            outline: none;
            border-color: var(--color-primary);
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }

        /* Badges */
        .badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            font-size: 0.875rem;
            font-weight: bold;
            border-radius: 4px;
            text-transform: uppercase;
        }

        .badge-success {
            background: var(--color-success);
            color: white;
        }

        .badge-warning {
            background: var(--color-warning);
            color: white;
        }

        .badge-danger {
            background: var(--color-danger);
            color: white;
        }

        .badge-primary {
            background: var(--color-primary);
            color: white;
        }

        /* Utilidades */
        .text-center { text-align: center; }
        .text-muted { color: var(--color-muted); }
        .mb-3 { margin-bottom: 1.5rem; }
        .mt-3 { margin-top: 1.5rem; }
        .price {
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--color-success);
        }

        /* ================================================================
           FOOTER
           ================================================================ */
        .footer {
            background: var(--color-secondary);
            color: white;
            text-align: center;
            padding: 2rem 1rem;
            margin-top: auto;
        }

        /* ================================================================
           RESPONSIVE
           ================================================================ */
        @media (max-width: 768px) {
            .navbar-content {
                flex-direction: column;
                gap: 1rem;
            }

            .navbar-menu {
                gap: 1rem;
            }

            .products-grid {
                grid-template-columns: 1fr;
            }

            .main-content {
                padding: 1rem;
            }
        }

        /* ================================================================
           ANIMACIONES
           ================================================================ */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

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
            animation: fadeIn 0.6s ease;
        }
    </style>

    {% block extra_css %}{% endblock %}
</head>

<body class="page-container">
    <!-- NAVEGACIÓN -->
    <nav class="navbar">
        <div class="navbar-content">
            <a href="{{ url_for('index') }}" class="navbar-brand">
                🛍️ TechStore
            </a>
            <ul class="navbar-menu">
                <li><a href="{{ url_for('index') }}" class="{{ 'active' if request.endpoint == 'index' }}">Inicio</a></li>
                <li><a href="{{ url_for('productos') }}" class="{{ 'active' if request.endpoint == 'productos' }}">Productos</a></li>
                <li><a href="{{ url_for('contacto') }}" class="{{ 'active' if request.endpoint == 'contacto' }}">Contacto</a></li>
                <li><a href="{{ url_for('admin') }}" class="{{ 'active' if request.endpoint == 'admin' }}">Admin</a></li>
            </ul>
        </div>
    </nav>

    <!-- CONTENIDO PRINCIPAL -->
    <main class="main-content">
        <!-- Mensajes Flash -->
        <div class="alerts">
            {% with messages = get_flashed_messages(with_categories=true) %}
                {% if messages %}
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                {% endif %}
            {% endwith %}
        </div>

        {% block content %}
        <p>Contenido por defecto</p>
        {% endblock %}
    </main>

    <!-- FOOTER -->
    <footer class="footer">
        <p>&copy; {{ moment().year if moment else '2024' }} TechStore - Ejemplo Flask + HTML + CSS</p>
        <p>Creado para el curso de Python - Semana 8</p>
    </footer>

    {% block extra_js %}{% endblock %}
</body>
</html>
"""

# ============================================================================
# PLANTILLA DE INICIO
# ============================================================================

template_index = """
{% extends "base.html" %}

{% block title %}Inicio - {{ super() }}{% endblock %}

{% block content %}
<div class="fade-in">
    <!-- HERO SECTION -->
    <section class="text-center mb-3" style="background: linear-gradient(135deg, rgba(52, 152, 219, 0.1), rgba(39, 174, 96, 0.1)); padding: 3rem; border-radius: var(--border-radius); margin-bottom: 3rem;">
        <h1 style="font-size: 2.5rem; margin-bottom: 1rem; color: var(--color-secondary);">
            ¡Bienvenido a TechStore!
        </h1>
        <p style="font-size: 1.2rem; margin-bottom: 2rem; color: var(--color-muted);">
            Los mejores productos tecnológicos al mejor precio
        </p>
        <a href="{{ url_for('productos') }}" class="btn" style="font-size: 1.1rem; padding: 1rem 2rem;">
            Ver Catálogo
        </a>
    </section>

    <!-- ESTADÍSTICAS -->
    <section style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin: 3rem 0;">
        <div class="card text-center">
            <div class="card-body">
                <h3 style="font-size: 2rem; color: var(--color-primary); margin: 0;">{{ stats.total_productos }}</h3>
                <p style="margin: 0.5rem 0 0 0; color: var(--color-muted);">Productos</p>
            </div>
        </div>
        <div class="card text-center">
            <div class="card-body">
                <h3 style="font-size: 2rem; color: var(--color-success); margin: 0;">{{ stats.disponibles }}</h3>
                <p style="margin: 0.5rem 0 0 0; color: var(--color-muted);">Disponibles</p>
            </div>
        </div>
        <div class="card text-center">
            <div class="card-body">
                <h3 style="font-size: 2rem; color: var(--color-warning); margin: 0;">{{ stats.categorias }}</h3>
                <p style="margin: 0.5rem 0 0 0; color: var(--color-muted);">Categorías</p>
            </div>
        </div>
        <div class="card text-center">
            <div class="card-body">
                <h3 style="font-size: 2rem; color: var(--color-primary); margin: 0;">4.8/5</h3>
                <p style="margin: 0.5rem 0 0 0; color: var(--color-muted);">Calificación</p>
            </div>
        </div>
    </section>

    <!-- PRODUCTOS DESTACADOS -->
    <section>
        <h2 style="text-align: center; margin: 3rem 0 2rem 0; color: var(--color-secondary);">
            🌟 Productos Destacados
        </h2>

        <div class="products-grid">
            {% for producto in productos_destacados %}
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">{{ producto.nombre }}</h3>
                    <span class="badge badge-primary">Destacado</span>
                </div>
                <div class="card-body">
                    <p style="color: var(--color-muted); margin-bottom: 1rem;">{{ producto.descripcion }}</p>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <span class="price">${{ "%.2f"|format(producto.precio) }}</span>
                        {% if producto.stock > 0 %}
                            <span class="badge badge-success">Stock: {{ producto.stock }}</span>
                        {% else %}
                            <span class="badge badge-danger">Agotado</span>
                        {% endif %}
                    </div>
                    <div style="font-size: 0.9rem; color: var(--color-muted);">
                        <strong>Categoría:</strong> {{ producto.categoria }}
                    </div>
                </div>
                <div class="card-footer">
                    <a href="{{ url_for('detalle_producto', id=producto.id) }}" class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">Ver Detalles</a>
                    {% if producto.stock > 0 %}
                        <button class="btn" style="padding: 0.5rem 1rem; font-size: 0.9rem;" onclick="alert('¡Agregado al carrito! (Funcionalidad simulada)')">Agregar</button>
                    {% else %}
                        <button class="btn" disabled style="opacity: 0.5; cursor: not-allowed; padding: 0.5rem 1rem; font-size: 0.9rem;">Sin Stock</button>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    </section>

    <!-- CALL TO ACTION -->
    <section class="text-center" style="background: white; padding: 3rem; border-radius: var(--border-radius); box-shadow: var(--box-shadow); margin: 3rem 0;">
        <h3 style="margin-bottom: 1rem; color: var(--color-secondary);">¿Necesitas ayuda?</h3>
        <p style="margin-bottom: 2rem; color: var(--color-muted);">Nuestro equipo está listo para ayudarte</p>
        <a href="{{ url_for('contacto') }}" class="btn btn-success" style="font-size: 1.1rem; padding: 1rem 2rem;">Contáctanos</a>
    </section>
</div>
{% endblock %}
"""

# ============================================================================
# PLANTILLA DE PRODUCTOS
# ============================================================================

template_productos = """
{% extends "base.html" %}

{% block title %}Productos - {{ super() }}{% endblock %}

{% block content %}
<div class="fade-in">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <h1 style="color: var(--color-secondary); margin: 0;">📦 Catálogo de Productos</h1>
        <div style="color: var(--color-muted);">{{ productos|length }} productos encontrados</div>
    </div>

    <!-- FILTROS -->
    <div class="card mb-3">
        <div class="card-body">
            <form method="GET" style="display: grid; grid-template-columns: 1fr 1fr auto; gap: 1rem; align-items: end;">
                <div class="form-group" style="margin-bottom: 0;">
                    <label for="categoria" class="form-label">Filtrar por categoría:</label>
                    <select id="categoria" name="categoria" class="form-control">
                        <option value="">Todas las categorías</option>
                        {% for cat in categorias %}
                            <option value="{{ cat.nombre }}" {{ 'selected' if request.args.get('categoria') == cat.nombre }}>
                                {{ cat.nombre }}
                            </option>
                        {% endfor %}
                    </select>
                </div>

                <div class="form-group" style="margin-bottom: 0;">
                    <label for="disponible" class="form-label">Disponibilidad:</label>
                    <select id="disponible" name="disponible" class="form-control">
                        <option value="">Todos</option>
                        <option value="si" {{ 'selected' if request.args.get('disponible') == 'si' }}>Solo disponibles</option>
                        <option value="no" {{ 'selected' if request.args.get('disponible') == 'no' }}>Solo agotados</option>
                    </select>
                </div>

                <div>
                    <button type="submit" class="btn">Filtrar</button>
                </div>
            </form>
        </div>
    </div>

    {% if productos %}
        <div class="products-grid">
            {% for producto in productos %}
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">{{ producto.nombre }}</h3>
                    <div>
                        {% if producto.destacado %}
                            <span class="badge badge-warning">⭐ Destacado</span>
                        {% endif %}
                        {% if producto.stock > 10 %}
                            <span class="badge badge-success">Disponible</span>
                        {% elif producto.stock > 0 %}
                            <span class="badge badge-warning">Poco Stock</span>
                        {% else %}
                            <span class="badge badge-danger">Agotado</span>
                        {% endif %}
                    </div>
                </div>

                <div class="card-body">
                    <p style="font-size: 1.1rem; margin-bottom: 2rem; line-height: 1.8;">{{ producto.descripcion }}</p>

                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-bottom: 2rem;">
                        <div>
                            <h4 style="color: var(--color-secondary); margin-bottom: 1rem;">Especificaciones</h4>
                            <table style="width: 100%; font-size: 0.9rem;">
                                <tr>
                                    <td style="padding: 0.5rem 0; color: var(--color-muted);"><strong>Precio:</strong></td>
                                    <td style="padding: 0.5rem 0;"><span class="price" style="font-size: 1.2rem;">${{ "%.2f"|format(producto.precio) }}</span></td>
                                </tr>
                                <tr>
                                    <td style="padding: 0.5rem 0; color: var(--color-muted);"><strong>Stock:</strong></td>
                                    <td style="padding: 0.5rem 0;">{{ producto.stock }} unidades</td>
                                </tr>
                                <tr>
                                    <td style="padding: 0.5rem 0; color: var(--color-muted);"><strong>Categoría:</strong></td>
                                    <td style="padding: 0.5rem 0;">{{ producto.categoria }}</td>
                                </tr>
                                <tr>
                                    <td style="padding: 0.5rem 0; color: var(--color-muted);"><strong>ID:</strong></td>
                                    <td style="padding: 0.5rem 0;">#{{ producto.id }}</td>
                                </tr>
                            </table>
                        </div>

                        <div>
                            <h4 style="color: var(--color-secondary); margin-bottom: 1rem;">Estado</h4>
                            <div style="font-size: 0.9rem;">
                                {% if producto.stock > 10 %}
                                    <div style="color: var(--color-success); margin-bottom: 0.5rem;">✅ En stock</div>
                                    <p style="color: var(--color-muted);">Producto disponible para envío inmediato</p>
                                {% elif producto.stock > 0 %}
                                    <div style="color: var(--color-warning); margin-bottom: 0.5rem;">⚠️ Pocas unidades</div>
                                    <p style="color: var(--color-muted);">Solo quedan {{ producto.stock }} unidades</p>
                                {% else %}
                                    <div style="color: var(--color-danger); margin-bottom: 0.5rem;">❌ Agotado</div>
                                    <p style="color: var(--color-muted);">Producto temporalmente sin stock</p>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card-footer" style="justify-content: space-between;">
                    <a href="{{ url_for('productos') }}" class="btn btn-secondary">← Volver al catálogo</a>
                    <div style="display: flex; gap: 1rem;">
                        {% if producto.stock > 0 %}
                            <button class="btn btn-success" onclick="agregarAlCarrito({{ producto.id }})">Agregar al Carrito</button>
                            <button class="btn" onclick="comprarAhora({{ producto.id }})">Comprar Ahora</button>
                        {% else %}
                            <button class="btn" disabled style="opacity: 0.5; cursor: not-allowed;">Sin Stock</button>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- PRODUCTOS RELACIONADOS -->
    <section>
        <h3 style="color: var(--color-secondary); margin: 3rem 0 2rem 0;">Productos Relacionados</h3>
        <div class="products-grid" style="grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));">
            {% for p in productos_relacionados %}
            <div class="card">
                <div class="card-header">
                    <h4 class="card-title" style="font-size: 1rem;">{{ p.nombre }}</h4>
                    {% if p.stock > 0 %}
                        <span class="badge badge-success">Disponible</span>
                    {% else %}
                        <span class="badge badge-danger">Agotado</span>
                    {% endif %}
                </div>
                <div class="card-body">
                    <p style="font-size: 0.9rem; color: var(--color-muted);">{{ p.descripcion[:60] }}...</p>
                    <span class="price" style="font-size: 1.1rem;">${{ "%.2f"|format(p.precio) }}</span>
                </div>
                <div class="card-footer">
                    <a href="{{ url_for('detalle_producto', id=p.id) }}" class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">Ver</a>
                </div>
            </div>
            {% endfor %}
        </div>
    </section>
</div>

<script>
function agregarAlCarrito(productoId) {
    alert(`¡Producto #${productoId} agregado al carrito!\n(Funcionalidad simulada)`);
}

function comprarAhora(productoId) {
    if (confirm('¿Proceder con la compra?\n(Esta es una funcionalidad simulada)')) {
        alert(`¡Compra iniciada para producto #${productoId}!`);
    }
}
</script>
{% endblock %}
"""

# ============================================================================
# PLANTILLA DE CONTACTO
# ============================================================================

template_contacto = """
{% extends "base.html" %}

{% block title %}Contacto - {{ super() }}{% endblock %}

{% block content %}
<div class="fade-in">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem;">
        <!-- FORMULARIO DE CONTACTO -->
        <div>
            <h1 style="color: var(--color-secondary); margin-bottom: 2rem;">📞 Contáctanos</h1>

            <form class="form" method="POST">
                <div class="form-group">
                    <label for="nombre" class="form-label">Nombre completo *</label>
                    <input type="text" id="nombre" name="nombre" class="form-control"
                           value="{{ request.form.get('nombre', '') if request.method == 'POST' }}" required>
                </div>

                <div class="form-group">
                    <label for="email" class="form-label">Correo electrónico *</label>
                    <input type="email" id="email" name="email" class="form-control"
                           value="{{ request.form.get('email', '') if request.method == 'POST' }}" required>
                </div>

                <div class="form-group">
                    <label for="telefono" class="form-label">Teléfono</label>
                    <input type="tel" id="telefono" name="telefono" class="form-control"
                           value="{{ request.form.get('telefono', '') if request.method == 'POST' }}">
                </div>

                <div class="form-group">
                    <label for="asunto" class="form-label">Asunto *</label>
                    <select id="asunto" name="asunto" class="form-control" required>
                        <option value="">Selecciona un asunto</option>
                        <option value="consulta" {{ 'selected' if request.form.get('asunto') == 'consulta' }}>Consulta general</option>
                        <option value="soporte" {{ 'selected' if request.form.get('asunto') == 'soporte' }}>Soporte técnico</option>
                        <option value="venta" {{ 'selected' if request.form.get('asunto') == 'venta' }}>Información de venta</option>
                        <option value="reclamo" {{ 'selected' if request.form.get('asunto') == 'reclamo' }}>Reclamo</option>
                        <option value="otro" {{ 'selected' if request.form.get('asunto') == 'otro' }}>Otro</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="mensaje" class="form-label">Mensaje *</label>
                    <textarea id="mensaje" name="mensaje" class="form-control" rows="6" required
                              placeholder="Describe tu consulta o mensaje...">{{ request.form.get('mensaje', '') if request.method == 'POST' }}</textarea>
                </div>

                <div class="form-group">
                    <input type="checkbox" id="newsletter" name="newsletter" value="si"
                           {{ 'checked' if request.form.get('newsletter') }}>
                    <label for="newsletter" style="display: inline; margin-left: 0.5rem;">
                        Quiero recibir novedades y promociones por email
                    </label>
                </div>

                <div style="display: flex; gap: 1rem;">
                    <button type="submit" class="btn" style="flex: 1;">Enviar Mensaje</button>
                    <button type="reset" class="btn btn-secondary">Limpiar</button>
                </div>
            </form>
        </div>

        <!-- INFORMACIÓN DE CONTACTO -->
        <div>
            <h2 style="color: var(--color-secondary); margin-bottom: 2rem;">📍 Información</h2>

            <div class="card mb-3">
                <div class="card-body">
                    <h4 style="color: var(--color-primary); margin-bottom: 1rem;">🏢 Dirección</h4>
                    <p>Av. Tecnología 123<br>
                    Ciudad de Buenos Aires<br>
                    CP: 1000<br>
                    Argentina</p>
                </div>
            </div>

            <div class="card mb-3">
                <div class="card-body">
                    <h4 style="color: var(--color-primary); margin-bottom: 1rem;">📞 Teléfonos</h4>
                    <p><strong>Ventas:</strong> +54 11 1234-5678<br>
                    <strong>Soporte:</strong> +54 11 8765-4321<br>
                    <strong>WhatsApp:</strong> +54 9 11 9999-8888</p>
                </div>
            </div>

            <div class="card mb-3">
                <div class="card-body">
                    <h4 style="color: var(--color-primary); margin-bottom: 1rem;">✉️ Emails</h4>
                    <p><strong>General:</strong> info@techstore.com<br>
                    <strong>Ventas:</strong> ventas@techstore.com<br>
                    <strong>Soporte:</strong> soporte@techstore.com</p>
                </div>
            </div>

            <div class="card">
                <div class="card-body">
                    <h4 style="color: var(--color-primary); margin-bottom: 1rem;">🕒 Horarios</h4>
                    <p><strong>Lunes a Viernes:</strong> 9:00 - 18:00<br>
                    <strong>Sábados:</strong> 10:00 - 16:00<br>
                    <strong>Domingos:</strong> Cerrado</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""

# ============================================================================
# PLANTILLA DE ADMINISTRACIÓN
# ============================================================================

template_admin = """
{% extends "base.html" %}

{% block title %}Administración - {{ super() }}{% endblock %}

{% block content %}
<div class="fade-in">
    <h1 style="color: var(--color-secondary); margin-bottom: 2rem;">⚙️ Panel de Administración</h1>

    <!-- ESTADÍSTICAS -->
    <section style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 3rem;">
        <div class="card text-center">
            <div class="card-body">
                <h3 style="font-size: 2rem; color: var(--color-primary); margin: 0;">{{ stats.total_productos }}</h3>
                <p style="margin: 0.5rem 0 0 0; color: var(--color-muted);">Total Productos</p>
            </div>
        </div>
        <div class="card text-center">
            <div class="card-body">
                <h3 style="font-size: 2rem; color: var(--color-success); margin: 0;">{{ stats.disponibles }}</h3>
                <p style="margin: 0.5rem 0 0 0; color: var(--color-muted);">Disponibles</p>
            </div>
        </div>
        <div class="card text-center">
            <div class="card-body">
                <h3 style="font-size: 2rem; color: var(--color-danger); margin: 0;">{{ stats.agotados }}</h3>
                <p style="margin: 0.5rem 0 0 0; color: var(--color-muted);">Agotados</p>
            </div>
        </div>
        <div class="card text-center">
            <div class="card-body">
                <h3 style="font-size: 2rem; color: var(--color-warning); margin: 0;">{{ contactos|length }}</h3>
                <p style="margin: 0.5rem 0 0 0; color: var(--color-muted);">Mensajes</p>
            </div>
        </div>
    </section>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;">
        <!-- LISTA DE PRODUCTOS -->
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">📦 Gestión de Productos</h3>
            </div>
            <div class="card-body">
                <div style="max-height: 400px; overflow-y: auto;">
                    {% for producto in productos %}
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; border-bottom: 1px solid #eee;">
                        <div>
                            <strong>{{ producto.nombre }}</strong>
                            <div style="font-size: 0.9rem; color: var(--color-muted);">
                                ${{ "%.2f"|format(producto.precio) }} - Stock: {{ producto.stock }}
                            </div>
                        </div>
                        <div>
                            {% if producto.stock > 10 %}
                                <span class="badge badge-success">OK</span>
                            {% elif producto.stock > 0 %}
                                <span class="badge badge-warning">Bajo</span>
                            {% else %}
                                <span class="badge badge-danger">Sin Stock</span>
                            {% endif %}
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            <div class="card-footer">
                <button class="btn" onclick="alert('Función de agregar producto (simulada)')">+ Nuevo Producto</button>
            </div>
        </div>

        <!-- MENSAJES DE CONTACTO -->
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">💬 Mensajes de Contacto</h3>
            </div>
            <div class="card-body">
                {% if contactos %}
                <div style="max-height: 400px; overflow-y: auto;">
                    {% for contacto in contactos %}
                    <div style="border: 1px solid #eee; border-radius: var(--border-radius); padding: 1rem; margin-bottom: 1rem;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                            <strong>{{ contacto.nombre }}</strong>
                            <span class="badge badge-{{ 'primary' if contacto.asunto == 'consulta' else 'warning' if contacto.asunto == 'soporte' else 'info' }}">
                                {{ contacto.asunto|title }}
                            </span>
                        </div>
                        <div style="font-size: 0.9rem; color: var(--color-muted); margin-bottom: 0.5rem;">
                            {{ contacto.email }} | {{ contacto.fecha.strftime('%d/%m/%Y %H:%M') }}
                        </div>
                        <p style="font-size: 0.9rem; margin: 0;">{{ contacto.mensaje[:100] }}{% if contacto.mensaje|length > 100 %}...{% endif %}</p>
                    </div>
                    {% endfor %}
                </div>
                {% else %}
                <p class="text-muted text-center" style="padding: 2rem;">No hay mensajes aún</p>
                {% endif %}
            </div>
        </div>
    </div>

    <!-- ACCIONES RÁPIDAS -->
    <section style="margin-top: 2rem;">
        <h3 style="color: var(--color-secondary); margin-bottom: 1rem;">🚀 Acciones Rápidas</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
            <button class="btn" onclick="actualizarStock()" style="padding: 1.5rem; font-size: 1.1rem;">
                📊 Actualizar Stock
            </button>
            <button class="btn btn-success" onclick="generarReporte()" style="padding: 1.5rem; font-size: 1.1rem;">
                📄 Generar Reporte
            </button>
            <button class="btn btn-secondary" onclick="exportarDatos()" style="padding: 1.5rem; font-size: 1.1rem;">
                💾 Exportar Datos
            </button>
            <button class="btn btn-danger" onclick="limpiarCache()" style="padding: 1.5rem; font-size: 1.1rem;">
                🗑️ Limpiar Cache
            </button>
        </div>
    </section>
</div>

<script>
function actualizarStock() {
    alert('Actualizando stock de todos los productos...\n(Funcionalidad simulada)');
}

function generarReporte() {
    alert('Generando reporte de ventas...\n(Funcionalidad simulada)');
}

function exportarDatos() {
    alert('Exportando datos a CSV...\n(Funcionalidad simulada)');
}

function limpiarCache() {
    if (confirm('¿Estás seguro de limpiar el cache?')) {
        alert('Cache limpiado correctamente\n(Funcionalidad simulada)');
    }
}
</script>
{% endblock %}
"""

# ============================================================================
# RUTAS DE LA APLICACIÓN FLASK
# ============================================================================

@app.route('/')
def index():
    """Página de inicio con productos destacados"""
    productos_destacados = [p for p in productos_db if p.get('destacado', False)]

    # Estadísticas para la página principal
    stats = {
        'total_productos': len(productos_db),
        'disponibles': len([p for p in productos_db if p['stock'] > 0]),
        'categorias': len(set(p['categoria'] for p in productos_db))
    }

    return render_template_string(
        template_base + template_index,
        productos_destacados=productos_destacados,
        stats=stats
    )

@app.route('/productos')
def productos():
    """Página del catálogo de productos con filtros"""
    # Obtener filtros de la URL
    categoria_filter = request.args.get('categoria', '')
    disponible_filter = request.args.get('disponible', '')

    # Filtrar productos
    productos_filtrados = productos_db.copy()

    if categoria_filter:
        productos_filtrados = [p for p in productos_filtrados if p['categoria'] == categoria_filter]

    if disponible_filter == 'si':
        productos_filtrados = [p for p in productos_filtrados if p['stock'] > 0]
    elif disponible_filter == 'no':
        productos_filtrados = [p for p in productos_filtrados if p['stock'] == 0]

    return render_template_string(
        template_base + template_productos,
        productos=productos_filtrados,
        categorias=categorias_db
    )

@app.route('/producto/<int:id>')
def detalle_producto(id):
    """Página de detalle de un producto específico"""
    producto = next((p for p in productos_db if p['id'] == id), None)

    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos'))

    # Productos relacionados (misma categoría, excluyendo el actual)
    productos_relacionados = [
        p for p in productos_db
        if p['categoria'] == producto['categoria'] and p['id'] != id
    ][:3]  # Solo los primeros 3

    return render_template_string(
        template_base + template_detalle,
        producto=producto,
        productos_relacionados=productos_relacionados
    )

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    """Página de contacto con formulario"""
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        telefono = request.form.get('telefono', '').strip()
        asunto = request.form.get('asunto', '').strip()
        mensaje = request.form.get('mensaje', '').strip()
        newsletter = request.form.get('newsletter') == 'si'

        # Validación básica
        if not all([nombre, email, asunto, mensaje]):
            flash('Por favor completa todos los campos obligatorios', 'danger')
        else:
            # Simular guardado del mensaje
            nuevo_contacto = {
                'id': len(contactos_db) + 1,
                'nombre': nombre,
                'email': email,
                'telefono': telefono,
                'asunto': asunto,
                'mensaje': mensaje,
                'newsletter': newsletter,
                'fecha': datetime.now()
            }
            contactos_db.append(nuevo_contacto)

            flash(f'¡Gracias {nombre}! Tu mensaje ha sido enviado correctamente.', 'success')
            return redirect(url_for('contacto'))

    return render_template_string(template_base + template_contacto)

@app.route('/admin')
def admin():
    """Panel de administración"""
    # Estadísticas para el admin
    stats = {
        'total_productos': len(productos_db),
        'disponibles': len([p for p in productos_db if p['stock'] > 0]),
        'agotados': len([p for p in productos_db if p['stock'] == 0]),
        'poco_stock': len([p for p in productos_db if 0 < p['stock'] <= 5])
    }

    return render_template_string(
        template_base + template_admin,
        productos=productos_db,
        contactos=contactos_db,
        stats=stats
    )

# ============================================================================
# FILTROS PERSONALIZADOS PARA JINJA2
# ============================================================================

@app.template_filter('currency')
def currency_filter(amount):
    """Filtro para formatear moneda"""
    return f"${amount:,.2f}"

@app.template_filter('datetime')
def datetime_filter(date, format='%d/%m/%Y'):
    """Filtro para formatear fechas"""
    return date.strftime(format)

# ============================================================================
# CONTEXTO GLOBAL PARA TODAS LAS PLANTILLAS
# ============================================================================

@app.context_processor
def inject_globals():
    """Inyectar variables globales en todas las plantillas"""
    return {
        'moment': datetime,
        'current_year': datetime.now().year,
        'app_name': 'TechStore'
    }

# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def page_not_found(error):
    """Página de error 404"""
    error_template = """
    {% extends "base.html" %}

    {% block title %}Página no encontrada - {{ super() }}{% endblock %}

    {% block content %}
    <div class="text-center fade-in" style="padding: 3rem;">
        <div class="card" style="max-width: 500px; margin: 0 auto;">
            <div class="card-body" style="padding: 3rem;">
                <h1 style="font-size: 4rem; color: var(--color-primary); margin-bottom: 1rem;">404</h1>
                <h2 style="color: var(--color-secondary); margin-bottom: 1rem;">Página no encontrada</h2>
                <p class="text-muted" style="margin-bottom: 2rem;">
                    Lo sentimos, la página que buscas no existe.
                </p>
                <a href="{{ url_for('index') }}" class="btn" style="margin-right: 1rem;">🏠 Volver al inicio</a>
                <a href="{{ url_for('productos') }}" class="btn btn-secondary">📦 Ver productos</a>
            </div>
        </div>
    </div>
    {% endblock %}
    """
    return render_template_string(template_base + error_template), 404

@app.errorhandler(500)
def internal_error(error):
    """Página de error 500"""
    return render_template_string("""
    {% extends "base.html" %}

    {% block content %}
    <div class="text-center" style="padding: 3rem;">
        <h1>Error interno del servidor</h1>
        <p>Algo salió mal. Por favor intenta nuevamente.</p>
        <a href="{{ url_for('index') }}" class="btn">Volver al inicio</a>
    </div>
    {% endblock %}
    """), 500

# ============================================================================
# CONFIGURACIÓN Y EJECUCIÓN
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 INICIANDO APLICACIÓN FLASK - EJEMPLO HTML + CSS")
    print("=" * 70)
    print()
    print("📋 INFORMACIÓN DE LA APLICACIÓN:")
    print(f"   • Productos en catálogo: {len(productos_db)}")
    print(f"   • Categorías disponibles: {len(categorias_db)}")
    print(f"   • Productos destacados: {len([p for p in productos_db if p.get('destacado')])}")
    print()
    print("🌐 PÁGINAS DISPONIBLES:")
    print("   • http://localhost:5000/           - Página de inicio")
    print("   • http://localhost:5000/productos  - Catálogo de productos")
    print("   • http://localhost:5000/contacto   - Formulario de contacto")
    print("   • http://localhost:5000/admin      - Panel de administración")
    print()
    print("✨ CARACTERÍSTICAS INCLUIDAS:")
    print("   • ✅ HTML semántico y estructurado")
    print("   • ✅ CSS moderno con variables y efectos")
    print("   • ✅ Diseño responsivo (móvil, tablet, desktop)")
    print("   • ✅ Formularios con validación")
    print("   • ✅ Navegación dinámica")
    print("   • ✅ Plantillas con herencia Jinja2")
    print("   • ✅ Mensajes flash")
    print("   • ✅ Filtros y datos dinámicos")
    print()
    print("🎯 ESTE EJEMPLO DEMUESTRA:")
    print("   • Cómo integrar HTML y CSS en Flask")
    print("   • Uso de plantillas con Jinja2")
    print("   • Formularios y validación")
    print("   • Navegación entre páginas")
    print("   • Diseño responsivo moderno")
    print()
    print("=" * 70)
    print("🌟 ¡Aplicación lista! Abre tu navegador en http://localhost:5000")
    print("=" * 70)
    print()

    # Ejecutar la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)
                        {% endif %}
                    </div>
                </div>

                <div class="card-body">
                    <p style="color: var(--color-muted); margin-bottom: 1rem; min-height: 3rem;">{{ producto.descripcion }}</p>

                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <span class="price">${{ "%.2f"|format(producto.precio) }}</span>
                        <span style="font-size: 0.9rem; color: var(--color-muted);">Stock: {{ producto.stock }}</span>
                    </div>

                    <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: var(--color-muted);">
                        <span><strong>Categoría:</strong> {{ producto.categoria }}</span>
                        <span><strong>ID:</strong> #{{ producto.id }}</span>
                    </div>
                </div>

                <div class="card-footer">
                    <a href="{{ url_for('detalle_producto', id=producto.id) }}" class="btn btn-secondary" style="padding: 0.5rem 1rem; font-size: 0.9rem;">Ver Detalles</a>
                    {% if producto.stock > 0 %}
                        <button class="btn" style="padding: 0.5rem 1rem; font-size: 0.9rem;" onclick="agregarAlCarrito({{ producto.id }})">+ Carrito</button>
                    {% else %}
                        <button class="btn" disabled style="opacity: 0.5; cursor: not-allowed; padding: 0.5rem 1rem; font-size: 0.9rem;">Sin Stock</button>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="card text-center" style="padding: 3rem;">
            <div class="card-body">
                <h3>No se encontraron productos</h3>
                <p class="text-muted">Intenta cambiar los filtros o <a href="{{ url_for('productos') }}">ver todos los productos</a></p>
            </div>
        </div>
    {% endif %}
</div>

<script>
function agregarAlCarrito(productoId) {
    // Simular agregar al carrito
    alert(`¡Producto #${productoId} agregado al carrito!\n(Esta es una funcionalidad simulada)`);

    // En una aplicación real, aquí harías una petición AJAX al servidor
    // fetch('/api/carrito/agregar', {
    //     method: 'POST',
    //     headers: {'Content-Type': 'application/json'},
    //     body: JSON.stringify({producto_id: productoId})
    // });
}
</script>
{% endblock %}
"""

# ============================================================================
# PLANTILLA DE DETALLE DE PRODUCTO
# ============================================================================

template_detalle = """
{% extends "base.html" %}

{% block title %}{{ producto.nombre }} - {{ super() }}{% endblock %}

{% block content %}
<div class="fade-in">
    <!-- Breadcrumb -->
    <nav style="margin-bottom: 2rem; color: var(--color-muted);">
        <a href="{{ url_for('index') }}" style="color: var(--color-primary); text-decoration: none;">Inicio</a> >
        <a href="{{ url_for('productos') }}" style="color: var(--color-primary); text-decoration: none;">Productos</a> >
        <span>{{ producto.nombre }}</span>
    </nav>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; margin-bottom: 3rem;">
        <!-- IMAGEN DEL PRODUCTO (Simulada) -->
        <div class="card">
            <div class="card-body text-center" style="padding: 3rem;">
                <div style="font-size: 8rem; color: var(--color-light); margin-bottom: 1rem;">
                    {% if producto.categoria == 'Tecnología' %}📱
                    {% elif producto.categoria == 'Accesorios' %}🖱️
                    {% elif producto.categoria == 'Pantallas' %}🖥️
                    {% else %}📦
                    {% endif %}
                </div>
                <p class="text-muted"><em>Imagen del producto: {{ producto.imagen }}</em></p>
                <p style="font-size: 0.9rem; color: var(--color-muted);">
                    En una aplicación real, aquí se mostraría la imagen real del producto
                </p>
            </div>
        </div>

        <!-- INFORMACIÓN DEL PRODUCTO -->
        <div>
            <div class="card">
                <div class="card-header">
                    <h1 class="card-title" style="font-size: 2rem;">{{ producto.nombre }}</h1>
                    <div>
                        {% if producto.destacado %}
                            <span class="badge badge-warning">⭐ Destacado</span>
                        {% endif %}
                        {% if producto.stock > 10 %}
                            <span class="badge badge-success">Disponible</span>
                        {% elif producto.stock > 0 %}
                            <span class="badge badge-warning">Poco Stock</span>
                        {% else %}
                            <span class="badge badge-danger">Agotado
