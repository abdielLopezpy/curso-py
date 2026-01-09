# ============================================================================
# PASO 4: Consultar Datos en SQLite (SELECT)
# ============================================================================
# En este archivo aprenderás:
# - Cómo consultar datos con SELECT
# - Filtrar con WHERE
# - Ordenar con ORDER BY
# - Limitar resultados con LIMIT
# - Funciones de agregación (COUNT, SUM, AVG, etc.)
# - Agrupar con GROUP BY
# ============================================================================

import sqlite3

print("=" * 60)
print("🎓 PASO 4: Consultar Datos (SELECT)")
print("=" * 60)

# Conectar a la base de datos de la tienda
conexion = sqlite3.connect('datos/tienda.db')
cursor = conexion.cursor()

# ============================================================================
# 1. SINTAXIS BÁSICA DE SELECT
# ============================================================================
print("""
📚 Sintaxis básica de SELECT:

    SELECT columnas FROM tabla;

Ejemplos:
    SELECT * FROM productos;           -- Todas las columnas
    SELECT nombre, precio FROM productos;  -- Columnas específicas
    SELECT DISTINCT categoria_id FROM productos;  -- Sin duplicados
""")

input("Presiona ENTER para ver ejemplos...")

# ============================================================================
# 2. SELECCIONAR TODAS LAS COLUMNAS (*)
# ============================================================================
print("\n" + "=" * 60)
print("🔍 SELECT * - Todas las columnas")
print("=" * 60)

cursor.execute("SELECT * FROM categorias")
categorias = cursor.fetchall()

print("Todas las categorías:")
print("-" * 50)
for cat in categorias:
    print(f"  ID: {cat[0]} | Nombre: {cat[1]} | Desc: {cat[2]}")

print(f"\nTotal: {len(categorias)} categorías")

# ============================================================================
# 3. SELECCIONAR COLUMNAS ESPECÍFICAS
# ============================================================================
print("\n" + "=" * 60)
print("🔍 SELECT columnas específicas")
print("=" * 60)

cursor.execute("SELECT nombre, precio FROM productos")
productos = cursor.fetchall()

print("Productos (nombre y precio):")
print("-" * 40)
for nombre, precio in productos:
    print(f"  {nombre:<25} ${precio:.2f}")

# ============================================================================
# 4. FILTRAR CON WHERE
# ============================================================================
print("\n" + "=" * 60)
print("🔎 WHERE - Filtrar resultados")
print("=" * 60)

print("""
Operadores de comparación:
=   Igual              <>  Diferente
>   Mayor que          <   Menor que
>=  Mayor o igual      <=  Menor o igual
""")

# Productos con precio mayor a 50
print("Productos con precio > $50:")
print("-" * 50)

cursor.execute("SELECT nombre, precio FROM productos WHERE precio > 50")
for nombre, precio in cursor.fetchall():
    print(f"  {nombre:<25} ${precio:.2f}")

# ============================================================================
# 5. OPERADORES LÓGICOS (AND, OR, NOT)
# ============================================================================
print("\n" + "=" * 60)
print("🔎 AND, OR, NOT - Combinar condiciones")
print("=" * 60)

# Productos baratos Y con stock alto
print("Productos baratos (< $50) Y con stock alto (> 30):")
print("-" * 50)

cursor.execute("""
    SELECT nombre, precio, stock
    FROM productos
    WHERE precio < 50 AND stock > 30
""")
for nombre, precio, stock in cursor.fetchall():
    print(f"  {nombre:<25} ${precio:.2f}  Stock: {stock}")

# Productos de electrónica O libros
print("\nProductos de Electrónica (cat 1) O Libros (cat 5):")
print("-" * 50)

cursor.execute("""
    SELECT nombre, precio, categoria_id
    FROM productos
    WHERE categoria_id = 1 OR categoria_id = 5
""")
for nombre, precio, cat in cursor.fetchall():
    print(f"  {nombre:<25} ${precio:.2f}  Cat: {cat}")

# ============================================================================
# 6. LIKE - Buscar patrones de texto
# ============================================================================
print("\n" + "=" * 60)
print("🔎 LIKE - Buscar patrones de texto")
print("=" * 60)

