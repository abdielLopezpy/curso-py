# ============================================================================
# PASO 4: Relaciones Entre Modelos
# ============================================================================
# Las RELACIONES permiten conectar tablas entre sí.
# Con ORM, las relaciones son MUCHO más fáciles que con SQL y JOINs.
# ============================================================================

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, Session, relationship
from datetime import datetime

Base = declarative_base()

# ============================================================================
# MODELOS CON RELACIONES
# ============================================================================

class Categoria(Base):
    """
    Modelo Categoría.
    Una categoría tiene MUCHOS productos (relación uno-a-muchos).
    """
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(500))

    # RELACIÓN: Una categoría tiene muchos productos
    # back_populates conecta ambos lados de la relación
    productos = relationship("Producto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(id={self.id}, nombre='{self.nombre}')>"


class Producto(Base):
    """
    Modelo Producto.
    Un producto PERTENECE a una categoría (relación muchos-a-uno).
    """
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    # CLAVE FORÁNEA: Conecta con la tabla categorias
    categoria_id = Column(Integer, ForeignKey('categorias.id'))

    # RELACIÓN: Un producto pertenece a una categoría
    categoria = relationship("Categoria", back_populates="productos")

    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}')>"


class Cliente(Base):
    """
    Modelo Cliente.
    Un cliente tiene MUCHOS pedidos.
    """
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    email = Column(String(150), unique=True, nullable=False)

    # RELACIÓN: Un cliente tiene muchos pedidos
    pedidos = relationship("Pedido", back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(id={self.id}, nombre='{self.nombre}')>"


class Pedido(Base):
    """
    Modelo Pedido.
    Un pedido PERTENECE a un cliente y tiene MUCHOS items.
    """
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.now)
    total = Column(Float, default=0)

    # CLAVE FORÁNEA
    cliente_id = Column(Integer, ForeignKey('clientes.id'))

    # RELACIONES
    cliente = relationship("Cliente", back_populates="pedidos")
    items = relationship("ItemPedido", back_populates="pedido")

    def __repr__(self):
        return f"<Pedido(id={self.id}, cliente_id={self.cliente_id}, total={self.total})>"

    def calcular_total(self):
        """Calcula el total del pedido sumando todos los items."""
        self.total = sum(item.subtotal for item in self.items)
        return self.total


class ItemPedido(Base):
    """
    Modelo Item de Pedido.
    Representa un producto dentro de un pedido (tabla intermedia).
    """
    __tablename__ = 'items_pedido'

    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)

    # CLAVES FORÁNEAS
    pedido_id = Column(Integer, ForeignKey('pedidos.id'))
    producto_id = Column(Integer, ForeignKey('productos.id'))

    # RELACIONES
    pedido = relationship("Pedido", back_populates="items")
    producto = relationship("Producto")

    @property
    def subtotal(self):
        """Calcula el subtotal del item."""
        return self.cantidad * self.precio_unitario

    def __repr__(self):
        return f"<ItemPedido(cantidad={self.cantidad}, precio={self.precio_unitario})>"


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

engine = create_engine('sqlite:///datos/relaciones.db', echo=False)
Base.metadata.create_all(engine)

print("=" * 60)
print("RELACIONES ENTRE MODELOS CON ORM")
print("=" * 60)

print("""
Las relaciones en ORM son MUCHO más fáciles que con SQL:

SQL Manual (Semana 6):
    cursor.execute('''
        SELECT p.*, c.nombre as categoria_nombre
        FROM productos p
        LEFT JOIN categorias c ON p.categoria_id = c.id
        WHERE p.id = ?
    ''', (1,))

Con ORM (ahora):
    producto = session.get(Producto, 1)
    print(producto.categoria.nombre)  # ¡Acceso directo!
""")

