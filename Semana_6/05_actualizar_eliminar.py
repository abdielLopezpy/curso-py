# ============================================================================
# PASO 5: Actualizar y Eliminar Datos (UPDATE / DELETE)
# ============================================================================
# En este archivo aprenderás:
# - Cómo actualizar registros con UPDATE
# - Cómo eliminar registros con DELETE
# - Precauciones importantes
# - Uso de transacciones
# ============================================================================

import sqlite3

print("=" * 60)
print("🎓 PASO 5: Actualizar y Eliminar Datos")
print("=" * 60)

# Conectar a la base de datos de la tienda
conexion = sqlite3.connect('datos/tienda.db')
cursor = conexion.cursor()

# ============================================================================
# 1. SINTAXIS DE UPDATE
# ============================================================================
print("""
📚 Sintaxis de UPDATE:

    UPDATE tabla
    SET columna1 = valor1, columna2 = valor2
    WHERE condicion;

⚠️ ¡IMPORTANTE! Siempre usa WHERE
   Sin WHERE, se actualizan TODOS los registros.
""")

input("Presiona ENTER para ver ejemplos de UPDATE...")

# ============================================================================
# 2. ACTUALIZAR UN REGISTRO ESPECÍFICO
# ============================================================================
print("\n" + "=" * 60)
print("✏️ UPDATE - Actualizar un registro específico")
print("=" * 60)

# Ver el producto antes
cursor.execute("SELECT id, nombre, precio FROM productos WHERE id = 1")
antes = cursor.fetchone()
print(f"ANTES: ID {antes[0]} | {antes[1]} | ${antes[2]}")

# Actualizar el precio
nuevo_precio = 849.99
cursor.execute("""
    UPDATE productos
    SET precio = ?
    WHERE id = 1
""", (nuevo_precio,))
conexion.commit()

# Ver el producto después
cursor.execute("SELECT id, nombre, precio FROM productos WHERE id = 1")
despues = cursor.fetchone()
print(f"DESPUÉS: ID {despues[0]} | {despues[1]} | ${despues[2]}")
print("✅ Precio actualizado correctamente")

# ============================================================================
# 3. ACTUALIZAR MÚLTIPLES COLUMNAS
# ============================================================================
print("\n" + "=" * 60)
print("✏️ UPDATE - Múltiples columnas a la vez")
print("=" * 60)

# Actualizar nombre, precio y stock de un producto
cursor.execute("""
    UPDATE productos
    SET nombre = ?, precio = ?, stock = ?
    WHERE id = 2
""", ("Samsung Galaxy S24", 799.99, 25))
conexion.commit()

# Verificar
cursor.execute("SELECT nombre, precio, stock FROM productos WHERE id = 2")
prod = cursor.fetchone()
print("Producto actualizado:")
print(f"  Nombre: {prod[0]}")
print(f"  Precio: ${prod[1]}")
print(f"  Stock: {prod[2]}")

# ============================================================================
# 4. ACTUALIZAR CON EXPRESIONES
# ============================================================================
print("\n" + "=" * 60)
print("✏️ UPDATE - Usar expresiones y cálculos")
print("=" * 60)

# Aumentar el stock de todos los productos en 10
print("Aumentando stock de TODOS los productos en 10 unidades...")

cursor.execute("UPDATE productos SET stock = stock + 10")
conexion.commit()

filas_afectadas = cursor.rowcount
print(f"✅ {filas_afectadas} productos actualizados")

# Aplicar 10% de descuento a productos de categoría 1
print("\nAplicando 10% de descuento a Electrónica (cat 1)...")

cursor.execute("""
    UPDATE productos
    SET precio = precio * 0.90
    WHERE categoria_id = 1
""")
conexion.commit()

print(f"✅ {cursor.rowcount} productos con descuento aplicado")

# Ver productos actualizados
cursor.execute("""
    SELECT nombre, precio FROM productos WHERE categoria_id = 1
""")
print("\nProductos de Electrónica con nuevo precio:")
for nombre, precio in cursor.fetchall():
    print(f"  {nombre}: ${precio:.2f}")

# ============================================================================
# 5. SINTAXIS DE DELETE
# ============================================================================
print("\n" + "=" * 60)
print("🗑️ DELETE - Sintaxis básica")
print("=" * 60)

print("""
📚 Sintaxis de DELETE:

    DELETE FROM tabla WHERE condicion;

⚠️ ¡MUY IMPORTANTE! Siempre usa WHERE
   Sin WHERE, se eliminan TODOS los registros.

Ejemplo seguro:
    DELETE FROM productos WHERE id = 5;

Ejemplo PELIGROSO (borra todo):
    DELETE FROM productos;  -- ¡CUIDADO!
""")

input("Presiona ENTER para ver ejemplos de DELETE...")

# ============================================================================
# 6. ELIMINAR UN REGISTRO ESPECÍFICO
# ============================================================================
print("\n" + "=" * 60)
print("🗑️ DELETE - Eliminar un registro específico")
print("=" * 60)

# Primero, insertar un producto temporal para eliminar
cursor.execute("""
    INSERT INTO productos (nombre, precio, stock, categoria_id)
    VALUES ('Producto Temporal', 9.99, 1, 1)
""")
conexion.commit()
id_temporal = cursor.lastrowid
print(f"Producto temporal insertado con ID: {id_temporal}")

# Contar productos antes
cursor.execute("SELECT COUNT(*) FROM productos")
antes = cursor.fetchone()[0]
print(f"Total productos antes: {antes}")

# Eliminar el producto temporal
cursor.execute("DELETE FROM productos WHERE id = ?", (id_temporal,))
conexion.commit()
print(f"✅ Producto con ID {id_temporal} eliminado")

