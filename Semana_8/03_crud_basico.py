# ============================================================================
# SEMANA 8 - PASO 3: Operaciones CRUD Básicas
# ============================================================================
# CRUD = Create, Read, Update, Delete (Crear, Leer, Actualizar, Eliminar)
#
# Este archivo te enseña las 4 operaciones fundamentales de cualquier
# aplicación que trabaje con bases de datos.
# ============================================================================

"""
============================================================================
¿QUÉ ES CRUD?
============================================================================

CRUD son las 4 operaciones básicas que puedes hacer con datos:

    C - CREATE (Crear)     →  Insertar nuevos registros
    R - READ (Leer)        →  Consultar registros existentes
    U - UPDATE (Actualizar)→  Modificar registros existentes
    D - DELETE (Eliminar)  →  Borrar registros

En SQLAlchemy:

    Operación    │  Método
    ─────────────┼──────────────────────────
    CREATE       │  session.add(objeto)
    READ         │  session.query(Modelo)
    UPDATE       │  objeto.atributo = nuevo_valor
    DELETE       │  session.delete(objeto)

Después de CREATE, UPDATE o DELETE, siempre: session.commit()

============================================================================
"""

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURA TU CADENA DE CONEXIÓN AQUÍ                                     ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
DATABASE_URL = "postgresql://usuario:contraseña@ep-xxx.region.aws.neon.tech/neondb?sslmode=require"

# Configuración de SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# ============================================================================
# MODELO: Producto
# ============================================================================

class Producto(Base):
    """Modelo de producto para practicar CRUD."""
    __tablename__ = 'productos_crud'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(String(500))
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio})>"


# ============================================================================
# FUNCIONES CRUD
# ============================================================================
# Estas funciones encapsulan las operaciones CRUD.
# Puedes copiarlas y adaptarlas para tus propios modelos.
# ============================================================================

# ============================================================================
# CREATE - Crear nuevos registros
# ============================================================================

def crear_producto(nombre: str, precio: float, descripcion: str = "", stock: int = 0) -> Producto:
    """
    Crea un nuevo producto en la base de datos.

    Args:
        nombre: Nombre del producto (requerido)
        precio: Precio del producto (requerido)
        descripcion: Descripción opcional
        stock: Cantidad en stock (default: 0)

    Returns:
        El producto creado con su ID asignado

    Ejemplo:
        laptop = crear_producto("Laptop Gaming", 1299.99, "16GB RAM", 10)
    """
    # Crear una sesión
    with Session() as session:
        # Crear el objeto
        producto = Producto(
            nombre=nombre,
            precio=precio,
            descripcion=descripcion,
            stock=stock
        )

        # Agregarlo a la sesión
        session.add(producto)

        # Guardar los cambios (commit)
        session.commit()

        # Refrescar para obtener el ID asignado
        session.refresh(producto)

        print(f"[CREATE] Producto creado: {producto}")
        return producto


def crear_varios_productos(productos_data: list) -> list:
    """
    Crea múltiples productos de una vez.

    Args:
        productos_data: Lista de diccionarios con datos de productos

    Returns:
        Lista de productos creados

    Ejemplo:
        datos = [
            {"nombre": "Mouse", "precio": 29.99},
            {"nombre": "Teclado", "precio": 59.99}
        ]
        productos = crear_varios_productos(datos)
    """
    with Session() as session:
        productos = []
        for data in productos_data:
            producto = Producto(**data)
            productos.append(producto)

        # Agregar todos de una vez
        session.add_all(productos)
        session.commit()

        # Refrescar para obtener IDs
        for p in productos:
            session.refresh(p)

        print(f"[CREATE] {len(productos)} productos creados")
        return productos


# ============================================================================
# READ - Leer/Consultar registros
# ============================================================================

def obtener_todos_los_productos() -> list:
    """
    Obtiene todos los productos de la base de datos.

    Returns:
        Lista de todos los productos

    Ejemplo:
        productos = obtener_todos_los_productos()
        for p in productos:
            print(p.nombre)
    """
    with Session() as session:
        productos = session.query(Producto).all()
        print(f"[READ] {len(productos)} productos encontrados")
        return productos


def obtener_producto_por_id(producto_id: int) -> Producto:
    """
    Obtiene un producto por su ID.

    Args:
        producto_id: ID del producto a buscar

    Returns:
        El producto encontrado o None si no existe

    Ejemplo:
        producto = obtener_producto_por_id(1)
        if producto:
            print(producto.nombre)
    """
    with Session() as session:
        producto = session.get(Producto, producto_id)
        if producto:
            print(f"[READ] Producto encontrado: {producto}")
        else:
            print(f"[READ] Producto con ID {producto_id} no encontrado")
        return producto


