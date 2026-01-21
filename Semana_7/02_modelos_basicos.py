# ============================================================================
# PASO 2: Modelos Básicos con SQLAlchemy
# ============================================================================
# Los MODELOS son clases Python que representan tablas en la base de datos.
# Cada instancia de un modelo es una fila en la tabla.
# ============================================================================

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime

# Base para todos los modelos
Base = declarative_base()

# ============================================================================
# MODELO 1: Usuario - Tipos de datos básicos
# ============================================================================

class Usuario(Base):
    """
    Modelo de Usuario.

    Cada atributo con Column() es una columna en la tabla.
    """
    __tablename__ = 'usuarios'

    # INTEGER - Números enteros
    id = Column(Integer, primary_key=True)

    # STRING - Texto corto (hasta 255 caracteres por defecto)
    nombre = Column(String(100), nullable=False)  # Máximo 100 caracteres
    email = Column(String(150), unique=True, nullable=False)  # Único, no nulo

    # TEXT - Texto largo (sin límite)
    biografia = Column(Text)

    # BOOLEAN - Verdadero/Falso
    activo = Column(Boolean, default=True)

    # DATETIME - Fecha y hora
    fecha_registro = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"


# ============================================================================
# MODELO 2: Producto - Con validaciones
# ============================================================================

class Producto(Base):
    """
    Modelo de Producto con diferentes tipos de columnas.
    """
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)

    # String con longitud específica
    nombre = Column(String(200), nullable=False)
    codigo = Column(String(50), unique=True)  # Código único

    # Float para decimales
    precio = Column(Float, nullable=False)

    # Integer con valor por defecto
    stock = Column(Integer, default=0)

    # Boolean para estado
    disponible = Column(Boolean, default=True)

    # Text para descripciones largas
    descripcion = Column(Text)

    # DateTime para auditoría
    creado_en = Column(DateTime, default=datetime.now)
    actualizado_en = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio})>"

    @property
    def precio_con_iva(self):
        """Propiedad calculada - precio con IVA (16%)."""
        return self.precio * 1.16

    def aplicar_descuento(self, porcentaje: float):
        """Aplica un descuento al precio."""
        descuento = self.precio * (porcentaje / 100)
        self.precio -= descuento
        return self.precio


# ============================================================================
# MODELO 3: Categoria - Simple
# ============================================================================

class Categoria(Base):
    """Modelo simple de Categoría."""
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(String(500))
    activa = Column(Boolean, default=True)

    def __repr__(self):
        return f"<Categoria(id={self.id}, nombre='{self.nombre}')>"


# ============================================================================
# CONFIGURACIÓN Y DEMOSTRACIÓN
# ============================================================================

# Crear el engine (conexión a la base de datos)
engine = create_engine('sqlite:///datos/modelos_basicos.db', echo=False)

# Crear todas las tablas
Base.metadata.create_all(engine)

print("=" * 60)
print("MODELOS BÁSICOS CON SQLAlchemy")
print("=" * 60)

