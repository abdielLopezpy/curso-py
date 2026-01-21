# Comparativa: SQL Manual vs ORM

Esta guía muestra lado a lado cómo se hacen las mismas operaciones con SQL manual (Semana 6) y con ORM (Semana 7).

---

## Configuración Inicial

### SQL Manual (Semana 6)

```python
import sqlite3

# Conectar
conexion = sqlite3.connect('mi_db.db')
conexion.row_factory = sqlite3.Row
cursor = conexion.cursor()

# Crear tabla
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER DEFAULT 0,
        categoria_id INTEGER,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
""")
conexion.commit()
```

### Con ORM (Semana 7)

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, Session, relationship

Base = declarative_base()

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    categoria = relationship("Categoria", back_populates="productos")

engine = create_engine('sqlite:///mi_db.db')
Base.metadata.create_all(engine)
session = Session(engine)
```

**Ventaja ORM**: La definición de la tabla es más legible y las relaciones son explícitas.

---

## CREATE - Insertar Datos

### SQL Manual

```python
# Insertar uno
cursor.execute("""
    INSERT INTO productos (nombre, precio, stock, categoria_id)
    VALUES (?, ?, ?, ?)
""", ("Laptop", 999.99, 10, 1))
conexion.commit()
id_nuevo = cursor.lastrowid

# Insertar varios
datos = [
    ("Mouse", 29.99, 50, 1),
    ("Teclado", 49.99, 30, 1),
]
cursor.executemany("""
    INSERT INTO productos (nombre, precio, stock, categoria_id)
    VALUES (?, ?, ?, ?)
""", datos)
conexion.commit()
```

### Con ORM

```python
# Insertar uno
producto = Producto(nombre="Laptop", precio=999.99, stock=10, categoria_id=1)
session.add(producto)
session.commit()
# El ID está en producto.id automáticamente

# Insertar varios
productos = [
    Producto(nombre="Mouse", precio=29.99, stock=50, categoria_id=1),
    Producto(nombre="Teclado", precio=49.99, stock=30, categoria_id=1),
]
session.add_all(productos)
session.commit()
```

**Ventaja ORM**: Código más limpio, no hay strings SQL, el ID se asigna automáticamente al objeto.

---

## READ - Consultar Datos

### Obtener Todos

**SQL Manual:**
```python
cursor.execute("SELECT * FROM productos")
filas = cursor.fetchall()
productos = []
for fila in filas:
    producto = Producto(
        id=fila['id'],
        nombre=fila['nombre'],
        precio=fila['precio'],
        stock=fila['stock']
    )
    productos.append(producto)
```

**Con ORM:**
```python
productos = session.query(Producto).all()
```

### Obtener por ID

**SQL Manual:**
```python
cursor.execute("SELECT * FROM productos WHERE id = ?", (1,))
fila = cursor.fetchone()
if fila:
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

### Filtrar

**SQL Manual:**
```python
cursor.execute("""
    SELECT * FROM productos
    WHERE precio < ? AND stock > ?
    ORDER BY precio DESC
""", (100, 10))
filas = cursor.fetchall()
# ... mapear a objetos ...
```

**Con ORM:**
```python
productos = session.query(Producto).filter(
    Producto.precio < 100,
    Producto.stock > 10
).order_by(Producto.precio.desc()).all()
```

**Ventaja ORM**: No hay mapeo manual fila→objeto, sintaxis Python en lugar de strings SQL.

---

## UPDATE - Actualizar Datos

### SQL Manual

```python
cursor.execute("""
    UPDATE productos
    SET precio = ?, stock = ?
    WHERE id = ?
""", (899.99, 5, 1))
conexion.commit()
```

### Con ORM

```python
producto = session.get(Producto, 1)
producto.precio = 899.99
producto.stock = 5
session.commit()
```

**Ventaja ORM**: Modificas el objeto directamente, sin escribir SQL.

---

## DELETE - Eliminar Datos

### SQL Manual

```python
cursor.execute("DELETE FROM productos WHERE id = ?", (1,))
conexion.commit()
```

### Con ORM

```python
producto = session.get(Producto, 1)
session.delete(producto)
session.commit()
```

---

## Relaciones y JOINs

### Obtener producto con su categoría

