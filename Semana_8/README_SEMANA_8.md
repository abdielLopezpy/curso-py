# Semana 8: Flask + Neon - Aplicaciones Web con PostgreSQL en la Nube

Bienvenido a la Semana 8 del curso. Esta semana aprenderás a crear **aplicaciones web con Flask** usando **Neon**, una base de datos PostgreSQL serverless moderna y gratuita.

**⚡ NUEVO:** Esta semana también incluye una **introducción completa a HTML y CSS** para que entiendas cómo funcionan los motores de plantillas y puedas crear interfaces web profesionales.

---

## Objetivos de Aprendizaje

Al finalizar esta semana serás capaz de:

- 🌐 **Dominar HTML y CSS** para crear interfaces web modernas
- 🎨 **Entender cómo funcionan los motores de plantillas** (Jinja2)
- 💾 Configurar una base de datos PostgreSQL en Neon (gratis)
- 🔗 Conectar Flask con PostgreSQL usando SQLAlchemy
- 📊 Crear modelos y realizar operaciones CRUD
- 🚀 Construir una aplicación web completa con diseño responsivo
- ➕ Agregar nuevas entidades fácilmente
- 📱 Crear formularios interactivos y componentes reutilizables

---

## ¿Por qué Neon?

### Ventajas de Neon

| Característica | Beneficio |
|----------------|-----------|
| **Serverless** | No necesitas instalar nada en tu PC |
| **Gratuito** | Tier gratuito generoso para aprender |
| **PostgreSQL** | El motor de BD más robusto y usado |
| **Escalable** | Crece automáticamente con tu app |
| **Branching** | Puedes crear "ramas" de tu BD (como Git) |

### SQLite vs PostgreSQL vs Neon

| Aspecto | SQLite (Semana 6-7) | PostgreSQL | Neon |
|---------|---------------------|------------|------|
| Instalación | Ninguna | Compleja | Ninguna |
| Ubicación | Local (archivo) | Local/Servidor | Nube |
| Costo | Gratis | Gratis/Pago | Gratis |
| Producción | No recomendado | Estándar | Moderno |
| Escalabilidad | Limitada | Alta | Automática |

---

## Estructura del Proyecto

```
Semana_8/
├── README_SEMANA_8.md              <-- Este archivo
├── GUIA_HTML_CSS.md                📖 Guía completa de HTML y CSS
├── GUIA_JINJA2.md                  📖 Guía del motor de plantillas
│
├── ejemplos_html_css/              🎯 EJEMPLOS PRÁCTICOS NUEVOS
│   ├── 01_basico.html              HTML básico con ejemplos
│   ├── 02_css_avanzado.html        CSS moderno y responsivo
│   └── 03_flask_integrado.py       Aplicación Flask completa
│
├── 01_intro_neon.py                Paso 1: Conectar con Neon
├── 02_modelos_sqlalchemy.py        Paso 2: Definir modelos
├── 03_crud_basico.py               Paso 3: Operaciones CRUD
├── 04_relaciones.py                Paso 4: Relaciones entre tablas
│
├── app_flask.py                    Aplicación Flask completa
│
├── templates/                      Plantillas HTML
│   ├── base.html                   Plantilla base
│   ├── index.html                  Página principal
│   ├── productos/                  CRUD de productos
│   │   ├── lista.html
│   │   ├── formulario.html
│   │   └── detalle.html
│   └── categorias/                 CRUD de categorías
│       ├── lista.html
│       └── formulario.html
│
└── static/                         Archivos estáticos
    └── css/
        └── styles.css              Estilos CSS avanzados
```

---

## Configuración de Neon (5 minutos)

### Paso 1: Crear cuenta en Neon

1. Ve a: https://neon.tech
2. Clic en "Sign Up" (puedes usar GitHub)
3. Confirma tu email

### Paso 2: Crear un proyecto

1. Clic en "Create Project"
2. Nombre: `curso-python` (o el que quieras)
3. Región: Selecciona la más cercana
4. Clic en "Create Project"

### Paso 3: Obtener la cadena de conexión

