# ============================================================================
# SEMANA 8 - PASO 4: Relaciones entre Tablas
# ============================================================================
# Este archivo te enseña cómo crear relaciones entre diferentes modelos.
#
# Las relaciones son fundamentales para modelar datos del mundo real:
# - Un cliente tiene muchos pedidos
# - Un producto pertenece a una categoría
# - Un autor escribe muchos libros
# ============================================================================

"""
============================================================================
TIPOS DE RELACIONES
============================================================================

1. UNO A MUCHOS (One-to-Many) - El más común
   ─────────────────────────────────────────
   Una categoría tiene MUCHOS productos.
   Un producto pertenece a UNA categoría.

   Categoría (1) ←──────→ (*) Producto
        │                      │
        └── productos         └── categoria

2. MUCHOS A MUCHOS (Many-to-Many)
   ───────────────────────────────
   Un producto puede estar en MUCHAS órdenes.
   Una orden puede tener MUCHOS productos.

   Producto (*) ←──────→ (*) Orden
                    │
             tabla_intermedia

3. UNO A UNO (One-to-One)
   ──────────────────────
   Un usuario tiene UN perfil.
   Un perfil pertenece a UN usuario.

   Usuario (1) ←──────→ (1) Perfil

============================================================================
"""

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURA TU CADENA DE CONEXIÓN AQUÍ                                     ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
DATABASE_URL = "postgresql://usuario:contraseña@ep-xxx.region.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


# ============================================================================
# RELACIÓN UNO A MUCHOS: Categoría → Productos
# ============================================================================
# Una categoría puede tener muchos productos.
# Un producto pertenece a una sola categoría.
# ============================================================================

class Categoria(Base):
    """
    Modelo de Categoría.

    LADO "UNO" de la relación uno-a-muchos.
    Una categoría tiene muchos productos.
    """
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500))

    # -------------------------------------------------------------------------
    # RELACIÓN: Una categoría tiene MUCHOS productos
    # -------------------------------------------------------------------------
    # relationship() crea una "lista virtual" de productos relacionados.
    # back_populates conecta esta relación con la del otro modelo.
    # -------------------------------------------------------------------------
    productos = relationship(
        "Producto",           # Nombre del modelo relacionado
        back_populates="categoria",  # Nombre del atributo en Producto
        cascade="all, delete-orphan"  # Si se elimina la categoría, se eliminan sus productos
    )

    def __repr__(self):
        return f"<Categoria(id={self.id}, nombre='{self.nombre}')>"


class Producto(Base):
    """
    Modelo de Producto.

    LADO "MUCHOS" de la relación uno-a-muchos.
    Un producto pertenece a una categoría.
    """
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    # -------------------------------------------------------------------------
    # CLAVE FORÁNEA: Conecta este producto con una categoría
    # -------------------------------------------------------------------------
    # ForeignKey() crea la relación a nivel de base de datos.
    # El formato es 'nombre_tabla.nombre_columna'
    # -------------------------------------------------------------------------
    categoria_id = Column(Integer, ForeignKey('categorias.id'))

    # -------------------------------------------------------------------------
    # RELACIÓN: Un producto pertenece a UNA categoría
    # -------------------------------------------------------------------------
    # Esto permite acceder a la categoría como: producto.categoria
    # -------------------------------------------------------------------------
    categoria = relationship(
        "Categoria",
        back_populates="productos"
    )

    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', categoria_id={self.categoria_id})>"


# ============================================================================
# RELACIÓN UNO A MUCHOS: Cliente → Pedidos
# ============================================================================
# Un cliente puede hacer muchos pedidos.
# Un pedido pertenece a un solo cliente.
# ============================================================================

