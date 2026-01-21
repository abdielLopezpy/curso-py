# Semana 7: ORM - La Forma Fácil de Trabajar con Bases de Datos

Bienvenido a la Semana 7 del curso. Esta semana descubrirás cómo un **ORM (Object-Relational Mapping)** hace que trabajar con bases de datos sea increíblemente fácil y elegante.

---

## 🎯 Objetivos de Aprendizaje

Al finalizar esta semana serás capaz de:

- Entender qué es un ORM y por qué simplifica tu vida
- Definir modelos de datos como clases Python simples
- Realizar operaciones CRUD sin escribir SQL
- Crear relaciones entre tablas de forma intuitiva
- Ejecutar consultas complejas con sintaxis Python
- Construir sistemas completos de forma rápida y limpia

---

## 🤔 ¿Por qué ORM?

### El Problema con SQL Manual (Semana 6)

En la Semana 6 aprendiste a usar SQLite con SQL manual. Funcionó, pero:

```python
# ❌ SQL Manual - Mucho código repetitivo
cursor.execute("""
    INSERT INTO productos (nombre, precio, stock, categoria_id)
    VALUES (?, ?, ?, ?)
""", (producto.nombre, producto.precio, producto.stock, producto.categoria_id))
conexion.commit()

# Luego para leer...
cursor.execute("SELECT * FROM productos WHERE id = ?", (id,))
fila = cursor.fetchone()
if fila:
    producto = Producto(
        id=fila['id'],
        nombre=fila['nombre'],
        precio=fila['precio'],
        stock=fila['stock'],
        categoria_id=fila['categoria_id']
    )
```

### La Solución con ORM

```python
# ✅ Con ORM - Simple y elegante
session.add(producto)
session.commit()

# Para leer...
producto = session.get(Producto, id)
```

**¡Eso es todo!** El ORM se encarga de:
- Generar el SQL automáticamente
- Convertir filas a objetos Python
- Manejar las conexiones
- Validar tipos de datos

---

## 📁 Estructura del Proyecto

```
Semana_7/
├── README_SEMANA_7.md              👈 Este archivo
├── COMPARATIVA_SQL_VS_ORM.md       👈 SQL manual vs ORM lado a lado
│
├── 01_intro_orm.py                 📖 Paso 1: ¿Qué es un ORM?
├── 02_modelos_basicos.py           📖 Paso 2: Definir modelos
├── 03_crud_simple.py               📖 Paso 3: CRUD sin escribir SQL
├── 04_relaciones.py                📖 Paso 4: Relaciones fáciles
├── 05_consultas_avanzadas.py       📖 Paso 5: Consultas poderosas
├── 06_sistema_completo.py          📖 Paso 6: Sistema completo
│
├── quiz_semana_7.py                🎮 Quiz interactivo
│
└── datos/                          💾 Bases de datos SQLite
    └── [archivos .db se crean aquí]
```

---

## 📚 ¿Qué es un ORM?

**ORM** significa **Object-Relational Mapping** (Mapeo Objeto-Relacional).

Es una técnica que te permite:
- Trabajar con bases de datos usando **objetos Python**
- **No escribir SQL** (el ORM lo genera por ti)
- **Menos código, menos errores, más productividad**

### Analogía Simple

| Sin ORM | Con ORM |
|---------|---------|
| Hablas SQL con la base de datos | Hablas Python con la base de datos |
| Traduces manualmente objetos ↔ filas | El ORM traduce automáticamente |
| Escribes consultas SQL a mano | Escribes código Python intuitivo |

---

## 🐍 SQLAlchemy: El ORM de Python

**SQLAlchemy** es el ORM más popular de Python. Es usado por:
- Instagram
- Dropbox
- Reddit
- Uber
- Y miles de empresas más

### Instalación

```bash
pip install sqlalchemy
```

### Características Principales

| Característica | Beneficio |
|---------------|-----------|
| **Sintaxis Pythónica** | Escribe código Python, no SQL |
| **Múltiples Bases de Datos** | SQLite, PostgreSQL, MySQL, etc. |
| **Relaciones Automáticas** | Define relaciones de forma simple |
| **Validación de Tipos** | Detecta errores antes de ejecutar |
| **Alto Rendimiento** | Optimizado para producción |

---

## 🔄 Comparación Lado a Lado

### Definir una Tabla

**SQL Manual:**
```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL CHECK(precio >= 0),
        stock INTEGER DEFAULT 0
    )
""")
```

**Con ORM:**
```python
class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
```

### Insertar Datos

**SQL Manual:**
```python
cursor.execute(
    "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
    ("Laptop", 999.99, 10)
)
conexion.commit()
```

**Con ORM:**
```python
producto = Producto(nombre="Laptop", precio=999.99, stock=10)
session.add(producto)
session.commit()
```

### Buscar por ID

**SQL Manual:**
```python
cursor.execute("SELECT * FROM productos WHERE id = ?", (1,))
fila = cursor.fetchone()
producto = Producto(
    id=fila['id'],
    nombre=fila['nombre'],
    precio=fila['precio'],
    stock=fila['stock']
)
```

**Con ORM:**
```python
producto = session.get(Producto, 1)
```

### Actualizar

