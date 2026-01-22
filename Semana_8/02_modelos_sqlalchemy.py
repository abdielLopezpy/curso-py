# ============================================================================
# SEMANA 8 - PASO 2: Definir Modelos con SQLAlchemy
# ============================================================================
# Este archivo te enseña cómo definir modelos (tablas) usando SQLAlchemy.
# Es idéntico a la Semana 7, pero ahora conectado a PostgreSQL en Neon.
#
# Los modelos definen la ESTRUCTURA de tus datos.
# ============================================================================

"""
============================================================================
¿QUÉ ES UN MODELO?
============================================================================

Un MODELO es una clase Python que representa una TABLA en la base de datos.

    Clase Python (Modelo)          Tabla en la BD
    ─────────────────────          ──────────────
    class Producto:          →     productos
        id                   →         id (columna)
        nombre               →         nombre (columna)
        precio               →         precio (columna)

Cada INSTANCIA del modelo representa una FILA:

    laptop = Producto(...)   →     Una fila en la tabla productos

============================================================================
"""

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURA TU CADENA DE CONEXIÓN AQUÍ                                     ║
# ╚═══════════════════════════════════════════════════════════════════════════╝
DATABASE_URL = "postgresql://usuario:contraseña@ep-xxx.region.aws.neon.tech/neondb?sslmode=require"

# Crear el engine y la base
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)

# ============================================================================
# MODELO 1: Producto (Ejemplo básico)
# ============================================================================
# Este es el modelo más simple. Define una tabla con columnas básicas.
# ============================================================================

class Producto(Base):
    """
    Modelo para la tabla 'productos'.

    Representa un producto en una tienda con sus propiedades básicas.

    CÓMO CREAR TU PROPIO MODELO:
    ────────────────────────────
    1. Crea una clase que herede de Base
    2. Define __tablename__ con el nombre de la tabla
    3. Define las columnas usando Column()
    4. (Opcional) Define métodos auxiliares como __repr__
    """

    # -------------------------------------------------------------------------
    # Nombre de la tabla en la base de datos
    # -------------------------------------------------------------------------
    # Por convención: minúsculas, plural, guiones bajos para separar palabras
    # Ejemplos: 'productos', 'usuarios', 'ordenes_compra'
    # -------------------------------------------------------------------------
    __tablename__ = 'productos'

    # -------------------------------------------------------------------------
    # COLUMNAS
    # -------------------------------------------------------------------------
    # Cada columna se define con Column(Tipo, opciones...)
    #
    # TIPOS COMUNES:
    #   Integer     → Números enteros (1, 2, 3...)
    #   String(n)   → Texto con máximo n caracteres
    #   Text        → Texto largo sin límite
    #   Float       → Números decimales (19.99, 3.14...)
    #   Boolean     → True/False
    #   DateTime    → Fecha y hora
    #
    # OPCIONES COMUNES:
    #   primary_key=True  → Es la clave primaria (identificador único)
    #   nullable=False    → No puede ser NULL (es requerido)
    #   default=valor     → Valor por defecto si no se especifica
    #   unique=True       → No puede haber duplicados
    # -------------------------------------------------------------------------

    # Clave primaria - siempre necesitas una
    id = Column(Integer, primary_key=True)

    # Campo de texto requerido (máximo 200 caracteres)
    nombre = Column(String(200), nullable=False)

    # Campo de texto opcional para descripción larga
    descripcion = Column(Text, nullable=True)

    # Campo numérico decimal para el precio
    precio = Column(Float, nullable=False)

    # Campo entero con valor por defecto
    stock = Column(Integer, default=0)

    # Campo booleano con valor por defecto
    activo = Column(Boolean, default=True)

    # Campo de fecha/hora que se llena automáticamente
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    # -------------------------------------------------------------------------
    # MÉTODO __repr__
    # -------------------------------------------------------------------------
    # Define cómo se muestra el objeto cuando lo imprimes.
    # Es útil para debugging.
    # -------------------------------------------------------------------------
    def __repr__(self):
        return f"<Producto(id={self.id}, nombre='{self.nombre}', precio={self.precio})>"


# ============================================================================
# MODELO 2: Usuario (Otro ejemplo)
# ============================================================================
# Otro modelo común en aplicaciones web.
# ============================================================================

class Usuario(Base):
    """
    Modelo para la tabla 'usuarios'.

    Representa un usuario del sistema con sus datos básicos.
    """
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)

    # Email único (no puede haber dos usuarios con el mismo email)
    email = Column(String(100), nullable=False, unique=True)

    # Nombre del usuario
    nombre = Column(String(100), nullable=False)

    # Contraseña (en producción, ¡siempre hasheada!)
    password_hash = Column(String(255), nullable=False)

    # Estado del usuario
    activo = Column(Boolean, default=True)

    # Fechas de auditoría
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    ultimo_acceso = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Usuario(id={self.id}, email='{self.email}')>"