class Cliente(Base):
    """
    Modelo de Cliente.

    Un cliente puede hacer muchos pedidos.
    """
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20))

    # Relación: Un cliente tiene muchos pedidos
    pedidos = relationship(
        "Pedido",
        back_populates="cliente",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Cliente(id={self.id}, nombre='{self.nombre}')>"


class Pedido(Base):
    """
    Modelo de Pedido.

    Un pedido pertenece a un cliente y tiene muchos items.
    """
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    total = Column(Float, default=0)
    estado = Column(String(50), default="pendiente")  # pendiente, pagado, enviado, entregado

    # Clave foránea al cliente
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=False)

    # Relación: Un pedido pertenece a un cliente
    cliente = relationship("Cliente", back_populates="pedidos")

    # Relación: Un pedido tiene muchos items
    items = relationship(
        "ItemPedido",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Pedido(id={self.id}, cliente_id={self.cliente_id}, total={self.total})>"

    def calcular_total(self):
        """Calcula el total del pedido sumando sus items."""
        self.total = sum(item.subtotal for item in self.items)
        return self.total


class ItemPedido(Base):
    """
    Modelo de Item de Pedido.

    Representa un producto dentro de un pedido con su cantidad.
    Esta es una tabla intermedia que también guarda información adicional.
    """
    __tablename__ = 'items_pedido'

    id = Column(Integer, primary_key=True)
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Float, nullable=False)  # Precio al momento de la compra

    # Claves foráneas
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('productos.id'), nullable=False)

    # Relaciones
    pedido = relationship("Pedido", back_populates="items")
    producto = relationship("Producto")

    @property
    def subtotal(self):
        """Calcula el subtotal de este item."""
        return self.cantidad * self.precio_unitario

    def __repr__(self):
        return f"<ItemPedido(producto_id={self.producto_id}, cantidad={self.cantidad})>"


# ============================================================================
# PLANTILLA PARA CREAR RELACIONES
# ============================================================================
# Copia estas plantillas para agregar relaciones a tus propios modelos.
# ============================================================================

"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                 PLANTILLA: RELACIÓN UNO A MUCHOS                          ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  # LADO "UNO" (el padre)                                                  ║
║  class Padre(Base):                                                       ║
║      __tablename__ = 'padres'                                             ║
║      id = Column(Integer, primary_key=True)                               ║
║      nombre = Column(String(100))                                         ║
║                                                                           ║
║      # Relación: un padre tiene muchos hijos                              ║
║      hijos = relationship("Hijo", back_populates="padre")                 ║
║                                                                           ║
║                                                                           ║
║  # LADO "MUCHOS" (el hijo)                                                ║
║  class Hijo(Base):                                                        ║
║      __tablename__ = 'hijos'                                              ║
║      id = Column(Integer, primary_key=True)                               ║
║      nombre = Column(String(100))                                         ║
║                                                                           ║
║      # Clave foránea (OBLIGATORIA en el lado "muchos")                    ║
║      padre_id = Column(Integer, ForeignKey('padres.id'))                  ║
║                                                                           ║
║      # Relación: un hijo pertenece a un padre                             ║
║      padre = relationship("Padre", back_populates="hijos")                ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""