**SQL Manual:**
```python
cursor.execute(
    "UPDATE productos SET precio = ?, stock = ? WHERE id = ?",
    (899.99, 15, 1)
)
conexion.commit()
```

**Con ORM:**
```python
producto.precio = 899.99
producto.stock = 15
session.commit()
```

### Eliminar

**SQL Manual:**
```python
cursor.execute("DELETE FROM productos WHERE id = ?", (1,))
conexion.commit()
```

**Con ORM:**
```python
session.delete(producto)
session.commit()
```

---

## 🔗 Relaciones Entre Tablas

### Sin ORM (Doloroso)

```python
# Crear tablas con FK
cursor.execute("""
    CREATE TABLE productos (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        categoria_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
""")

# Obtener producto con su categoría
cursor.execute("""
    SELECT p.*, c.nombre as categoria_nombre
    FROM productos p
    LEFT JOIN categorias c ON p.categoria_id = c.id
    WHERE p.id = ?
""", (1,))
```

### Con ORM (Fácil)

```python
class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    categoria = relationship("Categoria", back_populates="productos")

# Usar la relación
producto = session.get(Producto, 1)
print(producto.categoria.nombre)  # ¡Acceso directo!

categoria = session.get(Categoria, 1)
for prod in categoria.productos:  # ¡Lista automática!
    print(prod.nombre)
```

---

## 🔍 Consultas Poderosas

### Filtros

```python
# Productos baratos
baratos = session.query(Producto).filter(Producto.precio < 100).all()

# Productos con stock
con_stock = session.query(Producto).filter(Producto.stock > 0).all()

# Búsqueda por nombre
laptops = session.query(Producto).filter(
    Producto.nombre.like("%laptop%")
).all()
```

### Ordenamiento

```python
# Por precio ascendente
productos = session.query(Producto).order_by(Producto.precio).all()

# Por nombre descendente
productos = session.query(Producto).order_by(
    Producto.nombre.desc()
).all()
```

### Agregaciones

```python
from sqlalchemy import func

# Contar productos
total = session.query(func.count(Producto.id)).scalar()

# Precio promedio
promedio = session.query(func.avg(Producto.precio)).scalar()

# Valor total del inventario
valor = session.query(
    func.sum(Producto.precio * Producto.stock)
).scalar()
```

---

## 🚀 Orden de Estudio Recomendado

1. **`01_intro_orm.py`** - Entiende qué es un ORM
2. **`02_modelos_basicos.py`** - Define tus primeros modelos
3. **`03_crud_simple.py`** - Operaciones CRUD sin SQL
4. **`04_relaciones.py`** - Conecta tablas fácilmente
5. **`05_consultas_avanzadas.py`** - Consultas poderosas
6. **`06_sistema_completo.py`** - Sistema integrado

Después:
- **`COMPARATIVA_SQL_VS_ORM.md`** - Referencia rápida
- **`quiz_semana_7.py`** - Evalúa tu conocimiento

---

## 💡 Beneficios del ORM

### 1. Menos Código
- El ORM genera el SQL por ti
- No repites código de mapeo objeto-fila

### 2. Más Seguro
- Previene inyección SQL automáticamente
- Validación de tipos integrada

### 3. Más Mantenible
- El código es más legible
- Los cambios son más fáciles

### 4. Portable
- Cambia de SQLite a PostgreSQL sin cambiar tu código
- El ORM genera el SQL correcto para cada base de datos

### 5. Productivo
- Desarrollas más rápido
- Te enfocas en la lógica de negocio, no en SQL

---

## ⚠️ Cuándo NO Usar ORM

El ORM es excelente para el 90% de los casos, pero:

- **Consultas muy complejas**: A veces SQL raw es más claro
- **Optimización extrema**: Para queries críticos de rendimiento
- **Bases de datos heredadas**: Con esquemas muy raros

Pero para aprender y para la mayoría de proyectos: **¡usa ORM!**

---

## ✅ Checklist de la Semana

### Teoría
- [ ] Entiendo qué es un ORM
- [ ] Sé por qué es más fácil que SQL manual
- [ ] Conozco SQLAlchemy

### Práctica
- [ ] Ejecuté y estudié `01_intro_orm.py`
- [ ] Creé modelos con `02_modelos_basicos.py`
- [ ] Practiqué CRUD con `03_crud_simple.py`
- [ ] Entendí relaciones con `04_relaciones.py`
- [ ] Hice consultas con `05_consultas_avanzadas.py`
- [ ] Revisé el sistema completo

### Comparación
- [ ] Leí `COMPARATIVA_SQL_VS_ORM.md`
- [ ] Entiendo las diferencias con la Semana 6
- [ ] Completé el quiz

---

## 🎓 Próximos Pasos

Después de esta semana estarás listo para:

1. **Frameworks Web**: Flask-SQLAlchemy, FastAPI con SQLAlchemy
2. **Django ORM**: El ORM integrado de Django
3. **Bases de datos avanzadas**: PostgreSQL, MySQL
4. **Migraciones**: Alembic para versionar esquemas
5. **APIs REST**: Crear servicios web con datos persistentes

---

**¡Bienvenido al mundo de los ORMs!** 🎉

> "Un buen desarrollador no escribe SQL innecesario; usa las herramientas adecuadas para ser productivo."