print("""
Comodines:
%  = Cualquier cantidad de caracteres
_  = Un solo carácter

Ejemplos:
'A%'     → Empieza con A
'%a'     → Termina con a
'%ana%'  → Contiene 'ana'
'_a%'    → Segunda letra es 'a'
""")

# Productos que contienen "Bluetooth" o empiezan con "L"
print("Productos que empiezan con 'L':")
cursor.execute("SELECT nombre FROM productos WHERE nombre LIKE 'L%'")
for (nombre,) in cursor.fetchall():
    print(f"  - {nombre}")

print("\nProductos que contienen 'Code':")
cursor.execute("SELECT nombre FROM productos WHERE nombre LIKE '%Code%'")
for (nombre,) in cursor.fetchall():
    print(f"  - {nombre}")

# ============================================================================
# 7. IN - Buscar en una lista
# ============================================================================
print("\n" + "=" * 60)
print("🔎 IN - Buscar en una lista de valores")
print("=" * 60)

print("Productos en categorías 1, 4 o 5:")
print("-" * 50)

cursor.execute("""
    SELECT nombre, precio, categoria_id
    FROM productos
    WHERE categoria_id IN (1, 4, 5)
""")
for nombre, precio, cat in cursor.fetchall():
    print(f"  {nombre:<25} ${precio:.2f}  Cat: {cat}")

# ============================================================================
# 8. BETWEEN - Rango de valores
# ============================================================================
print("\n" + "=" * 60)
print("🔎 BETWEEN - Rango de valores")
print("=" * 60)

print("Productos con precio entre $30 y $100:")
print("-" * 50)

cursor.execute("""
    SELECT nombre, precio
    FROM productos
    WHERE precio BETWEEN 30 AND 100
""")
for nombre, precio in cursor.fetchall():
    print(f"  {nombre:<25} ${precio:.2f}")

# ============================================================================
# 9. ORDER BY - Ordenar resultados
# ============================================================================
print("\n" + "=" * 60)
print("📊 ORDER BY - Ordenar resultados")
print("=" * 60)

print("""
Sintaxis:
    ORDER BY columna ASC   -- Ascendente (A-Z, 1-9)
    ORDER BY columna DESC  -- Descendente (Z-A, 9-1)
""")

# Productos ordenados por precio (más caro primero)
print("Productos ordenados por precio (más caro primero):")
print("-" * 50)

cursor.execute("""
    SELECT nombre, precio
    FROM productos
    ORDER BY precio DESC
""")
for nombre, precio in cursor.fetchall():
    print(f"  {nombre:<25} ${precio:.2f}")

# ============================================================================
# 10. LIMIT - Limitar cantidad de resultados
# ============================================================================
print("\n" + "=" * 60)
print("📊 LIMIT - Limitar resultados")
print("=" * 60)

print("Top 3 productos más caros:")
print("-" * 40)

cursor.execute("""
    SELECT nombre, precio
    FROM productos
    ORDER BY precio DESC
    LIMIT 3
""")
for i, (nombre, precio) in enumerate(cursor.fetchall(), 1):
    print(f"  {i}. {nombre:<25} ${precio:.2f}")

# LIMIT con OFFSET (para paginación)
print("\nProductos 4 al 6 (LIMIT 3 OFFSET 3):")
print("-" * 40)

cursor.execute("""
    SELECT nombre, precio
    FROM productos
    ORDER BY precio DESC
    LIMIT 3 OFFSET 3
""")
for nombre, precio in cursor.fetchall():
    print(f"  - {nombre:<25} ${precio:.2f}")

# ============================================================================
# 11. FUNCIONES DE AGREGACIÓN
# ============================================================================
print("\n" + "=" * 60)
print("📈 Funciones de Agregación")
print("=" * 60)

print("""
Funciones disponibles:
COUNT()  - Contar registros
SUM()    - Sumar valores
AVG()    - Promedio
MAX()    - Valor máximo
MIN()    - Valor mínimo
""")

# COUNT - Contar productos
cursor.execute("SELECT COUNT(*) FROM productos")
total = cursor.fetchone()[0]
print(f"📊 Total de productos: {total}")