# Contar productos después
cursor.execute("SELECT COUNT(*) FROM productos")
despues = cursor.fetchone()[0]
print(f"Total productos después: {despues}")

# ============================================================================
# 7. ELIMINAR CON CONDICIONES
# ============================================================================
print("\n" + "=" * 60)
print("🗑️ DELETE - Eliminar con condiciones")
print("=" * 60)

# Insertar algunos productos para demostración
productos_temp = [
    ("Producto Demo 1", 5.00, 0, 3),
    ("Producto Demo 2", 3.00, 0, 3),
    ("Producto Demo 3", 2.00, 0, 3)
]
cursor.executemany("""
    INSERT INTO productos (nombre, precio, stock, categoria_id)
    VALUES (?, ?, ?, ?)
""", productos_temp)
conexion.commit()
print("Insertados 3 productos demo con stock = 0")

# Eliminar productos sin stock (stock = 0)
cursor.execute("DELETE FROM productos WHERE stock = 0")
conexion.commit()
print(f"✅ {cursor.rowcount} productos sin stock eliminados")

# ============================================================================
# 8. TRANSACCIONES - Agrupar operaciones
# ============================================================================
print("\n" + "=" * 60)
print("🔄 TRANSACCIONES - Todo o nada")
print("=" * 60)

print("""
Una TRANSACCIÓN agrupa varias operaciones.
Si algo falla, se puede deshacer TODO.

Métodos:
- commit()   → Confirmar cambios
- rollback() → Deshacer cambios

Ejemplo de transferencia bancaria:
1. Restar dinero de cuenta A
2. Sumar dinero a cuenta B
Si el paso 2 falla, rollback() deshace el paso 1.
""")

# Ejemplo de transacción
print("\nEjemplo: Transferir stock entre productos")

try:
    # Verificar stock actual
    cursor.execute("SELECT stock FROM productos WHERE id = 1")
    stock_origen = cursor.fetchone()[0]
    print(f"Stock producto 1 antes: {stock_origen}")

    # Restar del producto 1
    cursor.execute("UPDATE productos SET stock = stock - 5 WHERE id = 1")

    # Sumar al producto 2
    cursor.execute("UPDATE productos SET stock = stock + 5 WHERE id = 2")

    # Confirmar
    conexion.commit()
    print("✅ Transferencia exitosa")

    # Verificar
    cursor.execute("SELECT stock FROM productos WHERE id = 1")
    print(f"Stock producto 1 después: {cursor.fetchone()[0]}")

except Exception as e:
    # Si hay error, deshacer todo
    conexion.rollback()
    print(f"❌ Error, cambios revertidos: {e}")

# ============================================================================
# 9. ROLLBACK - Deshacer cambios
# ============================================================================
print("\n" + "=" * 60)
print("⏪ ROLLBACK - Deshacer cambios")
print("=" * 60)

# Ver precio actual
cursor.execute("SELECT precio FROM productos WHERE id = 1")
precio_original = cursor.fetchone()[0]
print(f"Precio original: ${precio_original}")

# Hacer un cambio
cursor.execute("UPDATE productos SET precio = 9999.99 WHERE id = 1")
print("Precio cambiado a $9999.99 (sin commit)")

# Verificar en memoria
cursor.execute("SELECT precio FROM productos WHERE id = 1")
print(f"Precio en memoria: ${cursor.fetchone()[0]}")

# Deshacer
conexion.rollback()
print("ROLLBACK ejecutado")

# Verificar después del rollback
cursor.execute("SELECT precio FROM productos WHERE id = 1")
print(f"Precio después de rollback: ${cursor.fetchone()[0]}")
print("✅ El cambio fue revertido")

# ============================================================================
# 10. PRECAUCIONES IMPORTANTES
# ============================================================================
print("\n" + "=" * 60)
print("⚠️ PRECAUCIONES IMPORTANTES")
print("=" * 60)

print("""
1️⃣ SIEMPRE usa WHERE en UPDATE y DELETE
   Sin WHERE afectas TODOS los registros

2️⃣ Haz BACKUP antes de operaciones masivas
   Copia el archivo .db antes de cambios grandes

3️⃣ Usa transacciones para operaciones críticas
   Si algo falla, puedes hacer rollback

4️⃣ Verifica con SELECT antes de UPDATE/DELETE
   SELECT * FROM tabla WHERE condicion;
   -- Si es lo que quieres, entonces:
   UPDATE/DELETE ... WHERE condicion;

5️⃣ Usa parámetros (?) para evitar SQL injection
   NUNCA: f"DELETE FROM t WHERE id = {id}"
   SIEMPRE: "DELETE FROM t WHERE id = ?", (id,)
""")

# Cerrar conexión
conexion.close()

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 60)
print("📝 RESUMEN - Paso 5")
print("=" * 60)

print("""
Has aprendido:

1️⃣ UPDATE básico:
   UPDATE tabla SET col = valor WHERE condicion

2️⃣ UPDATE múltiples columnas:
   UPDATE tabla SET col1 = v1, col2 = v2 WHERE ...

3️⃣ UPDATE con expresiones:
   UPDATE tabla SET precio = precio * 0.9 WHERE ...

4️⃣ DELETE básico:
   DELETE FROM tabla WHERE condicion

5️⃣ Transacciones:
   - commit() para confirmar
   - rollback() para deshacer

6️⃣ Contar filas afectadas:
   cursor.rowcount

⚠️ REGLA DE ORO:
   Siempre usa WHERE en UPDATE y DELETE

🎯 Siguiente paso: 06_relaciones_joins.py
""")

print("✅ ¡Felicidades! Has completado el Paso 5")
print("=" * 60)