1. En el dashboard, verás "Connection Details"
2. Selecciona "Python" en el dropdown
3. Copia la cadena que empieza con `postgresql://`

```
Tu cadena se verá así:
postgresql://usuario:contraseña@ep-xxx.region.aws.neon.tech/neondb?sslmode=require
```

### Paso 4: Configurar en Python

```python
# Guarda tu cadena de conexión (¡no la compartas!)
DATABASE_URL = "postgresql://usuario:contraseña@ep-xxx.region.aws.neon.tech/neondb?sslmode=require"
```

---

## Instalación de Dependencias

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install flask sqlalchemy psycopg2-binary python-dotenv
```

---

## Conexión Básica

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Tu cadena de conexión de Neon
DATABASE_URL = "postgresql://..."

# Crear el engine (conexión)
engine = create_engine(DATABASE_URL)

# Crear la sesión
Session = sessionmaker(bind=engine)

# Base para los modelos
Base = declarative_base()
```

---

## Definir Modelos (Igual que Semana 7)

```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

class Categoria(Base):
    """
    Modelo para categorías de productos.

    Para agregar una nueva entidad:
    1. Crea una clase que herede de Base
    2. Define __tablename__
    3. Define las columnas con Column()
    4. Agrega relaciones si es necesario
    """
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500))

    # Relación: una categoría tiene muchos productos
    productos = relationship("Producto", back_populates="categoria")


class Producto(Base):
    """
    Modelo para productos.
    """
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))

    # Relación: un producto pertenece a una categoría
    categoria = relationship("Categoria", back_populates="productos")
```

---

## CRUD Básico

### Crear
```python
# Crear una categoría
categoria = Categoria(nombre="Electrónica", descripcion="Gadgets y dispositivos")
session.add(categoria)
session.commit()

# Crear un producto
producto = Producto(
    nombre="Laptop Gaming",
    precio=1299.99,
    stock=10,
    categoria_id=categoria.id
)
session.add(producto)
session.commit()
```

### Leer
```python
# Obtener todos
productos = session.query(Producto).all()

# Obtener por ID
producto = session.get(Producto, 1)

# Filtrar
baratos = session.query(Producto).filter(Producto.precio < 100).all()
```

### Actualizar
```python
producto = session.get(Producto, 1)
producto.precio = 999.99
session.commit()
```

### Eliminar
```python
producto = session.get(Producto, 1)
session.delete(producto)
session.commit()
```

---

## Integración con Flask

```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal con lista de productos."""
    productos = session.query(Producto).all()
    return render_template('index.html', productos=productos)

@app.route('/producto/nuevo', methods=['GET', 'POST'])
def nuevo_producto():
    """Crear un nuevo producto."""
    if request.method == 'POST':
        producto = Producto(
            nombre=request.form['nombre'],
            precio=float(request.form['precio']),
            stock=int(request.form['stock'])
        )
        session.add(producto)
        session.commit()
        return redirect(url_for('index'))

    return render_template('productos/formulario.html')
```

---

## Cómo Agregar Nuevas Entidades

### Paso 1: Crear el Modelo

```python
# ============================================================================
# PLANTILLA PARA NUEVA ENTIDAD
# ============================================================================
# Copia esta plantilla y personaliza los campos según tu necesidad.
# ============================================================================

class MiEntidad(Base):
    """
    Descripción de tu entidad.

    Ejemplo: Cliente, Pedido, Empleado, etc.
    """
    __tablename__ = 'mi_entidad'  # Nombre de la tabla (en minúsculas, plural)

    # ------------------------------------------------------------------
    # COLUMNAS BÁSICAS
    # ------------------------------------------------------------------
    id = Column(Integer, primary_key=True)  # Siempre necesitas un ID

    # Campos de texto
    nombre = Column(String(100), nullable=False)      # Requerido
    descripcion = Column(String(500), nullable=True)  # Opcional

    # Campos numéricos
    cantidad = Column(Integer, default=0)
    precio = Column(Float)

    # Campo booleano
    activo = Column(Boolean, default=True)

    # Campo de fecha
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # ------------------------------------------------------------------
    # RELACIONES (Opcional)
    # ------------------------------------------------------------------
    # Si esta entidad pertenece a otra:
    # otra_entidad_id = Column(Integer, ForeignKey('otra_entidad.id'))
    # otra_entidad = relationship("OtraEntidad", back_populates="mis_entidades")

    # ------------------------------------------------------------------
    # MÉTODOS ÚTILES (Opcional)
    # ------------------------------------------------------------------
    def __repr__(self):
        return f"<MiEntidad(id={self.id}, nombre='{self.nombre}')>"
```

