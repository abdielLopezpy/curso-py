# ============================================================================
# PASO 3: Insertar Datos en SQLite (INSERT)
# ============================================================================
# En este archivo aprenderás:
# - Cómo insertar registros con INSERT
# - Insertar un registro
# - Insertar múltiples registros
# - Usar parámetros seguros (evitar SQL Injection)
# - Obtener el ID del último registro insertado
# ============================================================================

import sqlite3

print("=" * 60)
print("🎓 PASO 3: Insertar Datos (INSERT)")
print("=" * 60)

# Conectar a la base de datos de la tienda
conexion = sqlite3.connect('datos/tienda.db')
cursor = conexion.cursor()

# ============================================================================
# 1. SINTAXIS BÁSICA DE INSERT
# ============================================================================
print("""
📚 Sintaxis básica de INSERT:

    INSERT INTO tabla (columna1, columna2, ...)
    VALUES (valor1, valor2, ...);

Ejemplo:
    INSERT INTO productos (nombre, precio)
    VALUES ('Laptop', 999.99);

💡 No incluyas el 'id' si es AUTOINCREMENT
   ¡Se genera solo!
""")

input("Presiona ENTER para insertar datos...")

# ============================================================================
# 2. INSERTAR CATEGORÍAS
# ============================================================================
print("\n" + "=" * 60)
print("📦 Insertando categorías...")
print("=" * 60)

# Lista de categorías a insertar
categorias = [
    ("Electrónica", "Dispositivos electrónicos y gadgets"),
    ("Ropa", "Vestimenta y accesorios"),
    ("Hogar", "Artículos para el hogar"),
    ("Deportes", "Equipamiento deportivo"),
    ("Libros", "Libros y material de lectura")
]

# Método 1: Insertar uno por uno con execute()
print("\n📝 Método 1: Insertar uno por uno")
print("-" * 40)

for nombre, descripcion in categorias:
    try:
        cursor.execute(
            "INSERT INTO categorias (nombre, descripcion) VALUES (?, ?)",
            (nombre, descripcion)
        )
        print(f"  ✅ Categoría '{nombre}' insertada")
    except sqlite3.IntegrityError:
        print(f"  ⚠️ Categoría '{nombre}' ya existe (UNIQUE)")

conexion.commit()

# ============================================================================
# 3. USAR PLACEHOLDERS (?) PARA SEGURIDAD
# ============================================================================
print("\n" + "=" * 60)
print("🔒 Usando Placeholders (?) para seguridad")
print("=" * 60)

print("""
⚠️ NUNCA hagas esto (vulnerable a SQL Injection):

    nombre = input("Nombre: ")
    cursor.execute(f"INSERT INTO tabla VALUES ('{nombre}')")

✅ SIEMPRE usa placeholders (?):

    nombre = input("Nombre: ")
    cursor.execute("INSERT INTO tabla (nombre) VALUES (?)", (nombre,))

Los placeholders:
- Escapan caracteres peligrosos automáticamente
- Previenen ataques de inyección SQL
- Son más limpios y legibles
""")

# ============================================================================
# 4. INSERTAR PRODUCTOS
# ============================================================================
print("=" * 60)
print("📦 Insertando productos...")
print("=" * 60)

# Lista de productos: (nombre, precio, stock, categoria_id)
productos = [
    ("Laptop HP", 899.99, 15, 1),
    ("Smartphone Samsung", 699.99, 30, 1),
    ("Audífonos Bluetooth", 79.99, 50, 1),
    ("Camiseta Nike", 35.99, 100, 2),
    ("Pantalón Levi's", 59.99, 45, 2),
    ("Lámpara LED", 24.99, 60, 3),
    ("Balón de Fútbol", 29.99, 25, 4),
    ("Raqueta de Tenis", 89.99, 15, 4),
    ("Python Crash Course", 39.99, 20, 5),
    ("Clean Code", 44.99, 18, 5)
]

print("\n📝 Insertando productos uno por uno...")
print("-" * 40)

for nombre, precio, stock, cat_id in productos:
    try:
        cursor.execute("""
            INSERT INTO productos (nombre, precio, stock, categoria_id)
            VALUES (?, ?, ?, ?)
        """, (nombre, precio, stock, cat_id))
        print(f"  ✅ Producto '{nombre}' insertado (${precio})")
    except sqlite3.IntegrityError as e:
        print(f"  ⚠️ Error con '{nombre}': {e}")

conexion.commit()

# ============================================================================
# 5. INSERTAR MÚLTIPLES REGISTROS CON executemany()
# ============================================================================
print("\n" + "=" * 60)
print("⚡ Insertar múltiples registros con executemany()")
print("=" * 60)