# ============================================================================
# PLANTILLA PARA CREAR TUS PROPIOS MODELOS
# ============================================================================
# Copia y modifica esta plantilla para crear nuevas entidades.
# ============================================================================

class PlantillaModelo(Base):
    """
    ╔═══════════════════════════════════════════════════════════════════════╗
    ║                    PLANTILLA PARA NUEVO MODELO                        ║
    ╠═══════════════════════════════════════════════════════════════════════╣
    ║                                                                       ║
    ║  INSTRUCCIONES:                                                       ║
    ║  1. Copia esta clase                                                  ║
    ║  2. Cambia el nombre de la clase (ej: Cliente, Pedido, Articulo)      ║
    ║  3. Cambia __tablename__ al nombre de tu tabla                        ║
    ║  4. Modifica las columnas según tu necesidad                          ║
    ║  5. Ejecuta Base.metadata.create_all(engine) para crear la tabla      ║
    ║                                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════╝
    """
    __tablename__ = 'plantilla_modelo'  # Cambia esto

    # -------------------------------------------------------------------------
    # COLUMNA OBLIGATORIA: Clave primaria
    # -------------------------------------------------------------------------
    id = Column(Integer, primary_key=True)

    # -------------------------------------------------------------------------
    # COLUMNAS DE TEXTO
    # -------------------------------------------------------------------------
    # String(n): texto corto con límite de n caracteres
    # Text: texto largo sin límite
    # -------------------------------------------------------------------------
    nombre = Column(String(100), nullable=False)        # Requerido
    descripcion = Column(Text, nullable=True)           # Opcional
    codigo = Column(String(50), unique=True)            # Único

    # -------------------------------------------------------------------------
    # COLUMNAS NUMÉRICAS
    # -------------------------------------------------------------------------
    cantidad = Column(Integer, default=0)               # Entero con default
    precio = Column(Float, nullable=True)               # Decimal opcional
    # Para dinero exacto, considera usar Numeric(10, 2)

    # -------------------------------------------------------------------------
    # COLUMNAS BOOLEANAS
    # -------------------------------------------------------------------------
    activo = Column(Boolean, default=True)
    verificado = Column(Boolean, default=False)

    # -------------------------------------------------------------------------
    # COLUMNAS DE FECHA/HORA
    # -------------------------------------------------------------------------
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_modificacion = Column(DateTime, onupdate=datetime.utcnow)

    # -------------------------------------------------------------------------
    # MÉTODO DE REPRESENTACIÓN
    # -------------------------------------------------------------------------
    def __repr__(self):
        return f"<PlantillaModelo(id={self.id}, nombre='{self.nombre}')>"


# ============================================================================
# CREAR LAS TABLAS EN LA BASE DE DATOS
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("SEMANA 8: Modelos con SQLAlchemy")
    print("=" * 70)

    try:
        # Crear todas las tablas definidas
        print("\n[1] Creando tablas en la base de datos...")
        Base.metadata.create_all(engine)
        print("    [OK] Tablas creadas exitosamente")

        # Mostrar las tablas creadas
        print("\n[2] Tablas disponibles:")
        for tabla in Base.metadata.tables:
            print(f"    - {tabla}")

        # Mostrar las columnas de Producto
        print("\n[3] Columnas de la tabla 'productos':")
        for columna in Producto.__table__.columns:
            tipo = str(columna.type)
            nullable = "opcional" if columna.nullable else "requerido"
            print(f"    - {columna.name}: {tipo} ({nullable})")

        print("\n" + "=" * 70)
        print("RESUMEN")
        print("=" * 70)
        print("""
Los modelos te permiten:

1. DEFINIR ESTRUCTURA
   - Cada clase = una tabla
   - Cada Column() = una columna
   - El ORM crea el SQL por ti

2. TIPOS DE DATOS
   - Integer: números enteros
   - String(n): texto con límite
   - Float: decimales
   - Boolean: verdadero/falso
   - DateTime: fechas

3. OPCIONES ÚTILES
   - primary_key: identificador único
   - nullable: si puede ser NULL
   - default: valor por defecto
   - unique: sin duplicados

PRÓXIMOS PASOS:
───────────────
Ejecuta: python 03_crud_basico.py
Para aprender a crear, leer, actualizar y eliminar datos.
        """)

    except Exception as e:
        print(f"\n[ERROR] {e}")
        print("\nAsegúrate de:")
        print("1. Configurar tu DATABASE_URL correctamente")
        print("2. Tener conexión a internet")
        print("3. Haber instalado: pip install psycopg2-binary")
