# Guía: Cómo Agregar una Nueva Entidad

Esta guía te enseña paso a paso cómo agregar una nueva entidad (tabla) a tu aplicación Flask.

**Tiempo estimado:** 15-20 minutos

---

## Resumen de Pasos

1. Crear el modelo en `app_flask.py`
2. Crear las rutas CRUD
3. Crear las plantillas HTML
4. Agregar al menú de navegación
5. Probar

---

## Ejemplo: Agregar entidad "Cliente"

Vamos a crear una entidad "Cliente" con: nombre, email, teléfono, activo.

---

## Paso 1: Crear el Modelo

Abre `app_flask.py` y agrega tu modelo después de los modelos existentes:

```python
# ============================================================================
# MODELO: Cliente
# ============================================================================

class Cliente(Base):
    """
    Modelo para clientes.

    Representa un cliente del sistema con sus datos de contacto.
    """
    __tablename__ = 'clientes'

    # Columnas
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20))
    direccion = Column(Text)
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Cliente {self.nombre}>"
```

### Tipos de columnas disponibles

| Tipo | Uso | Ejemplo |
|------|-----|---------|
| `Integer` | Números enteros | `edad = Column(Integer)` |
| `String(n)` | Texto corto (máx n caracteres) | `nombre = Column(String(100))` |
| `Text` | Texto largo | `descripcion = Column(Text)` |
| `Float` | Números decimales | `precio = Column(Float)` |
| `Boolean` | Verdadero/Falso | `activo = Column(Boolean)` |
| `DateTime` | Fecha y hora | `fecha = Column(DateTime)` |

### Opciones de columnas

| Opción | Uso |
|--------|-----|
| `primary_key=True` | Es la clave primaria |
| `nullable=False` | Campo requerido |
| `unique=True` | No permite duplicados |
| `default=valor` | Valor por defecto |
| `ForeignKey('tabla.id')` | Relación con otra tabla |

---

## Paso 2: Crear las Rutas CRUD

Agrega las rutas en `app_flask.py` después de las rutas existentes:

```python
# ============================================================================
# RUTAS CRUD PARA CLIENTES
# ============================================================================

@app.route('/clientes')
def listar_clientes():
    """Lista todos los clientes."""
    session = Session()
    try:
        clientes = session.query(Cliente).order_by(Cliente.nombre).all()
        return render_template('clientes/lista.html', clientes=clientes)
    finally:
        session.close()


@app.route('/clientes/nuevo', methods=['GET', 'POST'])
def crear_cliente():
    """Crea un nuevo cliente."""
    if request.method == 'POST':
        session = Session()
        try:
            cliente = Cliente(
                nombre=request.form['nombre'],
                email=request.form['email'],
                telefono=request.form.get('telefono', ''),
                direccion=request.form.get('direccion', '')
            )
            session.add(cliente)
            session.commit()
            flash(f'Cliente "{cliente.nombre}" creado exitosamente', 'success')
            return redirect(url_for('listar_clientes'))
        except Exception as e:
            session.rollback()
            flash(f'Error: {e}', 'danger')
        finally:
            session.close()

    return render_template('clientes/formulario.html', cliente=None)


@app.route('/clientes/<int:id>')
def ver_cliente(id):
    """Muestra el detalle de un cliente."""
    session = Session()
    try:
        cliente = session.query(Cliente).get(id)
        if not cliente:
            flash('Cliente no encontrado', 'danger')
            return redirect(url_for('listar_clientes'))
        return render_template('clientes/detalle.html', cliente=cliente)
    finally:
        session.close()


@app.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
def editar_cliente(id):
    """Edita un cliente existente."""
    session = Session()
    try:
        cliente = session.query(Cliente).get(id)
        if not cliente:
            flash('Cliente no encontrado', 'danger')
            return redirect(url_for('listar_clientes'))

        if request.method == 'POST':
            cliente.nombre = request.form['nombre']
            cliente.email = request.form['email']
            cliente.telefono = request.form.get('telefono', '')
            cliente.direccion = request.form.get('direccion', '')
            session.commit()
            flash(f'Cliente "{cliente.nombre}" actualizado', 'success')
            return redirect(url_for('listar_clientes'))

        return render_template('clientes/formulario.html', cliente=cliente)
    finally:
        session.close()


@app.route('/clientes/<int:id>/eliminar', methods=['POST'])
def eliminar_cliente(id):
    """Elimina un cliente."""
    session = Session()
    try:
        cliente = session.query(Cliente).get(id)
        if cliente:
            nombre = cliente.nombre
            session.delete(cliente)
            session.commit()
            flash(f'Cliente "{nombre}" eliminado', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Error: {e}', 'danger')
    finally:
        session.close()
    return redirect(url_for('listar_clientes'))
```

---

## Paso 3: Crear las Plantillas HTML

### 3.1 Crear la carpeta

```bash
mkdir templates/clientes
```

### 3.2 Lista (templates/clientes/lista.html)

```html
{% extends "base.html" %}
{% from "macros.html" import page_header, badge_estado, acciones_tabla, empty_state %}

{% block title %}Clientes{% endblock %}

{% block content %}

{{ page_header('Clientes', url_for('crear_cliente'), '+ Nuevo Cliente') }}

{% if clientes %}
    <div class="table-responsive">
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Email</th>
                    <th>Teléfono</th>
                    <th>Estado</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                {% for cliente in clientes %}
                <tr>
                    <td>{{ cliente.id }}</td>
                    <td>
                        <a href="{{ url_for('ver_cliente', id=cliente.id) }}">
                            {{ cliente.nombre }}
                        </a>
                    </td>
                    <td>{{ cliente.email }}</td>
                    <td>{{ cliente.telefono or '-' }}</td>
                    <td>{{ badge_estado(cliente.activo) }}</td>
                    <td>
                        {{ acciones_tabla(
                            url_for('editar_cliente', id=cliente.id),
                            url_for('eliminar_cliente', id=cliente.id)
                        ) }}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
{% else %}
    {{ empty_state('No hay clientes registrados', url_for('crear_cliente')) }}
{% endif %}

{% endblock %}
```