# Demostración
with Session(engine) as session:

    # -------------------------------------------------------------------
    # Crear usuarios
    # -------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("CREANDO USUARIOS")
    print("-" * 60)

    usuarios = [
        Usuario(
            nombre="Ana García",
            email="ana@email.com",
            biografia="Desarrolladora Python con 5 años de experiencia."
        ),
        Usuario(
            nombre="Luis Pérez",
            email="luis@email.com",
            activo=False  # Usuario inactivo
        ),
        Usuario(
            nombre="María López",
            email="maria@email.com",
            biografia="Estudiante de ingeniería de software."
        ),
    ]

    session.add_all(usuarios)
    session.commit()

    print("Usuarios creados:")
    for u in usuarios:
        print(f"  - {u.nombre} ({u.email})")
        print(f"    Activo: {u.activo}")
        print(f"    Registrado: {u.fecha_registro}")

    # -------------------------------------------------------------------
    # Crear categorías
    # -------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("CREANDO CATEGORÍAS")
    print("-" * 60)

    categorias = [
        Categoria(nombre="Electrónica", descripcion="Dispositivos electrónicos"),
        Categoria(nombre="Ropa", descripcion="Vestimenta y accesorios"),
        Categoria(nombre="Hogar", descripcion="Artículos del hogar"),
    ]

    session.add_all(categorias)
    session.commit()

    print("Categorías creadas:")
    for c in categorias:
        print(f"  - {c.nombre}: {c.descripcion}")

    # -------------------------------------------------------------------
    # Crear productos
    # -------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("CREANDO PRODUCTOS")
    print("-" * 60)

    productos = [
        Producto(
            nombre="Laptop Gaming",
            codigo="LAP-001",
            precio=1299.99,
            stock=10,
            descripcion="Laptop para gaming con RTX 4070"
        ),
        Producto(
            nombre="Mouse Inalámbrico",
            codigo="MOU-001",
            precio=29.99,
            stock=50
        ),
        Producto(
            nombre="Monitor 27 pulgadas",
            codigo="MON-001",
            precio=349.99,
            stock=15,
            disponible=True
        ),
    ]

    session.add_all(productos)
    session.commit()

    print("Productos creados:")
    for p in productos:
        print(f"  - [{p.codigo}] {p.nombre}")
        print(f"    Precio: ${p.precio:.2f} | Con IVA: ${p.precio_con_iva:.2f}")
        print(f"    Stock: {p.stock} | Disponible: {p.disponible}")

    # -------------------------------------------------------------------
    # Demostrar métodos del modelo
    # -------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("MÉTODOS DEL MODELO")
    print("-" * 60)

    # Obtener un producto
    laptop = session.query(Producto).filter(Producto.codigo == "LAP-001").first()

    print(f"\nProducto: {laptop.nombre}")
    print(f"Precio original: ${laptop.precio:.2f}")

    # Aplicar descuento
    nuevo_precio = laptop.aplicar_descuento(10)  # 10% de descuento
    session.commit()

    print(f"Precio con 10% descuento: ${nuevo_precio:.2f}")
    print(f"Precio con IVA: ${laptop.precio_con_iva:.2f}")

    # -------------------------------------------------------------------
    # Consultas básicas
    # -------------------------------------------------------------------
    print("\n" + "-" * 60)
    print("CONSULTAS BÁSICAS")
    print("-" * 60)

    # Usuarios activos
    activos = session.query(Usuario).filter(Usuario.activo == True).all()
    print(f"\nUsuarios activos ({len(activos)}):")
    for u in activos:
        print(f"  - {u.nombre}")

    # Productos disponibles con stock
    disponibles = session.query(Producto).filter(
        Producto.disponible == True,
        Producto.stock > 0
    ).all()
    print(f"\nProductos disponibles con stock ({len(disponibles)}):")
    for p in disponibles:
        print(f"  - {p.nombre} (stock: {p.stock})")

print("\n" + "=" * 60)
print("TIPOS DE COLUMNAS EN SQLAlchemy")
print("=" * 60)
print("""
| Tipo SQLAlchemy | Tipo Python | Tipo SQL      | Uso                    |
|-----------------|-------------|---------------|------------------------|
| Integer         | int         | INTEGER       | Números enteros        |
| String(n)       | str         | VARCHAR(n)    | Texto corto            |
| Text            | str         | TEXT          | Texto largo            |
| Float           | float       | REAL/FLOAT    | Decimales              |
| Boolean         | bool        | BOOLEAN       | Verdadero/Falso        |
| DateTime        | datetime    | DATETIME      | Fecha y hora           |
| Date            | date        | DATE          | Solo fecha             |
| Time            | time        | TIME          | Solo hora              |

OPCIONES DE COLUMNA:
- primary_key=True   -> Clave primaria
- nullable=False     -> No puede ser NULL
- unique=True        -> Valor único
- default=valor      -> Valor por defecto
- onupdate=func      -> Actualiza automáticamente
""")