print("""
Para insertar MUCHOS registros de una vez, usa executemany():

    datos = [
        ("valor1", "valor2"),
        ("valor3", "valor4"),
        ("valor5", "valor6")
    ]
    cursor.executemany("INSERT INTO tabla (a, b) VALUES (?, ?)", datos)

¡Es más rápido que múltiples execute()!
""")

# Insertar clientes con executemany
clientes = [
    ("Ana García", "ana@email.com", "555-1234", "Calle 123"),
    ("Luis Pérez", "luis@email.com", "555-5678", "Avenida 456"),
    ("María López", "maria@email.com", "555-9012", "Boulevard 789"),
    ("Carlos Ruiz", "carlos@email.com", "555-3456", "Plaza 321"),
    ("Sofia Torres", "sofia@email.com", "555-7890", "Paseo 654")
]

print("Insertando clientes con executemany()...")
print("-" * 40)

try:
    cursor.executemany("""
        INSERT INTO clientes (nombre, email, telefono, direccion)
        VALUES (?, ?, ?, ?)
    """, clientes)
    print(f"  ✅ {len(clientes)} clientes insertados de una vez")
except sqlite3.IntegrityError:
    print("  ⚠️ Algunos clientes ya existen (email UNIQUE)")

conexion.commit()

# ============================================================================
# 6. OBTENER EL ID DEL ÚLTIMO REGISTRO INSERTADO
# ============================================================================
print("\n" + "=" * 60)
print("🔢 Obtener el ID del último registro insertado")
print("=" * 60)

# Insertar un nuevo producto y obtener su ID
cursor.execute("""
    INSERT INTO productos (nombre, precio, stock, categoria_id)
    VALUES (?, ?, ?, ?)
""", ("Teclado Mecánico", 129.99, 20, 1))

ultimo_id = cursor.lastrowid
conexion.commit()

print(f"""
Se insertó: "Teclado Mecánico"
ID asignado automáticamente: {ultimo_id}

Código:
    cursor.execute("INSERT INTO ...")
    ultimo_id = cursor.lastrowid  # ← Obtener el ID

Útil cuando necesitas el ID para insertar en otra tabla.
""")

# ============================================================================
# 7. INSERT CON SELECT (Copiar datos)
# ============================================================================
print("=" * 60)
print("📋 INSERT con SELECT (copiar datos)")
print("=" * 60)

print("""
Puedes insertar datos de una consulta SELECT:

    INSERT INTO tabla_destino (col1, col2)
    SELECT colA, colB FROM tabla_origen WHERE condicion;

Ejemplo: Crear una tabla de productos caros
""")

# Crear tabla para productos premium
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos_premium (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio REAL
    )
""")

# Copiar productos con precio > 50
cursor.execute("""
    INSERT INTO productos_premium (nombre, precio)
    SELECT nombre, precio FROM productos WHERE precio > 50
""")

filas_insertadas = cursor.rowcount
conexion.commit()

print(f"  ✅ {filas_insertadas} productos premium copiados (precio > $50)")

# ============================================================================
# 8. VERIFICAR LOS DATOS INSERTADOS
# ============================================================================
print("\n" + "=" * 60)
print("🔍 Verificando datos insertados")
print("=" * 60)

# Contar registros en cada tabla
tablas = ['categorias', 'productos', 'clientes', 'productos_premium']

print("Registros por tabla:")
print("-" * 40)
for tabla in tablas:
    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
    cantidad = cursor.fetchone()[0]
    print(f"  📊 {tabla}: {cantidad} registros")

# Mostrar algunos productos
print("\n📦 Muestra de productos:")
print("-" * 50)
cursor.execute("SELECT id, nombre, precio, stock FROM productos LIMIT 5")
for prod in cursor.fetchall():
    print(f"  [{prod[0]}] {prod[1]:<25} ${prod[2]:<8} Stock: {prod[3]}")

# Cerrar conexión
conexion.close()

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 60)
print("📝 RESUMEN - Paso 3")
print("=" * 60)

print("""
Has aprendido:

1️⃣ Sintaxis INSERT básica:
   INSERT INTO tabla (cols) VALUES (vals)

2️⃣ Usar placeholders (?) para seguridad:
   cursor.execute("INSERT ... VALUES (?, ?)", (v1, v2))

3️⃣ Insertar múltiples registros:
   cursor.executemany("INSERT ...", lista_de_tuplas)

4️⃣ Obtener el último ID insertado:
   id = cursor.lastrowid

5️⃣ Contar filas afectadas:
   cantidad = cursor.rowcount

6️⃣ INSERT desde SELECT:
   INSERT INTO destino SELECT ... FROM origen

7️⃣ Siempre hacer commit():
   conexion.commit()

🎯 Siguiente paso: 04_consultar_datos.py
""")

print("✅ ¡Felicidades! Has completado el Paso 3")
print("=" * 60)
