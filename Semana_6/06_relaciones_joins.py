# ============================================================================
# PASO 6: Relaciones y JOINs en SQLite
# ============================================================================
# En este archivo aprenderás:
# - Cómo relacionar tablas
# - Tipos de JOINs (INNER, LEFT, RIGHT)
# - Consultas con múltiples tablas
# - Buenas prácticas para diseño relacional
# ============================================================================

import sqlite3

print("=" * 60)
print("🎓 PASO 6: Relaciones y JOINs")
print("=" * 60)

# Conectar a la base de datos de la tienda
conexion = sqlite3.connect('datos/tienda.db')
cursor = conexion.cursor()

# ============================================================================
# 1. ¿QUÉ SON LAS RELACIONES?
# ============================================================================
print("""
📚 ¿Qué son las relaciones entre tablas?

Las relaciones conectan datos de diferentes tablas usando
CLAVES FORÁNEAS (Foreign Keys).

Ejemplo:
┌─────────────────┐         ┌─────────────────┐
│    PRODUCTOS    │         │   CATEGORIAS    │
├─────────────────┤         ├─────────────────┤
│ id              │         │ id ◄────────────┤
│ nombre          │         │ nombre          │
│ categoria_id ───┼────────►│ descripcion     │
└─────────────────┘         └─────────────────┘

'categoria_id' en productos REFERENCIA a 'id' en categorias.
""")

input("Presiona ENTER para continuar...")

# ============================================================================
# 2. TIPOS DE RELACIONES
# ============================================================================
print("\n" + "=" * 60)
print("🔗 Tipos de Relaciones")
print("=" * 60)

print("""
1️⃣ UNO A UNO (1:1)
   Un usuario tiene UN perfil.
   Usuario (1) ─── (1) Perfil

2️⃣ UNO A MUCHOS (1:N)
   Una categoría tiene MUCHOS productos.
   Categoría (1) ─── (N) Productos

3️⃣ MUCHOS A MUCHOS (N:M)
   Un estudiante tiene MUCHOS cursos.
   Un curso tiene MUCHOS estudiantes.
   Estudiante (N) ─── (M) Cursos
   (Requiere tabla intermedia)
""")

# ============================================================================
# 3. CONSULTA SIN JOIN (Problema)
# ============================================================================
print("=" * 60)
print("❌ Consulta SIN JOIN - El problema")
print("=" * 60)

# Consulta simple de productos
cursor.execute("SELECT nombre, precio, categoria_id FROM productos LIMIT 5")
productos = cursor.fetchall()

print("Productos (solo vemos el ID de categoría, no el nombre):")
print("-" * 50)
for nombre, precio, cat_id in productos:
    print(f"  {nombre:<25} ${precio:<8} Cat ID: {cat_id}")

print("""
❌ El problema: Solo vemos categoria_id = 1, 2, etc.
   ¡Queremos ver el NOMBRE de la categoría!

✅ Solución: Usar JOIN para combinar tablas.
""")

# ============================================================================
# 4. INNER JOIN - Combinar tablas
# ============================================================================
print("=" * 60)
print("🔗 INNER JOIN - Combinar tablas")
print("=" * 60)

print("""
INNER JOIN devuelve solo las filas que tienen
coincidencias en AMBAS tablas.

Sintaxis:
    SELECT columnas
    FROM tabla1
    INNER JOIN tabla2 ON tabla1.columna = tabla2.columna
""")

# Productos con nombre de categoría
cursor.execute("""
    SELECT
        productos.nombre,
        productos.precio,
        categorias.nombre AS categoria
    FROM productos
    INNER JOIN categorias ON productos.categoria_id = categorias.id
""")

print("\nProductos con nombre de categoría (INNER JOIN):")
print("-" * 60)
for nombre, precio, categoria in cursor.fetchall():
    print(f"  {nombre:<25} ${precio:<8.2f} [{categoria}]")

