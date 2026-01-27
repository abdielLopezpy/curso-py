# ============================================================================
# SEMANA 8 - PASO 1: Introducción a Neon (PostgreSQL Serverless)
# ============================================================================
# Este archivo te enseña cómo conectarte a Neon, una base de datos PostgreSQL
# en la nube que es gratuita y fácil de usar.
#
# ANTES DE EJECUTAR:
# 1. Crea una cuenta en https://neon.tech
# 2. Crea un proyecto
# 3. Copia tu cadena de conexión
# 4. Pégala abajo donde dice DATABASE_URL
# ============================================================================

"""
============================================================================
¿QUÉ ES NEON?
============================================================================

Neon es PostgreSQL "serverless" (sin servidor):
- NO necesitas instalar nada en tu computadora
- La base de datos está en la NUBE
- Es GRATIS para proyectos pequeños
- Escala automáticamente según lo que necesites

COMPARACIÓN:

    SQLite (Semana 6-7):
    ┌─────────────────────────────────────┐
    │  Tu Computadora                     │
    │  ┌─────────────────┐                │
    │  │  archivo.db     │ <-- Archivo    │
    │  │  (datos locales)│     local      │
    │  └─────────────────┘                │
    └─────────────────────────────────────┘

    Neon (PostgreSQL en la nube):
    ┌─────────────────────────────────────┐
    │  Tu Computadora                     │
    │  ┌─────────────────┐                │
    │  │   Tu código     │                │
    │  │   Python        │───────┐        │
    │  └─────────────────┘       │        │
    └────────────────────────────│────────┘
                                 │ Internet
    ┌────────────────────────────│────────┐
    │  Neon (Nube)               │        │
    │  ┌─────────────────┐       │        │
    │  │   PostgreSQL    │ <─────┘        │
    │  │   (tus datos)   │                │
    │  └─────────────────┘                │
    └─────────────────────────────────────┘

============================================================================
"""

# ============================================================================
# PASO 1: Importar las librerías necesarias
# ============================================================================
# SQLAlchemy es el ORM que ya conoces de la Semana 7.
# psycopg2 es el "driver" que permite a Python hablar con PostgreSQL.
# ============================================================================

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# ============================================================================
# PASO 2: Configurar la conexión a Neon
# ============================================================================
# IMPORTANTE: Reemplaza la cadena de abajo con tu propia cadena de conexión.
#
# Para obtener tu cadena:
# 1. Ve a https://console.neon.tech
# 2. Selecciona tu proyecto
# 3. En "Connection Details", selecciona "Python"
# 4. Copia la cadena que empieza con "postgresql://"
# ============================================================================
# ╔═══════════════════════════════════════════════════════════════════════════╗
# ║  CONFIGURA TU CADENA DE CONEXIÓN AQUÍ                                     ║
# ╚═══════════════════════════════════════════════════════════════════════════╝

DATABASE_URL = "postgresql://neondb_owner:npg_xnKz5VIdoiv7@ep-hidden-voice-ahdtczjv-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
#               ↑           ↑       ↑            ↑                           ↑        ↑
#               │           │       │            │                           │        │
#               │           │       │            │                           │        └── Obligatorio para Neon
#               │           │       │            │                           └── Nombre de la base de datos
#               │           │       │            └── Host de Neon (único para tu proyecto)
#               │           │       └── Tu contraseña (generada por Neon)
#               │           └── Tu usuario (generalmente tu email o "neondb_owner")
#               └── Protocolo (siempre postgresql://)

# ============================================================================
# PASO 3: Crear el "engine" (motor de conexión)
# ============================================================================
# El engine es el puente entre Python y la base de datos.
# Es similar a lo que hacíamos en SQLite, pero ahora con PostgreSQL.
# ============================================================================

print("=" * 70)
print("SEMANA 8: Conectando con Neon (PostgreSQL en la Nube)")
print("=" * 70)