### 3.3 Formulario (templates/clientes/formulario.html)

```html
{% extends "base.html" %}
{% from "macros.html" import campo_texto, campo_textarea, boton %}

{% block title %}
    {% if cliente %}Editar{% else %}Nuevo{% endif %} Cliente
{% endblock %}

{% block content %}

<h1>{% if cliente %}Editar{% else %}Nuevo{% endif %} Cliente</h1>

<div class="card">
    <div class="card-body">
        <form method="POST" class="form">

            {{ campo_texto('nombre', 'Nombre',
                value=cliente.nombre if cliente else '',
                required=true) }}

            {{ campo_texto('email', 'Email',
                value=cliente.email if cliente else '',
                type='email',
                required=true) }}

            {{ campo_texto('telefono', 'Teléfono',
                value=cliente.telefono if cliente else '') }}

            {{ campo_textarea('direccion', 'Dirección',
                value=cliente.direccion if cliente else '') }}

            <div class="form-actions">
                {{ boton('Guardar', 'success', submit=true) }}
                {{ boton('Cancelar', 'secondary', url=url_for('listar_clientes')) }}
            </div>

        </form>
    </div>
</div>

{% endblock %}
```

### 3.4 Detalle (templates/clientes/detalle.html)

```html
{% extends "base.html" %}
{% from "macros.html" import badge_estado, boton, boton_eliminar %}

{% block title %}{{ cliente.nombre }}{% endblock %}

{% block content %}

<div class="card">
    <div class="card-header">
        <h1 class="card-title">{{ cliente.nombre }}</h1>
        {{ badge_estado(cliente.activo) }}
    </div>

    <div class="card-body">
        <p><strong>Email:</strong> {{ cliente.email }}</p>
        <p><strong>Teléfono:</strong> {{ cliente.telefono or 'No registrado' }}</p>
        <p><strong>Dirección:</strong> {{ cliente.direccion or 'No registrada' }}</p>
        <p><strong>Fecha de registro:</strong>
            {{ cliente.fecha_registro.strftime('%d/%m/%Y') if cliente.fecha_registro else 'N/A' }}
        </p>
    </div>

    <div class="card-footer">
        <div class="btn-group">
            {{ boton('Editar', 'primary', url=url_for('editar_cliente', id=cliente.id)) }}
            {{ boton_eliminar(url_for('eliminar_cliente', id=cliente.id)) }}
            {{ boton('Volver', 'secondary', url=url_for('listar_clientes')) }}
        </div>
    </div>
</div>

{% endblock %}
```

---

## Paso 4: Agregar al Menú

Edita `templates/base.html` y agrega el enlace en el navbar:

```html
<div class="navbar-menu">
    <a href="{{ url_for('index') }}">Inicio</a>
    <a href="{{ url_for('listar_categorias') }}">Categorías</a>
    <a href="{{ url_for('listar_productos') }}">Productos</a>
    <a href="{{ url_for('listar_clientes') }}">Clientes</a>  <!-- NUEVO -->
</div>
```

---

## Paso 5: Probar

1. Reinicia la aplicación:
   ```bash
   python app_flask.py
   ```

2. Abre http://localhost:5001/clientes

3. Prueba crear, editar, ver y eliminar clientes

---

## Agregar Relaciones

### Cliente tiene muchos Pedidos

```python
class Cliente(Base):
    __tablename__ = 'clientes'
    # ... columnas ...

    # Relación: un cliente tiene muchos pedidos
    pedidos = relationship("Pedido", back_populates="cliente")


class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, default=0)

    # Clave foránea al cliente
    cliente_id = Column(Integer, ForeignKey('clientes.id'))

    # Relación: un pedido pertenece a un cliente
    cliente = relationship("Cliente", back_populates="pedidos")
```

### Usar la relación en las plantillas

```html
{# Mostrar pedidos del cliente #}
<h2>Pedidos ({{ cliente.pedidos | length }})</h2>
<ul>
{% for pedido in cliente.pedidos %}
    <li>Pedido #{{ pedido.id }} - ${{ pedido.total }}</li>
{% endfor %}
</ul>
```

---

## Checklist

- [ ] Modelo creado en `app_flask.py`
- [ ] Rutas CRUD creadas (listar, crear, ver, editar, eliminar)
- [ ] Plantillas creadas (lista.html, formulario.html, detalle.html)
- [ ] Enlace agregado al menú
- [ ] Aplicación reiniciada
- [ ] Funcionalidad probada

---

## Errores Comunes

### "Table already exists"
La tabla ya existe con otro esquema. Usa `reset=True` en `crear_tablas()`.

### "Column does not exist"
Agregaste una columna al modelo pero la tabla ya existía. Usa `reset=True`.

### "url_for: could not build url"
El nombre de la función en `url_for()` no coincide con el nombre de la ruta.

### "Template not found"
Verifica que la plantilla esté en la carpeta correcta.

---

**¡Listo! Ahora puedes agregar cualquier entidad a tu aplicación.**