### Paso 2: Crear las Rutas

```python
# ============================================================================
# RUTAS CRUD PARA LA NUEVA ENTIDAD
# ============================================================================

# LISTAR todos
@app.route('/mi_entidad')
def listar_mi_entidad():
    items = session.query(MiEntidad).all()
    return render_template('mi_entidad/lista.html', items=items)

# CREAR nuevo
@app.route('/mi_entidad/nuevo', methods=['GET', 'POST'])
def crear_mi_entidad():
    if request.method == 'POST':
        item = MiEntidad(
            nombre=request.form['nombre'],
            descripcion=request.form.get('descripcion', '')
        )
        session.add(item)
        session.commit()
        return redirect(url_for('listar_mi_entidad'))
    return render_template('mi_entidad/formulario.html')

# VER detalle
@app.route('/mi_entidad/<int:id>')
def ver_mi_entidad(id):
    item = session.get(MiEntidad, id)
    return render_template('mi_entidad/detalle.html', item=item)

# EDITAR
@app.route('/mi_entidad/<int:id>/editar', methods=['GET', 'POST'])
def editar_mi_entidad(id):
    item = session.get(MiEntidad, id)
    if request.method == 'POST':
        item.nombre = request.form['nombre']
        item.descripcion = request.form.get('descripcion', '')
        session.commit()
        return redirect(url_for('ver_mi_entidad', id=id))
    return render_template('mi_entidad/formulario.html', item=item)

# ELIMINAR
@app.route('/mi_entidad/<int:id>/eliminar', methods=['POST'])
def eliminar_mi_entidad(id):
    item = session.get(MiEntidad, id)
    session.delete(item)
    session.commit()
    return redirect(url_for('listar_mi_entidad'))
```

### Paso 3: Crear las Plantillas

```html
<!-- templates/mi_entidad/lista.html -->
{% extends "base.html" %}
{% block title %}Mi Entidad{% endblock %}
{% block content %}
<h1>Lista de Mi Entidad</h1>
<a href="{{ url_for('crear_mi_entidad') }}">+ Nuevo</a>
<ul>
{% for item in items %}
    <li>
        <a href="{{ url_for('ver_mi_entidad', id=item.id) }}">{{ item.nombre }}</a>
    </li>
{% endfor %}
</ul>
{% endblock %}
```

---

## 🗺️ Orden de Estudio Recomendado

### Parte 1: Fundamentos Web (NUEVO)
1. **`GUIA_HTML_CSS.md`** - 📖 Leer la guía completa de HTML y CSS
2. **`ejemplos_html_css/01_basico.html`** - 🌐 Abrir en el navegador para ver HTML básico
3. **`ejemplos_html_css/02_css_avanzado.html`** - 🎨 Ver CSS moderno en acción
4. **`ejemplos_html_css/03_flask_integrado.py`** - 🚀 Ejecutar aplicación Flask completa

### Parte 2: Base de Datos y Backend
5. **`01_intro_neon.py`** - 💾 Configurar y probar conexión con Neon
6. **`02_modelos_sqlalchemy.py`** - 📊 Entender los modelos
7. **`03_crud_basico.py`** - ⚙️ Practicar operaciones CRUD
8. **`04_relaciones.py`** - 🔗 Relaciones entre tablas

### Parte 3: Integración Completa
9. **`app_flask.py`** - 🎯 Ejecutar la aplicación completa
10. **`GUIA_JINJA2.md`** - 📖 Dominar el motor de plantillas

---

## 🚀 Ejecutar las Aplicaciones

### Ejemplos HTML/CSS (SIN base de datos)