# ============================================================================
# 5. ALIAS DE TABLAS
# ============================================================================
print("\n" + "=" * 60)
print("🏷️ Alias de Tablas - Código más limpio")
print("=" * 60)

print("""
Puedes usar alias para nombres de tabla más cortos:

    SELECT p.nombre, c.nombre
    FROM productos AS p
    INNER JOIN categorias AS c ON p.categoria_id = c.id

O sin AS:
    FROM productos p
    INNER JOIN categorias c ON ...
""")

# Misma consulta con alias
cursor.execute("""
    SELECT p.nombre, p.precio, c.nombre AS categoria
    FROM productos p
    INNER JOIN categorias c ON p.categoria_id = c.id
    WHERE p.precio > 50
    ORDER BY p.precio DESC
""")

print("Productos > $50 con categoría (usando alias):")
print("-" * 60)
for nombre, precio, categoria in cursor.fetchall():
    print(f"  {nombre:<25} ${precio:<8.2f} [{categoria}]")

# ============================================================================
# 6. LEFT JOIN
# ============================================================================
print("\n" + "=" * 60)
print("⬅️ LEFT JOIN - Todos de la izquierda")
print("=" * 60)

print("""
LEFT JOIN devuelve TODAS las filas de la tabla izquierda,
aunque no tengan coincidencias en la tabla derecha.

    Tabla A LEFT JOIN Tabla B
    ─────────────────────────
    [A] [A ∩ B]
    Todos de A + coincidencias de B
""")

# Primero, crear una categoría sin productos
cursor.execute("""
    INSERT OR IGNORE INTO categorias (nombre, descripcion)
    VALUES ('Juguetes', 'Juguetes y juegos')
""")
conexion.commit()

# LEFT JOIN para ver todas las categorías
cursor.execute("""
    SELECT
        c.nombre AS categoria,
        COUNT(p.id) AS total_productos
    FROM categorias c
    LEFT JOIN productos p ON c.id = p.categoria_id
    GROUP BY c.id
""")

print("Todas las categorías con conteo de productos:")
print("-" * 40)
for categoria, total in cursor.fetchall():
    print(f"  {categoria:<15} {total} productos")

print("""
📝 Nota: 'Juguetes' aparece con 0 productos.
   Con INNER JOIN no aparecería.
""")

# ============================================================================
# 7. MÚLTIPLES JOINS
# ============================================================================
print("=" * 60)
print("🔗🔗 Múltiples JOINs - Conectar 3+ tablas")
print("=" * 60)

# Insertar algunas ventas para el ejemplo
ventas_ejemplo = [
    (1, 1, 2, 849.99, 1699.98),  # Ana compró 2 Laptops
    (1, 3, 3, 79.99, 239.97),    # Ana compró 3 Audífonos
    (2, 4, 1, 35.99, 35.99),     # Luis compró 1 Camiseta
    (3, 9, 2, 39.99, 79.98)      # María compró 2 libros
]

for cli_id, prod_id, cant, precio, total in ventas_ejemplo:
    try:
        cursor.execute("""
            INSERT INTO ventas (cliente_id, producto_id, cantidad,
                               precio_unitario, total)
            VALUES (?, ?, ?, ?, ?)
        """, (cli_id, prod_id, cant, precio, total))
    except sqlite3.IntegrityError:
        pass

conexion.commit()

# Consulta con 3 tablas
cursor.execute("""
    SELECT
        c.nombre AS cliente,
        p.nombre AS producto,
        v.cantidad,
        v.total
    FROM ventas v
    INNER JOIN clientes c ON v.cliente_id = c.id
    INNER JOIN productos p ON v.producto_id = p.id
    ORDER BY v.fecha DESC
""")

print("Historial de ventas (3 tablas: ventas, clientes, productos):")
print("-" * 65)
print(f"{'Cliente':<15} {'Producto':<25} {'Cant':>5} {'Total':>10}")
print("-" * 65)
for cliente, producto, cantidad, total in cursor.fetchall():
    print(f"{cliente:<15} {producto:<25} {cantidad:>5} ${total:>9.2f}")

