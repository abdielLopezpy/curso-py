# ============================================================================
# PASO 1: Introducción al ORM
# ============================================================================
# Este archivo te muestra qué es un ORM y por qué hace tu vida más fácil.
#
# ORM = Object-Relational Mapping (Mapeo Objeto-Relacional)
# Traduce entre objetos Python y tablas de base de datos AUTOMÁTICAMENTE.
# ============================================================================

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, Session

# ============================================================================
# PASO 1: Crear la "Base" - El fundamento de nuestros modelos
# ============================================================================

# Todos nuestros modelos heredarán de esta clase base
Base = declarative_base()

# ============================================================================
# PASO 2: Definir un Modelo - ¡Es solo una clase Python!
# ============================================================================

class Producto(Base):
    """
    Este es un MODELO. Representa la tabla 'productos' en la base de datos.

    Compara con SQL manual:

    SQL Manual (Semana 6):
    ----------------------
    cursor.execute('''
        CREATE TABLE productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER DEFAULT 0
        )
    ''')

    Con ORM (ahora):
    ----------------
    ¡Solo defines la clase abajo! El ORM crea la tabla por ti.
    """
    __tablename__ = 'productos'  # Nombre de la tabla

    # Columnas de la tabla
    id = Column(Integer, primary_key=True)  # AUTOINCREMENT automático
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    def __repr__(self):
        """Representación legible del objeto."""
        return f"<Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio})>"


# ============================================================================
# PASO 3: Crear el "Engine" - La conexión a la base de datos
# ============================================================================

# Esto es EQUIVALENTE a: conexion = sqlite3.connect('mi_db.db')
# Pero mucho más poderoso

engine = create_engine(
    'sqlite:///datos/intro_orm.db',  # Ruta a la base de datos
    echo=False  # Cambia a True para ver el SQL generado
)

# ============================================================================
# PASO 4: Crear las Tablas - ¡Una línea!
# ============================================================================

# Esto crea TODAS las tablas definidas en los modelos
Base.metadata.create_all(engine)

print("=" * 60)
print("ORM - Object-Relational Mapping")
print("=" * 60)
print("""
Un ORM te permite trabajar con bases de datos usando OBJETOS Python
en lugar de escribir SQL manualmente.

Lo que el ORM hace por ti:
1. Crea las tablas automáticamente desde las clases
2. Genera el SQL de INSERT, SELECT, UPDATE, DELETE
3. Convierte filas de la BD en objetos Python
4. Convierte objetos Python en filas de la BD
5. Maneja conexiones y transacciones
""")

# ============================================================================
# PASO 5: Usar el ORM - ¡Mira qué fácil!
# ============================================================================

