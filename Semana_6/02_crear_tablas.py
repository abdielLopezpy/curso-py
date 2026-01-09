# ============================================================================
# PASO 2: Crear Tablas en SQLite
# ============================================================================
# En este archivo aprenderás:
# - Cómo diseñar tablas correctamente
# - Tipos de datos en SQLite
# - Restricciones (constraints)
# - Claves primarias y foráneas
# - Buenas prácticas al crear tablas
# ============================================================================

import sqlite3
import os

# Crear carpeta si no existe
if not os.path.exists('datos'):
    os.makedirs('datos')

print("=" * 60)
print("🎓 PASO 2: Crear Tablas en SQLite")
print("=" * 60)

# Conectar a la base de datos
conexion = sqlite3.connect('datos/tienda.db')
cursor = conexion.cursor()

# ============================================================================
# 1. SINTAXIS BÁSICA PARA CREAR TABLAS
# ============================================================================
print("""
📚 Sintaxis básica para crear una tabla:

    CREATE TABLE nombre_tabla (
        columna1 TIPO restricciones,
        columna2 TIPO restricciones,
        ...
    );

Ejemplo simple:
    CREATE TABLE productos (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        precio REAL
    );
""")

input("Presiona ENTER para crear tu primera tabla...")

# ============================================================================
# 2. TIPOS DE DATOS EN SQLITE
# ============================================================================
print("\n" + "=" * 60)
print("📊 Tipos de Datos en SQLite")
print("=" * 60)

print("""
SQLite tiene 5 tipos de datos principales:

┌──────────┬───────────────────────┬─────────────────┐
│ Tipo     │ Descripción           │ Python equiv.   │
├──────────┼───────────────────────┼─────────────────┤
│ INTEGER  │ Números enteros       │ int             │
│ REAL     │ Números decimales     │ float           │
│ TEXT     │ Cadenas de texto      │ str             │
│ BLOB     │ Datos binarios        │ bytes           │
│ NULL     │ Valor nulo            │ None            │
└──────────┴───────────────────────┴─────────────────┘

💡 SQLite es "tipado dinámico" - es flexible con los tipos
   pero es buena práctica especificarlos correctamente.
""")

# ============================================================================
# 3. RESTRICCIONES (CONSTRAINTS)
# ============================================================================
print("=" * 60)
print("⚠️ Restricciones (Constraints)")
print("=" * 60)

print("""
Las restricciones definen reglas para los datos:

┌─────────────────┬────────────────────────────────────┐
│ Restricción     │ ¿Qué hace?                         │
├─────────────────┼────────────────────────────────────┤
│ PRIMARY KEY     │ Identificador único de cada fila   │
│ AUTOINCREMENT   │ Se incrementa automáticamente      │
│ NOT NULL        │ No puede estar vacío               │
│ UNIQUE          │ No puede repetirse en la tabla     │
│ DEFAULT valor   │ Valor por defecto si no se da      │
│ CHECK(cond)     │ Validación personalizada           │
│ FOREIGN KEY     │ Referencia a otra tabla            │
└─────────────────┴────────────────────────────────────┘
""")

input("Presiona ENTER para ver ejemplos prácticos...")

# ============================================================================
# 4. CREAR TABLA DE CATEGORÍAS
# ============================================================================
print("\n" + "=" * 60)
print("📦 Creando tabla: categorias")
print("=" * 60)

sql_categorias = """
CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    descripcion TEXT,
    activa INTEGER DEFAULT 1
)
"""

cursor.execute(sql_categorias)
conexion.commit()

print("""
✅ Tabla 'categorias' creada

Estructura:
┌──────────────┬─────────┬──────────────────────────────┐
│ Columna      │ Tipo    │ Restricciones                │
├──────────────┼─────────┼──────────────────────────────┤
│ id           │ INTEGER │ PRIMARY KEY AUTOINCREMENT    │
│ nombre       │ TEXT    │ NOT NULL UNIQUE              │
│ descripcion  │ TEXT    │ (ninguna - puede ser NULL)   │
│ activa       │ INTEGER │ DEFAULT 1                    │
└──────────────┴─────────┴──────────────────────────────┘

Explicación:
- id: Se genera solo (1, 2, 3, ...)
- nombre: Obligatorio y no puede repetirse
- descripcion: Opcional
- activa: Por defecto es 1 (true)
""")

