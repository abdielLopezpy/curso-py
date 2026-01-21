# ============================================================================
# PASO 3: CRUD Simple con ORM
# ============================================================================
# CRUD = Create, Read, Update, Delete
# Con ORM, todas estas operaciones son MUCHO más simples que con SQL manual.
# ============================================================================

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, Session

Base = declarative_base()

# ============================================================================
# MODELO
# ============================================================================

class Producto(Base):
    """Modelo de Producto para demostrar CRUD."""
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    activo = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio})>"


# Configuración
engine = create_engine('sqlite:///datos/crud_simple.db', echo=False)
Base.metadata.create_all(engine)

print("=" * 60)
print("CRUD CON ORM - ¡Sin escribir SQL!")
print("=" * 60)

with Session(engine) as session:

    # =========================================================================
    # CREATE (Crear)
    # =========================================================================
    print("\n" + "=" * 60)
    print("CREATE - Crear registros")
    print("=" * 60)

    print("""
    SQL Manual:
        cursor.execute(
            "INSERT INTO productos (nombre, precio, stock) VALUES (?, ?, ?)",
            ("Laptop", 999.99, 10)
        )
        conexion.commit()
        id_nuevo = cursor.lastrowid

    Con ORM:
        producto = Producto(nombre="Laptop", precio=999.99, stock=10)
        session.add(producto)
        session.commit()
        # El ID se asigna automáticamente a producto.id
    """)

    # Crear un solo producto
    print("\n--- Crear UN producto ---")
    laptop = Producto(nombre="Laptop Gaming", precio=1299.99, stock=5)
    session.add(laptop)
    session.commit()
    print(f"Creado: {laptop}")
    print(f"ID asignado: {laptop.id}")

    # Crear varios productos
    print("\n--- Crear VARIOS productos ---")
    productos = [
        Producto(nombre="Mouse Gamer", precio=49.99, stock=20),
        Producto(nombre="Teclado RGB", precio=89.99, stock=15),
        Producto(nombre="Monitor 4K", precio=449.99, stock=8),
        Producto(nombre="Webcam HD", precio=79.99, stock=25),
        Producto(nombre="Auriculares", precio=129.99, stock=12),
    ]
    session.add_all(productos)  # Agregar todos de una vez
    session.commit()

    for p in productos:
        print(f"  - [{p.id}] {p.nombre}: ${p.precio}")

    # =========================================================================
    # READ (Leer)
    # =========================================================================
    print("\n" + "=" * 60)
    print("READ - Leer/Consultar registros")
    print("=" * 60)

    # --- Obtener todos ---
    print("\n--- Obtener TODOS ---")
    print("""
    SQL Manual:
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall()

    Con ORM:
        todos = session.query(Producto).all()
    """)

    todos = session.query(Producto).all()
    print(f"Total de productos: {len(todos)}")
    for p in todos:
        print(f"  - {p.nombre}")

    # --- Obtener por ID ---
    print("\n--- Obtener por ID ---")
    print("""
    SQL Manual:
        cursor.execute("SELECT * FROM productos WHERE id = ?", (1,))
        fila = cursor.fetchone()

    Con ORM:
        producto = session.get(Producto, 1)
    """)

    producto = session.get(Producto, 1)
    print(f"Producto con ID 1: {producto}")

    # --- Obtener el primero ---
    print("\n--- Obtener el PRIMERO ---")
    primero = session.query(Producto).first()
    print(f"Primer producto: {primero}")

    # --- Filtrar ---
    print("\n--- FILTRAR resultados ---")
    print("""
    SQL Manual:
        cursor.execute("SELECT * FROM productos WHERE precio < ?", (100,))

    Con ORM:
        baratos = session.query(Producto).filter(Producto.precio < 100).all()
    """)

    baratos = session.query(Producto).filter(Producto.precio < 100).all()
    print(f"Productos menores a $100:")
    for p in baratos:
        print(f"  - {p.nombre}: ${p.precio}")

    # --- Múltiples filtros ---
    print("\n--- Múltiples FILTROS ---")
    filtrados = session.query(Producto).filter(
        Producto.precio < 200,
        Producto.stock > 10
    ).all()
    print(f"Precio < $200 Y stock > 10:")
    for p in filtrados:
        print(f"  - {p.nombre}: ${p.precio} (stock: {p.stock})")

    # --- Ordenar ---
    print("\n--- ORDENAR resultados ---")
    print("""
    SQL Manual:
        cursor.execute("SELECT * FROM productos ORDER BY precio DESC")

    Con ORM:
        ordenados = session.query(Producto).order_by(Producto.precio.desc()).all()
    """)

    ordenados = session.query(Producto).order_by(Producto.precio.desc()).all()
    print("Productos ordenados por precio (mayor a menor):")
    for p in ordenados:
        print(f"  - {p.nombre}: ${p.precio}")

    # --- Limitar ---
    print("\n--- LIMITAR resultados ---")
    top3 = session.query(Producto).order_by(Producto.precio.desc()).limit(3).all()
    print("Top 3 más caros:")
    for p in top3:
        print(f"  - {p.nombre}: ${p.precio}")

    # --- Contar ---
    print("\n--- CONTAR registros ---")
    total = session.query(Producto).count()
    baratos_count = session.query(Producto).filter(Producto.precio < 100).count()
    print(f"Total productos: {total}")
    print(f"Productos baratos: {baratos_count}")

    # =========================================================================
    # UPDATE (Actualizar)
    # =========================================================================
    print("\n" + "=" * 60)
    print("UPDATE - Actualizar registros")
    print("=" * 60)

    print("""
    SQL Manual:
        cursor.execute(
            "UPDATE productos SET precio = ?, stock = ? WHERE id = ?",
            (1199.99, 3, 1)
        )
        conexion.commit()

    Con ORM:
        producto = session.get(Producto, 1)
        producto.precio = 1199.99
        producto.stock = 3
        session.commit()
    """)

    # --- Actualizar un registro ---
    print("\n--- Actualizar UN registro ---")
    producto = session.get(Producto, 1)
    print(f"Antes: {producto.nombre} - ${producto.precio} (stock: {producto.stock})")

    producto.precio = 1199.99
    producto.stock = 3
    session.commit()

    print(f"Después: {producto.nombre} - ${producto.precio} (stock: {producto.stock})")

    # --- Actualizar varios registros ---
    print("\n--- Actualizar VARIOS registros ---")
    # Aumentar 10% el precio de productos con stock bajo
    productos_bajo_stock = session.query(Producto).filter(Producto.stock < 10).all()
    print("Aumentando 10% a productos con stock < 10:")
    for p in productos_bajo_stock:
        precio_anterior = p.precio
        p.precio *= 1.10
        print(f"  - {p.nombre}: ${precio_anterior:.2f} -> ${p.precio:.2f}")
    session.commit()

    # =========================================================================
    # DELETE (Eliminar)
    # =========================================================================
    print("\n" + "=" * 60)
    print("DELETE - Eliminar registros")
    print("=" * 60)

    print("""
    SQL Manual:
        cursor.execute("DELETE FROM productos WHERE id = ?", (5,))
        conexion.commit()

    Con ORM:
        producto = session.get(Producto, 5)
        session.delete(producto)
        session.commit()
    """)

    # --- Eliminar un registro ---
    print("\n--- Eliminar UN registro ---")
    producto_a_eliminar = session.get(Producto, 5)
    if producto_a_eliminar:
        print(f"Eliminando: {producto_a_eliminar}")
        session.delete(producto_a_eliminar)
        session.commit()
        print("Eliminado.")

    # Verificar eliminación
    print("\nProductos restantes:")
    for p in session.query(Producto).all():
        print(f"  - [{p.id}] {p.nombre}")