try:
    # Crear el engine con la URL de Neon
    # echo=True muestra las consultas SQL que se ejecutan (útil para aprender)
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Cambia a True para ver el SQL generado
        pool_pre_ping=True  # Verifica la conexión antes de usarla
    )

    # =========================================================================
    # PASO 4: Probar la conexión
    # =========================================================================
    # Ejecutamos una consulta simple para verificar que todo funciona.
    # =========================================================================

    print("\n[1] Probando conexión a Neon...")

    with engine.connect() as conexion:
        # Consulta simple para verificar la conexión
        resultado = conexion.execute(text("SELECT version()"))
        version = resultado.fetchone()[0]

        print(f"\n[OK] ¡Conexión exitosa!")
        print(f"\n    Servidor: PostgreSQL")
        print(f"    Versión: {version[:50]}...")

    # =========================================================================
    # PASO 5: Crear la Base para los modelos
    # =========================================================================
    # Esto es idéntico a lo que hacíamos con SQLite en la Semana 7.
    # =========================================================================

    print("\n[2] Configurando SQLAlchemy...")

    Base = declarative_base()

    # Crear una fábrica de sesiones
    Session = sessionmaker(bind=engine)

    print("    [OK] Base declarativa creada")
    print("    [OK] Session factory configurada")

    # =========================================================================
    # PASO 6: Crear una tabla de prueba
    # =========================================================================
    # Vamos a crear una tabla simple para verificar que podemos escribir.
    # =========================================================================

    print("\n[3] Creando tabla de prueba...")

    from sqlalchemy import Column, Integer, String, DateTime
    from datetime import datetime

    class PruebaConexion(Base):
        """
        Tabla de prueba para verificar que la conexión funciona.
        Esta tabla se puede eliminar después.
        """
        __tablename__ = 'prueba_conexion'

        id = Column(Integer, primary_key=True)
        mensaje = Column(String(200))
        fecha = Column(DateTime, default=datetime.utcnow)

    # Crear la tabla en la base de datos
    Base.metadata.create_all(engine)
    print("    [OK] Tabla 'prueba_conexion' creada")

    # =========================================================================
    # PASO 7: Insertar y leer datos de prueba
    # =========================================================================

    print("\n[4] Probando operaciones CRUD...")

    with Session() as session:
        # Insertar un registro de prueba
        prueba = PruebaConexion(mensaje="¡Hola desde Python!")
        session.add(prueba)
        session.commit()
        print(f"    [OK] Registro insertado con ID: {prueba.id}")

        # Leer el registro
        registro = session.query(PruebaConexion).first()
        print(f"    [OK] Registro leído: '{registro.mensaje}'")

        # Eliminar el registro (limpieza)
        session.delete(registro)
        session.commit()
        print("    [OK] Registro eliminado (limpieza)")

    # =========================================================================
    # RESUMEN
    # =========================================================================

    print("\n" + "=" * 70)
    print("¡CONEXIÓN EXITOSA!")
    print("=" * 70)
    print("""
Tu configuración está funcionando correctamente:

    [✓] Conexión a Neon establecida
    [✓] SQLAlchemy configurado
    [✓] Tabla de prueba creada
    [✓] Operaciones CRUD funcionando

PRÓXIMOS PASOS:
───────────────
1. Guarda tu DATABASE_URL en un lugar seguro
2. Ejecuta: python 02_modelos_sqlalchemy.py
3. Aprende a definir modelos y relaciones
    """)

except Exception as e:
    # =========================================================================
    # MANEJO DE ERRORES
    # =========================================================================

    print(f"\n[ERROR] No se pudo conectar: {e}")
    print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                         SOLUCIÓN DE PROBLEMAS                             ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  ERROR: "could not translate host name"                                   ║
║  ────────────────────────────────────────                                 ║
║  → La cadena de conexión es incorrecta                                    ║
║  → Copia la cadena completa desde Neon                                    ║
║                                                                           ║
║  ERROR: "password authentication failed"                                  ║
║  ───────────────────────────────────────                                  ║
║  → La contraseña es incorrecta                                            ║
║  → Copia la cadena de conexión COMPLETA desde Neon                        ║
║                                                                           ║
║  ERROR: "No module named 'psycopg2'"                                      ║
║  ─────────────────────────────────────                                    ║
║  → Instala el driver: pip install psycopg2-binary                         ║
║                                                                           ║
║  ERROR: "SSL connection is required"                                      ║
║  ───────────────────────────────────                                      ║
║  → Añade ?sslmode=require al final de tu cadena                           ║
║                                                                           ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  PASOS PARA OBTENER TU CADENA DE CONEXIÓN:                                ║
║                                                                           ║
║  1. Ve a: https://console.neon.tech                                       ║
║  2. Selecciona tu proyecto                                                ║
║  3. En "Connection Details", selecciona "Python"                          ║
║  4. Copia la cadena que empieza con "postgresql://"                       ║
║  5. Pégala arriba donde dice DATABASE_URL = "..."                         ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)

# ============================================================================
# INFORMACIÓN ADICIONAL
# ============================================================================

print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║                    DIFERENCIAS: SQLite vs PostgreSQL                      ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  Característica     │  SQLite           │  PostgreSQL (Neon)              ║
║  ───────────────────┼───────────────────┼────────────────────────────────║
║  Ubicación          │  Archivo local    │  Servidor en la nube           ║
║  Instalación        │  Ninguna          │  Ninguna (es serverless)       ║
║  Escalabilidad      │  Limitada         │  Alta                          ║
║  Concurrencia       │  Baja             │  Alta                          ║
║  Tipos de datos     │  Básicos          │  Avanzados (JSON, arrays...)   ║
║  Producción         │  No recomendado   │  Estándar de la industria      ║
║                                                                           ║
║  LO QUE NO CAMBIA:                                                        ║
║  - La sintaxis de SQLAlchemy es IDÉNTICA                                  ║
║  - Los modelos se definen igual                                           ║
║  - Las consultas funcionan igual                                          ║
║  - Solo cambia la cadena de conexión                                      ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
""")