# ============================================================================
# 8. SUBCONSULTAS
# ============================================================================
print("\n" + "=" * 60)
print("📦 SUBCONSULTAS - Consultas anidadas")
print("=" * 60)

print("""
Una subconsulta es un SELECT dentro de otro SELECT.

Ejemplo: Productos más caros que el promedio
""")

# Productos con precio mayor al promedio
cursor.execute("""
    SELECT nombre, precio
    FROM productos
    WHERE precio > (SELECT AVG(precio) FROM productos)
    ORDER BY precio DESC
""")

# Obtener el promedio para mostrarlo
cursor_temp = conexion.cursor()
cursor_temp.execute("SELECT AVG(precio) FROM productos")
promedio = cursor_temp.fetchone()[0]

print(f"Precio promedio: ${promedio:.2f}")
print("\nProductos con precio mayor al promedio:")
print("-" * 45)
for nombre, precio in cursor.fetchall():
    print(f"  {nombre:<30} ${precio:.2f}")

# ============================================================================
# 9. EJEMPLO PRÁCTICO: Reporte de Ventas
# ============================================================================
print("\n" + "=" * 60)
print("📊 Ejemplo Práctico: Reporte de Ventas")
print("=" * 60)

# Reporte: Ventas por cliente con total
cursor.execute("""
    SELECT
        c.nombre AS cliente,
        COUNT(v.id) AS num_compras,
        SUM(v.total) AS total_gastado
    FROM clientes c
    LEFT JOIN ventas v ON c.id = v.cliente_id
    GROUP BY c.id
    ORDER BY total_gastado DESC
""")

print("Reporte de clientes:")
print("-" * 55)
print(f"{'Cliente':<20} {'# Compras':>12} {'Total Gastado':>18}")
print("-" * 55)
for cliente, compras, total in cursor.fetchall():
    total_str = f"${total:.2f}" if total else "$0.00"
    print(f"{cliente:<20} {compras:>12} {total_str:>18}")

# Ventas por categoría
cursor.execute("""
    SELECT
        cat.nombre AS categoria,
        COUNT(v.id) AS ventas,
        COALESCE(SUM(v.total), 0) AS ingresos
    FROM categorias cat
    LEFT JOIN productos p ON cat.id = p.categoria_id
    LEFT JOIN ventas v ON p.id = v.producto_id
    GROUP BY cat.id
    ORDER BY ingresos DESC
""")

print("\nVentas por categoría:")
print("-" * 45)
print(f"{'Categoría':<15} {'Ventas':>10} {'Ingresos':>15}")
print("-" * 45)
for categoria, ventas, ingresos in cursor.fetchall():
    print(f"{categoria:<15} {ventas:>10} ${ingresos:>14.2f}")

# Cerrar conexión
conexion.close()

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 60)
print("📝 RESUMEN - Paso 6")
print("=" * 60)

print("""
Has aprendido:

1️⃣ Relaciones entre tablas:
   - Clave primaria (PK) identifica registros
   - Clave foránea (FK) conecta tablas

2️⃣ INNER JOIN:
   SELECT * FROM a INNER JOIN b ON a.id = b.a_id
   → Solo filas que coinciden en ambas

3️⃣ LEFT JOIN:
   SELECT * FROM a LEFT JOIN b ON a.id = b.a_id
   → Todas de A + coincidencias de B

4️⃣ Alias de tablas:
   FROM productos p INNER JOIN categorias c ...

5️⃣ Múltiples JOINs:
   FROM a JOIN b ON ... JOIN c ON ...

6️⃣ Subconsultas:
   WHERE precio > (SELECT AVG(precio) FROM ...)

🎯 Siguiente paso: 07_sistema_completo.py
""")

print("✅ ¡Felicidades! Has completado el Paso 6")
print("=" * 60)