def buscar_productos_por_nombre(nombre: str) -> list:
    """
    Busca productos que contengan el texto en su nombre.

    Args:
        nombre: Texto a buscar (búsqueda parcial)

    Returns:
        Lista de productos que coinciden

    Ejemplo:
        laptops = buscar_productos_por_nombre("laptop")
    """
    with Session() as session:
        # LIKE con % para búsqueda parcial (contiene)
        productos = session.query(Producto).filter(
            Producto.nombre.ilike(f"%{nombre}%")  # ilike = case insensitive
        ).all()
        print(f"[READ] {len(productos)} productos encontrados con '{nombre}'")
        return productos


def obtener_productos_activos() -> list:
    """
    Obtiene solo los productos activos.

    Returns:
        Lista de productos donde activo=True
    """
    with Session() as session:
        productos = session.query(Producto).filter(
            Producto.activo == True
        ).all()
        print(f"[READ] {len(productos)} productos activos")
        return productos


def obtener_productos_con_stock() -> list:
    """
    Obtiene productos que tienen stock disponible.

    Returns:
        Lista de productos con stock > 0
    """
    with Session() as session:
        productos = session.query(Producto).filter(
            Producto.stock > 0
        ).all()
        print(f"[READ] {len(productos)} productos con stock")
        return productos


def obtener_productos_baratos(precio_maximo: float) -> list:
    """
    Obtiene productos por debajo de un precio.

    Args:
        precio_maximo: Precio máximo a buscar

    Returns:
        Lista de productos con precio <= precio_maximo
    """
    with Session() as session:
        productos = session.query(Producto).filter(
            Producto.precio <= precio_maximo
        ).order_by(Producto.precio).all()  # Ordenados por precio
        print(f"[READ] {len(productos)} productos bajo ${precio_maximo}")
        return productos


# ============================================================================
# UPDATE - Actualizar registros existentes
# ============================================================================

def actualizar_precio(producto_id: int, nuevo_precio: float) -> Producto:
    """
    Actualiza el precio de un producto.

    Args:
        producto_id: ID del producto a actualizar
        nuevo_precio: Nuevo precio

    Returns:
        El producto actualizado o None si no existe

    Ejemplo:
        actualizar_precio(1, 999.99)
    """
    with Session() as session:
        producto = session.get(Producto, producto_id)
        if producto:
            precio_anterior = producto.precio
            producto.precio = nuevo_precio
            session.commit()
            print(f"[UPDATE] Precio actualizado: ${precio_anterior} → ${nuevo_precio}")
            return producto
        else:
            print(f"[UPDATE] Producto con ID {producto_id} no encontrado")
            return None


def actualizar_stock(producto_id: int, cantidad: int, operacion: str = "set") -> Producto:
    """
    Actualiza el stock de un producto.

    Args:
        producto_id: ID del producto
        cantidad: Cantidad a establecer/agregar/restar
        operacion: "set" (establecer), "add" (agregar), "sub" (restar)

    Returns:
        El producto actualizado

    Ejemplo:
        actualizar_stock(1, 50, "set")   # Establecer stock en 50
        actualizar_stock(1, 10, "add")   # Agregar 10 al stock
        actualizar_stock(1, 5, "sub")    # Restar 5 del stock
    """
    with Session() as session:
        producto = session.get(Producto, producto_id)
        if producto:
            stock_anterior = producto.stock

            if operacion == "set":
                producto.stock = cantidad
            elif operacion == "add":
                producto.stock += cantidad
            elif operacion == "sub":
                producto.stock = max(0, producto.stock - cantidad)  # No negativo

            session.commit()
            print(f"[UPDATE] Stock actualizado: {stock_anterior} → {producto.stock}")
            return producto
        return None


def desactivar_producto(producto_id: int) -> Producto:
    """
    Desactiva un producto (soft delete).

    En lugar de eliminar, marcamos como inactivo.
    Esto es útil para mantener historial.

    Args:
        producto_id: ID del producto a desactivar

    Returns:
        El producto desactivado
    """
    with Session() as session:
        producto = session.get(Producto, producto_id)
        if producto:
            producto.activo = False
            session.commit()
            print(f"[UPDATE] Producto '{producto.nombre}' desactivado")
            return producto
        return None


# ============================================================================
# DELETE - Eliminar registros
# ============================================================================

def eliminar_producto(producto_id: int) -> bool:
    """
    Elimina un producto de la base de datos.

    ADVERTENCIA: Esta operación es PERMANENTE.
    Considera usar desactivar_producto() en su lugar.

    Args:
        producto_id: ID del producto a eliminar

    Returns:
        True si se eliminó, False si no existía

    Ejemplo:
        if eliminar_producto(1):
            print("Producto eliminado")
    """
    with Session() as session:
        producto = session.get(Producto, producto_id)
        if producto:
            nombre = producto.nombre
            session.delete(producto)
            session.commit()
            print(f"[DELETE] Producto '{nombre}' eliminado permanentemente")
            return True
        else:
            print(f"[DELETE] Producto con ID {producto_id} no encontrado")
            return False