# ============================================================================
# RESUMEN VISUAL
# ============================================================================
print("\n" + "=" * 60)
print("RESUMEN: CRUD CON ORM")
print("=" * 60)
print("""
╔═══════════════════════════════════════════════════════════════╗
║  OPERACIÓN  │  SQL MANUAL              │  ORM                 ║
╠═══════════════════════════════════════════════════════════════╣
║  CREATE     │  INSERT INTO...          │  session.add()       ║
║             │  VALUES (?, ?, ?)        │  session.commit()    ║
╠═══════════════════════════════════════════════════════════════╣
║  READ       │  SELECT * FROM...        │  session.query()     ║
║             │  WHERE... ORDER BY...    │  .filter().all()     ║
║             │                          │  session.get(id)     ║
╠═══════════════════════════════════════════════════════════════╣
║  UPDATE     │  UPDATE... SET...        │  objeto.campo = x    ║
║             │  WHERE id = ?            │  session.commit()    ║
╠═══════════════════════════════════════════════════════════════╣
║  DELETE     │  DELETE FROM...          │  session.delete()    ║
║             │  WHERE id = ?            │  session.commit()    ║
╚═══════════════════════════════════════════════════════════════╝

MÉTODOS PRINCIPALES:
  session.add(objeto)       - Agregar un objeto
  session.add_all(lista)    - Agregar varios objetos
  session.get(Modelo, id)   - Obtener por ID
  session.query(Modelo)     - Iniciar consulta
  session.delete(objeto)    - Marcar para eliminar
  session.commit()          - Guardar cambios

MÉTODOS DE QUERY:
  .all()                    - Obtener todos
  .first()                  - Obtener el primero
  .count()                  - Contar resultados
  .filter(condicion)        - Filtrar
  .order_by(campo)          - Ordenar
  .limit(n)                 - Limitar resultados
  .offset(n)                - Saltar n resultados
""")