# ============================================================================
# PROGRAMA PRINCIPAL - DEMOSTRACIÓN
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SEMANA 8: Relaciones entre Tablas")
    print("=" * 70)

    try:
        # Crear todas las tablas
        Base.metadata.create_all(engine)
        print("\n[OK] Tablas creadas exitosamente")

        with Session() as session:
            # -----------------------------------------------------------------
            # Ejemplo 1: Crear categorías y productos
            # -----------------------------------------------------------------
            print("\n" + "-" * 70)
            print("EJEMPLO 1: Categorías y Productos (Uno a Muchos)")
            print("-" * 70)

            # Crear categorías
            electronica = Categoria(nombre="Electrónica", descripcion="Dispositivos electrónicos")
            ropa = Categoria(nombre="Ropa", descripcion="Vestimenta y accesorios")

            session.add_all([electronica, ropa])
            session.commit()
            print(f"\nCategorías creadas: {electronica.nombre}, {ropa.nombre}")

            # Crear productos asignándolos a categorías
            laptop = Producto(nombre="Laptop Pro", precio=1299.99, stock=10, categoria=electronica)
            mouse = Producto(nombre="Mouse Gamer", precio=49.99, stock=50, categoria=electronica)
            camiseta = Producto(nombre="Camiseta Python", precio=25.99, stock=100, categoria=ropa)

            session.add_all([laptop, mouse, camiseta])
            session.commit()
            print("Productos creados y asignados a categorías")

            # Acceder a la relación
            print(f"\nProductos en '{electronica.nombre}':")
            for producto in electronica.productos:
                print(f"  - {producto.nombre}: ${producto.precio}")

            print(f"\nCategoría del producto '{laptop.nombre}': {laptop.categoria.nombre}")

            # -----------------------------------------------------------------
            # Ejemplo 2: Cliente, Pedidos e Items
            # -----------------------------------------------------------------
            print("\n" + "-" * 70)
            print("EJEMPLO 2: Cliente, Pedidos e Items (Relaciones Anidadas)")
            print("-" * 70)

            # Crear un cliente
            cliente = Cliente(
                nombre="Juan Pérez",
                email="juan@email.com",
                telefono="555-1234"
            )
            session.add(cliente)
            session.commit()
            print(f"\nCliente creado: {cliente.nombre}")

            # Crear un pedido para el cliente
            pedido = Pedido(cliente=cliente)
            session.add(pedido)

            # Agregar items al pedido
            item1 = ItemPedido(
                pedido=pedido,
                producto=laptop,
                cantidad=1,
                precio_unitario=laptop.precio
            )
            item2 = ItemPedido(
                pedido=pedido,
                producto=mouse,
                cantidad=2,
                precio_unitario=mouse.precio
            )

            session.add_all([item1, item2])

            # Calcular el total del pedido
            pedido.calcular_total()
            session.commit()

            print(f"\nPedido #{pedido.id} creado para {cliente.nombre}")
            print(f"Items del pedido:")
            for item in pedido.items:
                print(f"  - {item.producto.nombre} x{item.cantidad} = ${item.subtotal:.2f}")
            print(f"Total: ${pedido.total:.2f}")

            # -----------------------------------------------------------------
            # Navegación por relaciones
            # -----------------------------------------------------------------
            print("\n" + "-" * 70)
            print("NAVEGACIÓN POR RELACIONES")
            print("-" * 70)

            # Desde el cliente, acceder a sus pedidos
            print(f"\nPedidos del cliente '{cliente.nombre}':")
            for p in cliente.pedidos:
                print(f"  Pedido #{p.id}: ${p.total:.2f} ({p.estado})")

            # Desde el pedido, acceder al cliente
            print(f"\nCliente del pedido #{pedido.id}: {pedido.cliente.nombre}")

            # Cadena de navegación
            print(f"\nCadena de navegación:")
            print(f"  cliente.pedidos[0].items[0].producto.categoria.nombre")
            print(f"  = {cliente.pedidos[0].items[0].producto.categoria.nombre}")

        # ---------------------------------------------------------------------
        # RESUMEN
        # ---------------------------------------------------------------------
        print("\n" + "=" * 70)
        print("RESUMEN DE RELACIONES")
        print("=" * 70)
        print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                        CÓMO CREAR RELACIONES                              ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  1. LADO "MUCHOS" (hijo):                                                 ║
║     - Agregar: categoria_id = Column(Integer, ForeignKey('categorias.id'))║
║     - Agregar: categoria = relationship("Categoria", back_populates="...")║
║                                                                           ║
║  2. LADO "UNO" (padre):                                                   ║
║     - Agregar: productos = relationship("Producto", back_populates="...")  ║
║                                                                           ║
║  3. USAR LA RELACIÓN:                                                     ║
║     - categoria.productos → lista de productos                            ║
║     - producto.categoria → la categoría del producto                      ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  RECUERDA:                                                                ║
║  - ForeignKey va en el lado "muchos"                                      ║
║  - relationship() va en AMBOS lados                                       ║
║  - back_populates conecta ambas direcciones                               ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

PRÓXIMOS PASOS:
───────────────
Ejecuta: python app_flask.py
Para ver todo integrado en una aplicación web.
        """)

    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nAsegúrate de configurar tu DATABASE_URL correctamente.")