# ============================================================================
# 5. CREAR TABLA DE PRODUCTOS
# ============================================================================
print("=" * 60)
print("📦 Creando tabla: productos")
print("=" * 60)

sql_productos = """
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL CHECK(precio > 0),
    stock INTEGER DEFAULT 0 CHECK(stock >= 0),
    categoria_id INTEGER,
    fecha_creacion TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
)
"""

cursor.execute(sql_productos)
conexion.commit()

print("""
✅ Tabla 'productos' creada

Estructura:
┌────────────────┬─────────┬──────────────────────────────────┐
│ Columna        │ Tipo    │ Restricciones                    │
├────────────────┼─────────┼──────────────────────────────────┤
│ id             │ INTEGER │ PRIMARY KEY AUTOINCREMENT        │
│ nombre         │ TEXT    │ NOT NULL                         │
│ precio         │ REAL    │ NOT NULL CHECK(precio > 0)       │
│ stock          │ INTEGER │ DEFAULT 0 CHECK(stock >= 0)      │
│ categoria_id   │ INTEGER │ FOREIGN KEY → categorias(id)     │
│ fecha_creacion │ TEXT    │ DEFAULT CURRENT_TIMESTAMP        │
└────────────────┴─────────┴──────────────────────────────────┘

Novedades:
- CHECK(precio > 0): El precio DEBE ser positivo
- CHECK(stock >= 0): El stock no puede ser negativo
- FOREIGN KEY: categoria_id referencia a categorias(id)
- CURRENT_TIMESTAMP: Fecha/hora actual automática
""")

# ============================================================================
# 6. CREAR TABLA DE CLIENTES
# ============================================================================
print("=" * 60)
print("👥 Creando tabla: clientes")
print("=" * 60)

sql_clientes = """
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    telefono TEXT,
    direccion TEXT,
    fecha_registro TEXT DEFAULT CURRENT_TIMESTAMP
)
"""

cursor.execute(sql_clientes)
conexion.commit()

print("""
✅ Tabla 'clientes' creada

Estructura:
┌────────────────┬─────────┬──────────────────────────────┐
│ Columna        │ Tipo    │ Restricciones                │
├────────────────┼─────────┼──────────────────────────────┤
│ id             │ INTEGER │ PRIMARY KEY AUTOINCREMENT    │
│ nombre         │ TEXT    │ NOT NULL                     │
│ email          │ TEXT    │ UNIQUE NOT NULL              │
│ telefono       │ TEXT    │ (opcional)                   │
│ direccion      │ TEXT    │ (opcional)                   │
│ fecha_registro │ TEXT    │ DEFAULT CURRENT_TIMESTAMP    │
└────────────────┴─────────┴──────────────────────────────┘
""")

# ============================================================================
# 7. CREAR TABLA DE VENTAS (Relación muchos a muchos)
# ============================================================================
print("=" * 60)
print("🧾 Creando tabla: ventas")
print("=" * 60)

sql_ventas = """
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    precio_unitario REAL NOT NULL,
    total REAL NOT NULL,
    fecha TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
)
"""

cursor.execute(sql_ventas)
conexion.commit()

print("""
✅ Tabla 'ventas' creada

Estructura:
┌────────────────┬─────────┬──────────────────────────────────┐
│ Columna        │ Tipo    │ Restricciones                    │
├────────────────┼─────────┼──────────────────────────────────┤
│ id             │ INTEGER │ PRIMARY KEY AUTOINCREMENT        │
│ cliente_id     │ INTEGER │ NOT NULL, FK → clientes(id)      │
│ producto_id    │ INTEGER │ NOT NULL, FK → productos(id)     │
│ cantidad       │ INTEGER │ NOT NULL CHECK(cantidad > 0)     │
│ precio_unitario│ REAL    │ NOT NULL                         │
│ total          │ REAL    │ NOT NULL                         │
│ fecha          │ TEXT    │ DEFAULT CURRENT_TIMESTAMP        │
└────────────────┴─────────┴──────────────────────────────────┘

Esta tabla conecta clientes con productos (relación N:M)
""")