# SUM - Suma de precios
cursor.execute("SELECT SUM(precio) FROM productos")
suma = cursor.fetchone()[0]
print(f"💰 Suma de todos los precios: ${suma:.2f}")

# AVG - Precio promedio
cursor.execute("SELECT AVG(precio) FROM productos")
promedio = cursor.fetchone()[0]
print(f"📉 Precio promedio: ${promedio:.2f}")

# MAX y MIN
cursor.execute("SELECT MAX(precio), MIN(precio) FROM productos")
maximo, minimo = cursor.fetchone()
print(f"⬆️ Precio más alto: ${maximo:.2f}")
print(f"⬇️ Precio más bajo: ${minimo:.2f}")

# ============================================================================
# 12. GROUP BY - Agrupar resultados
# ============================================================================
print("\n" + "=" * 60)
print("📊 GROUP BY - Agrupar resultados")
print("=" * 60)

print("Productos por categoría:")
print("-" * 40)

cursor.execute("""
    SELECT categoria_id, COUNT(*) as cantidad, AVG(precio) as precio_prom
    FROM productos
    GROUP BY categoria_id
""")
for cat_id, cantidad, precio_prom in cursor.fetchall():
    print(f"  Categoría {cat_id}: {cantidad} productos, Precio prom: ${precio_prom:.2f}")

# GROUP BY con HAVING (filtrar grupos)
print("\nCategorías con más de 2 productos (HAVING):")
print("-" * 40)

cursor.execute("""
    SELECT categoria_id, COUNT(*) as cantidad
    FROM productos
    GROUP BY categoria_id
    HAVING cantidad > 2
""")
for cat_id, cantidad in cursor.fetchall():
    print(f"  Categoría {cat_id}: {cantidad} productos")

# ============================================================================
# 13. ALIAS - Renombrar columnas y tablas
# ============================================================================
print("\n" + "=" * 60)
print("🏷️ AS - Alias para columnas y tablas")
print("=" * 60)

cursor.execute("""
    SELECT
        nombre AS producto,
        precio AS costo,
        stock AS disponible
    FROM productos
    WHERE precio > 100
""")

print("Productos costosos (con alias):")
print("-" * 50)
for producto, costo, disponible in cursor.fetchall():
    print(f"  Producto: {producto}")
    print(f"  Costo: ${costo:.2f}")
    print(f"  Disponible: {disponible} unidades")
    print()

# ============================================================================
# 14. MÉTODOS PARA OBTENER RESULTADOS
# ============================================================================
print("=" * 60)
print("📋 Métodos para obtener resultados")
print("=" * 60)

print("""
fetchone()   → Obtiene UN registro (o None)
fetchall()   → Obtiene TODOS los registros (lista)
fetchmany(n) → Obtiene N registros

También puedes iterar directamente sobre el cursor:
    for fila in cursor:
        print(fila)
""")

# Ejemplo con fetchone
cursor.execute("SELECT * FROM productos WHERE id = 1")
producto = cursor.fetchone()
if producto:
    print(f"Producto ID 1: {producto[1]} - ${producto[2]}")

# Cerrar conexión
conexion.close()

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 60)
print("📝 RESUMEN - Paso 4")
print("=" * 60)

print("""
Has aprendido:

1️⃣ SELECT básico:
   SELECT * FROM tabla
   SELECT col1, col2 FROM tabla

2️⃣ Filtrar con WHERE:
   WHERE precio > 50
   WHERE nombre LIKE '%texto%'
   WHERE id IN (1, 2, 3)
   WHERE precio BETWEEN 10 AND 100

3️⃣ Operadores lógicos:
   AND, OR, NOT

4️⃣ Ordenar:
   ORDER BY columna ASC/DESC

5️⃣ Limitar:
   LIMIT 10
   LIMIT 10 OFFSET 20

6️⃣ Funciones de agregación:
   COUNT(), SUM(), AVG(), MAX(), MIN()

7️⃣ Agrupar:
   GROUP BY columna
   HAVING condicion

8️⃣ Alias:
   SELECT nombre AS producto

🎯 Siguiente paso: 05_actualizar_eliminar.py
""")

print("✅ ¡Felicidades! Has completado el Paso 4")
print("=" * 60)