def eliminar_productos_sin_stock() -> int:
    """
    Elimina todos los productos sin stock.

    Returns:
        Número de productos eliminados
    """
    with Session() as session:
        # Buscar productos sin stock
        productos = session.query(Producto).filter(
            Producto.stock == 0
        ).all()

        cantidad = len(productos)

        # Eliminar cada uno
        for producto in productos:
            session.delete(producto)

        session.commit()
        print(f"[DELETE] {cantidad} productos sin stock eliminados")
        return cantidad


# ============================================================================
# PROGRAMA PRINCIPAL - DEMOSTRACIÓN
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SEMANA 8: Operaciones CRUD con SQLAlchemy")
    print("=" * 70)

    try:
        # Crear las tablas
        Base.metadata.create_all(engine)
        print("\n[OK] Tabla 'productos_crud' lista")

        # ---------------------------------------------------------------------
        # CREATE - Crear productos
        # ---------------------------------------------------------------------
        print("\n" + "-" * 70)
        print("CREATE - Crear productos")
        print("-" * 70)

        # Crear un producto individual
        laptop = crear_producto(
            nombre="Laptop Gaming Pro",
            precio=1499.99,
            descripcion="16GB RAM, RTX 4060, 1TB SSD",
            stock=5
        )

        # Crear varios productos
        productos_data = [
            {"nombre": "Mouse Gamer RGB", "precio": 49.99, "stock": 20},
            {"nombre": "Teclado Mecánico", "precio": 89.99, "stock": 15},
            {"nombre": "Monitor 27 4K", "precio": 399.99, "stock": 8},
            {"nombre": "Webcam HD", "precio": 79.99, "stock": 0},
            {"nombre": "Auriculares Pro", "precio": 149.99, "stock": 12},
        ]
        crear_varios_productos(productos_data)

        # ---------------------------------------------------------------------
        # READ - Consultar productos
        # ---------------------------------------------------------------------
        print("\n" + "-" * 70)
        print("READ - Consultar productos")
        print("-" * 70)

        # Obtener todos
        todos = obtener_todos_los_productos()
        print("\nTodos los productos:")
        for p in todos:
            print(f"  [{p.id}] {p.nombre}: ${p.precio:.2f} (stock: {p.stock})")

        # Buscar por nombre
        print()
        buscar_productos_por_nombre("gaming")

        # Productos baratos
        print()
        baratos = obtener_productos_baratos(100)
        print("Productos bajo $100:")
        for p in baratos:
            print(f"  - {p.nombre}: ${p.precio:.2f}")

        # Productos con stock
        print()
        obtener_productos_con_stock()

        # ---------------------------------------------------------------------
        # UPDATE - Actualizar productos
        # ---------------------------------------------------------------------
        print("\n" + "-" * 70)
        print("UPDATE - Actualizar productos")
        print("-" * 70)

        # Actualizar precio
        if todos:
            actualizar_precio(todos[0].id, 1299.99)

        # Actualizar stock
        if len(todos) > 1:
            actualizar_stock(todos[1].id, 5, "add")  # Agregar 5

        # ---------------------------------------------------------------------
        # DELETE - Eliminar productos
        # ---------------------------------------------------------------------
        print("\n" + "-" * 70)
        print("DELETE - Eliminar productos")
        print("-" * 70)

        # Eliminar productos sin stock
        eliminar_productos_sin_stock()

        # Mostrar productos restantes
        print("\nProductos restantes:")
        for p in obtener_todos_los_productos():
            print(f"  [{p.id}] {p.nombre}")

        # ---------------------------------------------------------------------
        # RESUMEN
        # ---------------------------------------------------------------------
        print("\n" + "=" * 70)
        print("RESUMEN DE OPERACIONES CRUD")
        print("=" * 70)
        print("""
╔═══════════════════════════════════════════════════════════════════════╗
║  OPERACIÓN  │  MÉTODO                    │  EJEMPLO                   ║
╠═════════════╪════════════════════════════╪════════════════════════════╣
║  CREATE     │  session.add(objeto)       │  session.add(producto)     ║
║             │  session.add_all(lista)    │  session.add_all(productos)║
║             │                            │  session.commit()          ║
╠═════════════╪════════════════════════════╪════════════════════════════╣
║  READ       │  session.query(Modelo)     │  session.query(Producto)   ║
║             │  .all()                    │  .all()                    ║
║             │  .first()                  │  .first()                  ║
║             │  .filter()                 │  .filter(precio < 100)     ║
║             │  session.get(Modelo, id)   │  session.get(Producto, 1)  ║
╠═════════════╪════════════════════════════╪════════════════════════════╣
║  UPDATE     │  objeto.atributo = valor   │  producto.precio = 99.99   ║
║             │  session.commit()          │  session.commit()          ║
╠═════════════╪════════════════════════════╪════════════════════════════╣
║  DELETE     │  session.delete(objeto)    │  session.delete(producto)  ║
║             │  session.commit()          │  session.commit()          ║
╚═══════════════════════════════════════════════════════════════════════╝

PRÓXIMOS PASOS:
───────────────
Ejecuta: python 04_relaciones.py
Para aprender a crear relaciones entre tablas.
        """)

    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nAsegúrate de configurar tu DATABASE_URL correctamente.")