# ============================================================================
# 8. VER LAS TABLAS CREADAS
# ============================================================================
print("=" * 60)
print("📋 Verificando tablas creadas")
print("=" * 60)

# SQLite guarda información de tablas en sqlite_master
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tablas = cursor.fetchall()

print("Tablas en la base de datos 'tienda.db':")
print("-" * 40)
for tabla in tablas:
    print(f"  📁 {tabla[0]}")

# ============================================================================
# 9. VER ESTRUCTURA DE UNA TABLA
# ============================================================================
print("\n" + "=" * 60)
print("🔍 Ver estructura de una tabla (PRAGMA)")
print("=" * 60)

print("Estructura de la tabla 'productos':")
print("-" * 60)

cursor.execute("PRAGMA table_info(productos)")
columnas = cursor.fetchall()

print(f"{'#':<3} {'Nombre':<16} {'Tipo':<10} {'NotNull':<8} {'Default':<20}")
print("-" * 60)
for col in columnas:
    cid, nombre, tipo, notnull, default, pk = col
    print(f"{cid:<3} {nombre:<16} {tipo:<10} {'Sí' if notnull else 'No':<8} {str(default):<20}")

# ============================================================================
# 10. ELIMINAR UNA TABLA (DROP TABLE)
# ============================================================================
print("\n" + "=" * 60)
print("🗑️ Eliminar una tabla (DROP TABLE)")
print("=" * 60)

print("""
Para eliminar una tabla usamos DROP TABLE:

    DROP TABLE nombre_tabla;

Para evitar errores si no existe:

    DROP TABLE IF EXISTS nombre_tabla;

⚠️ ¡CUIDADO! Esto elimina TODA la tabla y sus datos.
   No se puede deshacer.

Ejemplo (no lo ejecutaremos):
    cursor.execute("DROP TABLE IF EXISTS tabla_temporal")
""")

# ============================================================================
# 11. MODIFICAR UNA TABLA (ALTER TABLE)
# ============================================================================
print("=" * 60)
print("✏️ Modificar una tabla (ALTER TABLE)")
print("=" * 60)

print("""
SQLite tiene soporte LIMITADO para ALTER TABLE:

✅ Puedes agregar columnas:
    ALTER TABLE productos ADD COLUMN descuento REAL DEFAULT 0;

❌ NO puedes eliminar columnas directamente
❌ NO puedes modificar columnas existentes

Si necesitas cambios grandes, debes:
1. Crear una tabla nueva
2. Copiar los datos
3. Eliminar la tabla vieja
4. Renombrar la nueva
""")

# Agregar columna de ejemplo
try:
    cursor.execute("ALTER TABLE productos ADD COLUMN descuento REAL DEFAULT 0")
    conexion.commit()
    print("✅ Columna 'descuento' agregada a productos")
except sqlite3.OperationalError:
    print("ℹ️ La columna 'descuento' ya existe")

# Cerrar conexión
conexion.close()

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 60)
print("📝 RESUMEN - Paso 2")
print("=" * 60)

print("""
Has aprendido:

1️⃣ Crear tablas:
   CREATE TABLE nombre (columnas...)

2️⃣ Tipos de datos:
   INTEGER, REAL, TEXT, BLOB, NULL

3️⃣ Restricciones importantes:
   PRIMARY KEY, NOT NULL, UNIQUE, DEFAULT, CHECK, FOREIGN KEY

4️⃣ Claves foráneas:
   FOREIGN KEY (columna) REFERENCES otra_tabla(id)

5️⃣ Ver tablas existentes:
   SELECT name FROM sqlite_master WHERE type='table'

6️⃣ Ver estructura de tabla:
   PRAGMA table_info(nombre_tabla)

7️⃣ Eliminar tabla:
   DROP TABLE IF EXISTS nombre_tabla

8️⃣ Agregar columna:
   ALTER TABLE tabla ADD COLUMN columna TIPO

📁 Base de datos creada: datos/tienda.db
   Con tablas: categorias, productos, clientes, ventas

🎯 Siguiente paso: 03_insertar_datos.py
""")

print("✅ ¡Felicidades! Has completado el Paso 2")
print("=" * 60)