with Session(engine) as session:

    # =========================================================================
    # CREAR DATOS DE EJEMPLO
    # =========================================================================
    print("\n" + "-" * 60)
    print("CREANDO DATOS DE EJEMPLO")
    print("-" * 60)

    # Crear categorías
    electronica = Categoria(nombre="Electrónica", descripcion="Gadgets y dispositivos")
    ropa = Categoria(nombre="Ropa", descripcion="Vestimenta")
    hogar = Categoria(nombre="Hogar", descripcion="Artículos del hogar")

    session.add_all([electronica, ropa, hogar])
    session.commit()

    print("Categorías creadas:")
    for c in [electronica, ropa, hogar]:
        print(f"  - {c.nombre}")

    # Crear productos CON sus categorías
    productos = [
        Producto(nombre="Laptop Gaming", precio=1299.99, stock=10, categoria=electronica),
        Producto(nombre="Smartphone", precio=799.99, stock=25, categoria=electronica),
        Producto(nombre="Auriculares BT", precio=89.99, stock=50, categoria=electronica),
        Producto(nombre="Camiseta", precio=29.99, stock=100, categoria=ropa),
        Producto(nombre="Pantalón", precio=49.99, stock=60, categoria=ropa),
        Producto(nombre="Lámpara LED", precio=34.99, stock=40, categoria=hogar),
    ]

    session.add_all(productos)
    session.commit()

    print("\nProductos creados con sus categorías:")
    for p in productos:
        print(f"  - {p.nombre} -> {p.categoria.nombre}")

    # Crear clientes
    cliente1 = Cliente(nombre="Ana García", email="ana@email.com")
    cliente2 = Cliente(nombre="Luis Pérez", email="luis@email.com")

    session.add_all([cliente1, cliente2])
    session.commit()

    print("\nClientes creados:")
    for c in [cliente1, cliente2]:
        print(f"  - {c.nombre} ({c.email})")

    # =========================================================================
    # RELACIÓN UNO-A-MUCHOS: Categoría -> Productos
    # =========================================================================
    print("\n" + "=" * 60)
    print("RELACIÓN UNO-A-MUCHOS: Categoría -> Productos")
    print("=" * 60)

    print("""
    SQL Manual:
        cursor.execute('''
            SELECT * FROM productos WHERE categoria_id = ?
        ''', (categoria_id,))

    Con ORM:
        categoria.productos  # ¡Lista automática!
    """)

    # Acceder a los productos de una categoría
    categoria = session.get(Categoria, 1)  # Electrónica
    print(f"\nCategoría: {categoria.nombre}")
    print(f"Productos en esta categoría ({len(categoria.productos)}):")
    for p in categoria.productos:
        print(f"  - {p.nombre}: ${p.precio}")

    # =========================================================================
    # RELACIÓN MUCHOS-A-UNO: Producto -> Categoría
    # =========================================================================
    print("\n" + "=" * 60)
    print("RELACIÓN MUCHOS-A-UNO: Producto -> Categoría")
    print("=" * 60)

    print("""
    SQL Manual:
        cursor.execute('''
            SELECT p.*, c.nombre as categoria_nombre
            FROM productos p
            JOIN categorias c ON p.categoria_id = c.id
            WHERE p.id = ?
        ''', (1,))

    Con ORM:
        producto.categoria.nombre  # ¡Acceso directo!
    """)

    # Acceder a la categoría de un producto
    producto = session.get(Producto, 1)  # Laptop
    print(f"\nProducto: {producto.nombre}")
    print(f"Categoría: {producto.categoria.nombre}")
    print(f"Descripción categoría: {producto.categoria.descripcion}")

    # =========================================================================
    # CREAR PEDIDOS CON ITEMS
    # =========================================================================
    print("\n" + "=" * 60)
    print("CREANDO PEDIDOS CON ITEMS")
    print("=" * 60)

    # Crear un pedido para Ana
    pedido1 = Pedido(cliente=cliente1)
    session.add(pedido1)

    # Agregar items al pedido
    laptop = session.query(Producto).filter(Producto.nombre == "Laptop Gaming").first()
    auriculares = session.query(Producto).filter(Producto.nombre == "Auriculares BT").first()

    item1 = ItemPedido(
        pedido=pedido1,
        producto=laptop,
        cantidad=1,
        precio_unitario=laptop.precio
    )
    item2 = ItemPedido(
        pedido=pedido1,
        producto=auriculares,
        cantidad=2,
        precio_unitario=auriculares.precio
    )

    session.add_all([item1, item2])
    pedido1.calcular_total()
    session.commit()

    print(f"\nPedido #{pedido1.id} creado para {pedido1.cliente.nombre}")
    print("Items:")
    for item in pedido1.items:
        print(f"  - {item.producto.nombre} x{item.cantidad} = ${item.subtotal:.2f}")
    print(f"Total: ${pedido1.total:.2f}")

    # Crear otro pedido para Luis
    pedido2 = Pedido(cliente=cliente2)
    camiseta = session.query(Producto).filter(Producto.nombre == "Camiseta").first()

    item3 = ItemPedido(
        pedido=pedido2,
        producto=camiseta,
        cantidad=3,
        precio_unitario=camiseta.precio
    )

    session.add_all([pedido2, item3])
    pedido2.calcular_total()
    session.commit()

    print(f"\nPedido #{pedido2.id} creado para {pedido2.cliente.nombre}")
    print(f"Total: ${pedido2.total:.2f}")

    # =========================================================================
    # NAVEGAR RELACIONES
    # =========================================================================
    print("\n" + "=" * 60)
    print("NAVEGANDO RELACIONES")
    print("=" * 60)

    # Ver todos los pedidos de un cliente
    cliente = session.get(Cliente, 1)
    print(f"\nPedidos de {cliente.nombre}:")
    for pedido in cliente.pedidos:
        print(f"\n  Pedido #{pedido.id} - {pedido.fecha.strftime('%Y-%m-%d')}")
        print(f"  Items:")
        for item in pedido.items:
            print(f"    - {item.producto.nombre}: {item.cantidad} x ${item.precio_unitario:.2f}")
        print(f"  Total: ${pedido.total:.2f}")

    # =========================================================================
    # CONSULTAS CON RELACIONES
    # =========================================================================
    print("\n" + "=" * 60)
    print("CONSULTAS CON RELACIONES")
    print("=" * 60)

    # Productos de una categoría específica
    print("\n--- Productos de 'Electrónica' ---")
    productos_elec = session.query(Producto).join(Categoria).filter(
        Categoria.nombre == "Electrónica"
    ).all()
    for p in productos_elec:
        print(f"  - {p.nombre}")

    # Pedidos con más de $100
    print("\n--- Pedidos mayores a $100 ---")
    pedidos_grandes = session.query(Pedido).filter(Pedido.total > 100).all()
    for p in pedidos_grandes:
        print(f"  - Pedido #{p.id} de {p.cliente.nombre}: ${p.total:.2f}")