```bash
# 1. Ver HTML básico
# Abrir ejemplos_html_css/01_basico.html en tu navegador

# 2. Ver CSS avanzado  
# Abrir ejemplos_html_css/02_css_avanzado.html en tu navegador

# 3. Ejecutar aplicación Flask integrada (con datos simulados)
python ejemplos_html_css/03_flask_integrado.py
# Abrir: http://localhost:5000
```

### Aplicación completa con Neon (CON base de datos)

```bash
# Asegúrate de tener las dependencias instaladas
pip install flask sqlalchemy psycopg2-binary python-dotenv

# Ejecutar
python app_flask.py

# Abrir en el navegador
# http://localhost:5000
```

---

## ✅ Checklist de la Semana

### 🌐 Fundamentos Web (NUEVO)
- [ ] Leí la `GUIA_HTML_CSS.md` completa
- [ ] Abrí `01_basico.html` en el navegador
- [ ] Exploré `02_css_avanzado.html` y sus efectos
- [ ] Ejecuté `03_flask_integrado.py` correctamente
- [ ] Entiendo cómo HTML + CSS + Flask trabajan juntos
- [ ] Comprendo el concepto de diseño responsivo
- [ ] Sé crear formularios HTML funcionales

### 💾 Base de Datos y Backend
- [ ] Creé una cuenta en Neon
- [ ] Creé un proyecto y obtuve la cadena de conexión
- [ ] Instalé las dependencias
- [ ] Ejecuté `01_intro_neon.py` y conecté con Neon
- [ ] Entendí los modelos en `02_modelos_sqlalchemy.py`
- [ ] Practiqué CRUD en `03_crud_basico.py`
- [ ] Entendí las relaciones en `04_relaciones.py`
- [ ] Ejecuté `app_flask.py`

### 🎯 Integración y Proyecto
- [ ] Entiendo cómo Jinja2 conecta Python con HTML
- [ ] Sé usar variables, filtros y bucles en plantillas
- [ ] Agregué una nueva entidad al proyecto
- [ ] La aplicación funciona correctamente
- [ ] Puedo crear formularios que envían datos a Flask
- [ ] Entiendo la estructura MVC (Model-View-Controller)

---

## Solución de Problemas

### Error: "connection refused"
- Verifica que copiaste bien la cadena de conexión
- Asegúrate de incluir `?sslmode=require` al final

### Error: "authentication failed"
- La contraseña está en la cadena de conexión de Neon
- Copia la cadena completa desde el dashboard

### Error: "module not found"
- Instala las dependencias: `pip install psycopg2-binary`

---

## 📚 Recursos Adicionales

### HTML y CSS
- [MDN Web Docs - HTML](https://developer.mozilla.org/es/docs/Web/HTML)
- [MDN Web Docs - CSS](https://developer.mozilla.org/es/docs/Web/CSS)
- [CSS Grid Guide](https://css-tricks.com/snippets/css/complete-guide-grid/)
- [Flexbox Guide](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)

### Flask y Jinja2  
- [Documentación de Flask](https://flask.palletsprojects.com/)
- [Documentación de Jinja2](https://jinja.palletsprojects.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)

### Base de Datos
- [Documentación de Neon](https://neon.tech/docs)
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/)

---

---

## 🎉 ¡Felicitaciones!

Al completar esta semana, habrás aprendido:

- ✅ **HTML semántico** para estructurar contenido web
- ✅ **CSS moderno** con Grid, Flexbox y efectos avanzados  
- ✅ **Diseño responsivo** que funciona en móvil, tablet y desktop
- ✅ **Flask** para crear aplicaciones web robustas
- ✅ **Jinja2** para conectar Python con HTML dinámicamente
- ✅ **PostgreSQL en la nube** con Neon
- ✅ **Arquitectura MVC** para organizar tu código

**¡Ahora tienes todas las herramientas para crear aplicaciones web completas y profesionales!**

> *"El diseño no es solo cómo se ve o cómo se siente. El diseño es cómo funciona."* - Steve Jobs

---

**🌟 ¡Bienvenido al desarrollo web full-stack!**