**SQL Manual:**
```python
cursor.execute("""
    SELECT p.*, c.nombre as categoria_nombre
    FROM productos p
    LEFT JOIN categorias c ON p.categoria_id = c.id
    WHERE p.id = ?
""", (1,))
fila = cursor.fetchone()
producto_nombre = fila['nombre']
categoria_nombre = fila['categoria_nombre']
```

**Con ORM:**
```python
producto = session.get(Producto, 1)
print(producto.nombre)
print(producto.categoria.nombre)  # ¡Acceso directo a la relación!
```

### Obtener productos de una categoría

**SQL Manual:**
```python
cursor.execute("""
    SELECT * FROM productos WHERE categoria_id = ?
""", (categoria_id,))
# ... mapear resultados ...
```

**Con ORM:**
```python
categoria = session.get(Categoria, categoria_id)
productos = categoria.productos  # ¡Lista automática!
```

**Ventaja ORM**: Las relaciones son navegables como atributos de objeto.

---

## Agregaciones

### Contar, Sumar, Promediar

**SQL Manual:**
```python
cursor.execute("SELECT COUNT(*) FROM productos")
total = cursor.fetchone()[0]

cursor.execute("SELECT SUM(precio * stock) FROM productos")
valor = cursor.fetchone()[0]

cursor.execute("SELECT AVG(precio) FROM productos")
promedio = cursor.fetchone()[0]
```

**Con ORM:**
```python
from sqlalchemy import func

total = session.query(func.count(Producto.id)).scalar()
valor = session.query(func.sum(Producto.precio * Producto.stock)).scalar()
promedio = session.query(func.avg(Producto.precio)).scalar()
```

### GROUP BY

**SQL Manual:**
```python
cursor.execute("""
    SELECT categoria_id, COUNT(*), AVG(precio)
    FROM productos
    GROUP BY categoria_id
""")
```

**Con ORM:**
```python
resultado = session.query(
    Categoria.nombre,
    func.count(Producto.id),
    func.avg(Producto.precio)
).join(Producto).group_by(Categoria.id).all()
```

---

## Tabla Comparativa Resumen

| Operación | SQL Manual | ORM |
|-----------|------------|-----|
| **Crear tabla** | `CREATE TABLE...` en string | Clase con `Column()` |
| **Insertar** | `INSERT INTO... VALUES (?,?)` | `session.add(objeto)` |
| **Obtener todos** | `SELECT *` + mapeo manual | `session.query().all()` |
| **Obtener por ID** | `WHERE id = ?` + mapeo | `session.get(Modelo, id)` |
| **Filtrar** | `WHERE col < ?` en string | `.filter(Modelo.col < valor)` |
| **Ordenar** | `ORDER BY col` en string | `.order_by(Modelo.col)` |
| **Actualizar** | `UPDATE... SET... WHERE` | `objeto.campo = valor` |
| **Eliminar** | `DELETE FROM... WHERE` | `session.delete(objeto)` |
| **Relaciones** | `JOIN` manual en SQL | `objeto.relacion` automático |
| **Agregaciones** | `COUNT/SUM/AVG` en SQL | `func.count/sum/avg()` |

---

## ¿Cuándo Usar Cada Uno?

### Usa SQL Manual cuando:
- Necesitas consultas muy específicas y optimizadas
- Trabajas con bases de datos legacy con esquemas complejos
- Quieres control total sobre el SQL generado
- Estás aprendiendo SQL (¡como en la Semana 6!)

### Usa ORM cuando:
- Quieres desarrollar más rápido
- El código debe ser mantenible y legible
- Necesitas cambiar de base de datos fácilmente
- Las consultas son estándar (90% de los casos)
- Trabajas en un proyecto real o en equipo

---

## Conclusión

| Aspecto | SQL Manual | ORM |
|---------|------------|-----|
| **Líneas de código** | Más | Menos |
| **Legibilidad** | SQL en strings | Python puro |
| **Mapeo objeto-fila** | Manual | Automático |
| **Relaciones** | JOINs manuales | Navegación por atributos |
| **Seguridad** | Debes usar `?` | Automática |
| **Curva aprendizaje** | SQL + Python | Solo Python |
| **Flexibilidad** | Total | Alta (95% casos) |

**Recomendación**: Aprende ambos. Usa ORM para el día a día y SQL manual cuando necesites optimización específica.