print("\n" + "=" * 60)
print("RESUMEN: RELACIONES CON ORM")
print("=" * 60)
print("""
TIPOS DE RELACIONES:

1. UNO-A-MUCHOS (One-to-Many):
   - Una categoría tiene MUCHOS productos
   - Un cliente tiene MUCHOS pedidos

   class Categoria(Base):
       productos = relationship("Producto", back_populates="categoria")

   class Producto(Base):
       categoria_id = Column(Integer, ForeignKey('categorias.id'))
       categoria = relationship("Categoria", back_populates="productos")

2. MUCHOS-A-UNO (Many-to-One):
   - Muchos productos pertenecen a UNA categoría
   - Es el lado inverso de uno-a-muchos

3. MUCHOS-A-MUCHOS (Many-to-Many):
   - Se usa una tabla intermedia (como ItemPedido)
   - Un pedido tiene muchos productos
   - Un producto puede estar en muchos pedidos

ACCESO A RELACIONES:
   categoria.productos    # Lista de productos
   producto.categoria     # Objeto categoría
   cliente.pedidos        # Lista de pedidos
   pedido.cliente         # Objeto cliente
   pedido.items           # Lista de items
   item.producto          # Objeto producto

¡Sin escribir JOINs! El ORM navega las relaciones automáticamente.
""")