# Crear una sesión (como abrir una conexión)
with Session(engine) as session:

    # -------------------------------------------------------------------
    # INSERTAR - SQL Manual vs ORM
    # -------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("INSERTAR DATOS")
    print("-" * 60)

    print("""
SQL Manual (Semana 6):
    cursor.execute(
        "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
        ("Laptop", 999.99, 10)
    )
    conexion.commit()

Con ORM (ahora):
    producto = Producto(nombre="Laptop", precio=999.99, stock=10)
    session.add(producto)
    session.commit()
    """)

    # Crear un producto - ¡Es solo crear un objeto!
    laptop = Producto(nombre="Laptop Gaming", precio=1299.99, stock=5)

    # Agregarlo a la sesión
    session.add(laptop)

    # Guardar los cambios
    session.commit()

    print(f"Producto creado: {laptop}")
    print(f"ID asignado automáticamente: {laptop.id}")

    # -------------------------------------------------------------------
    # INSERTAR VARIOS - Igual de fácil
    # -------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("INSERTAR VARIOS")
    print("-" * 60)

    productos = [
        Producto(nombre="Mouse Gamer", precio=49.99, stock=20),
        Producto(nombre="Teclado Mecánico", precio=89.99, stock=15),
        Producto(nombre="Monitor 4K", precio=399.99, stock=8),
    ]

    # Agregar todos de una vez
    session.add_all(productos)
    session.commit()

    print("Productos agregados:")
    for p in productos:
        print(f"  - {p}")

    # -------------------------------------------------------------------
    # CONSULTAR - Bye bye SQL
    # -------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("CONSULTAR DATOS")
    print("-" * 60)

    print("""
SQL Manual:
    cursor.execute("SELECT * FROM productos")
    filas = cursor.fetchall()
    productos = [Producto(...) for fila in filas]

Con ORM:
    productos = session.query(Producto).all()
    """)

    # Obtener todos los productos
    todos = session.query(Producto).all()
    print(f"\nTodos los productos ({len(todos)}):")
    for p in todos:
        print(f"  [{p.id}] {p.nombre}: ${p.precio:.2f} (stock: {p.stock})")

    # -------------------------------------------------------------------
    # BUSCAR POR ID - Una línea
    # -------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("BUSCAR POR ID")
    print("-" * 60)

    print("""
SQL Manual:
    cursor.execute("SELECT * FROM productos WHERE id = ?", (1,))
    fila = cursor.fetchone()
    producto = Producto(id=fila['id'], nombre=fila['nombre'], ...)

Con ORM:
    producto = session.get(Producto, 1)
    """)

    # Buscar producto con ID 1
    producto = session.get(Producto, 1)
    print(f"\nProducto con ID 1: {producto}")

    # -------------------------------------------------------------------
    # FILTRAR - Sin escribir WHERE
    # -------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("FILTRAR DATOS")
    print("-" * 60)

    print("""
SQL Manual:
    cursor.execute("SELECT * FROM productos WHERE precio < ?", (100,))

Con ORM:
    baratos = session.query(Producto).filter(Producto.precio < 100).all()
    """)

    # Productos baratos (menos de $100)
    baratos = session.query(Producto).filter(Producto.precio < 100).all()
    print(f"\nProductos menores a $100:")
    for p in baratos:
        print(f"  - {p.nombre}: ${p.precio:.2f}")

    # -------------------------------------------------------------------
    # ACTUALIZAR - Solo cambia el atributo
    # -------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("ACTUALIZAR DATOS")
    print("-" * 60)

    print("""
SQL Manual:
    cursor.execute(
        "UPDATE productos SET precio = ?, stock = ? WHERE id = ?",
        (1199.99, 3, 1)
    )
    conexion.commit()

Con ORM:
    producto.precio = 1199.99
    producto.stock = 3
    session.commit()
    """)

    # Actualizar el producto
    producto = session.get(Producto, 1)
    print(f"\nAntes: {producto}")

    producto.precio = 1199.99
    producto.stock = 3
    session.commit()

    print(f"Después: {producto}")

    # -------------------------------------------------------------------
    # ELIMINAR - Igual de simple
    # -------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("ELIMINAR DATOS")
    print("-" * 60)

    print("""
SQL Manual:
    cursor.execute("DELETE FROM productos WHERE id = ?", (4,))
    conexion.commit()

Con ORM:
    session.delete(producto)
    session.commit()
    """)

    # Eliminar el último producto
    ultimo = session.query(Producto).order_by(Producto.id.desc()).first()
    if ultimo:
        print(f"\nEliminando: {ultimo}")
        session.delete(ultimo)
        session.commit()
        print("Eliminado.")

# La sesión se cierra automáticamente al salir del 'with'

print("\n" + "=" * 60)
print("RESUMEN")
print("=" * 60)
print("""
Con un ORM:

1. Defines modelos como CLASES Python
2. El ORM crea las tablas automáticamente
3. Insertas objetos con session.add()
4. Consultas con session.query() o session.get()
5. Actualizas modificando atributos
6. Eliminas con session.delete()
7. Confirmas con session.commit()

¡NO escribes SQL! El ORM lo hace por ti.

Ejecuta los siguientes archivos para aprender más:
- 02_modelos_basicos.py
- 03_crud_simple.py
- 04_relaciones.py
""")
