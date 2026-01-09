# ============================================================================
# PASO 1: Introducción a SQLite con Python
# ============================================================================
# En este archivo aprenderás:
# - Qué es SQLite y por qué usarlo
# - Cómo conectarte a una base de datos
# - Crear tu primera base de datos
# - Entender el flujo básico de trabajo
# ============================================================================

import sqlite3
import os

# Crear carpeta para las bases de datos si no existe
if not os.path.exists('datos'):
    os.makedirs('datos')
    print("📁 Carpeta 'datos' creada")

print("=" * 60)
print("🎓 PASO 1: Tu Primera Conexión a SQLite")
print("=" * 60)

# ============================================================================
# 1. ¿QUÉ ES SQLITE?
# ============================================================================
print("""
📚 ¿Qué es SQLite?

SQLite es una base de datos que:
✅ Viene INCLUIDA en Python - no necesitas instalar nada
✅ Guarda todo en UN SOLO ARCHIVO (.db)
✅ Es perfecta para aprender SQL
✅ Es usada por Firefox, Chrome, Android, iOS, etc.

La librería sqlite3 ya viene con Python:
    import sqlite3  # ¡Así de fácil!
""")

input("Presiona ENTER para continuar...")

# ============================================================================
# 2. CONECTAR A UNA BASE DE DATOS
# ============================================================================
print("\n" + "=" * 60)
print("🔌 Conectando a una base de datos...")
print("=" * 60)

# Si el archivo no existe, SQLite lo CREA automáticamente
nombre_archivo = 'datos/mi_primera_base.db'

# Conectar (o crear) la base de datos
conexion = sqlite3.connect(nombre_archivo)

print(f"""
✅ ¡Conexión exitosa!

Archivo creado: {nombre_archivo}

¿Qué pasó?
1. sqlite3.connect() busca el archivo
2. Si NO existe, lo CREA vacío
3. Si existe, lo ABRE
4. Devuelve un objeto 'conexion' para trabajar
""")

# ============================================================================
# 3. EL CURSOR - Tu herramienta para ejecutar SQL
# ============================================================================
print("=" * 60)
print("🖱️ El Cursor - Tu herramienta para ejecutar comandos SQL")
print("=" * 60)

# Crear un cursor
cursor = conexion.cursor()

print("""
El CURSOR es como un "control remoto" para la base de datos.
Con él puedes:
- Ejecutar comandos SQL
- Obtener resultados de consultas
- Navegar por los datos

Código:
    cursor = conexion.cursor()
""")

input("Presiona ENTER para continuar...")

# ============================================================================
# 4. EJECUTAR UN COMANDO SQL SIMPLE
# ============================================================================
print("\n" + "=" * 60)
print("⚡ Ejecutando tu primer comando SQL")
print("=" * 60)

# Crear una tabla simple
sql_crear_tabla = """
CREATE TABLE IF NOT EXISTS saludos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mensaje TEXT NOT NULL,
    fecha TEXT DEFAULT CURRENT_TIMESTAMP
)
"""

cursor.execute(sql_crear_tabla)
conexion.commit()  # ¡Importante! Guardar los cambios

print("""
✅ ¡Tabla 'saludos' creada!

El comando SQL fue:
    CREATE TABLE IF NOT EXISTS saludos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mensaje TEXT NOT NULL,
        fecha TEXT DEFAULT CURRENT_TIMESTAMP
    )

Explicación:
- CREATE TABLE: Crea una nueva tabla
- IF NOT EXISTS: Solo si no existe (evita errores)
- saludos: Nombre de la tabla
- id INTEGER PRIMARY KEY AUTOINCREMENT: ID único automático
- mensaje TEXT NOT NULL: Texto obligatorio
- fecha TEXT DEFAULT CURRENT_TIMESTAMP: Fecha automática
""")

# ============================================================================
# 5. INSERTAR DATOS
# ============================================================================
print("=" * 60)
print("➕ Insertando tu primer registro")
print("=" * 60)

# Insertar un saludo
sql_insertar = "INSERT INTO saludos (mensaje) VALUES (?)"
cursor.execute(sql_insertar, ("¡Hola, SQLite! 🎉",))
conexion.commit()

print("""
✅ ¡Registro insertado!

El comando SQL fue:
    INSERT INTO saludos (mensaje) VALUES (?)

El signo ? es un "placeholder" (marcador de posición).
El valor real se pasa como segundo argumento: ("¡Hola, SQLite!",)

¿Por qué usar ? en lugar del valor directo?
- ✅ Más seguro (previene inyección SQL)
- ✅ Más limpio
- ✅ Mejor práctica
""")

# ============================================================================
# 6. CONSULTAR DATOS
# ============================================================================
print("=" * 60)
print("🔍 Consultando los datos")
print("=" * 60)

# Obtener todos los registros
cursor.execute("SELECT * FROM saludos")
registros = cursor.fetchall()

print("Comando SQL: SELECT * FROM saludos")
print("\nResultados:")
print("-" * 40)

for registro in registros:
    print(f"  ID: {registro[0]}")
    print(f"  Mensaje: {registro[1]}")
    print(f"  Fecha: {registro[2]}")
    print("-" * 40)

print("""
Métodos para obtener resultados:
- fetchone()  → Obtiene UN registro
- fetchall()  → Obtiene TODOS los registros
- fetchmany(n) → Obtiene N registros
""")

# ============================================================================
# 7. CERRAR LA CONEXIÓN
# ============================================================================
print("=" * 60)
print("🔒 Cerrando la conexión")
print("=" * 60)

conexion.close()

print("""
✅ Conexión cerrada correctamente

¡IMPORTANTE! Siempre cierra la conexión cuando termines:
    conexion.close()

O usa el administrador de contexto (with):
    with sqlite3.connect('archivo.db') as conexion:
        cursor = conexion.cursor()
        # ... operaciones ...
    # Se cierra automáticamente aquí
""")

# ============================================================================
# 8. EJEMPLO COMPLETO CON 'with'
# ============================================================================
print("=" * 60)
print("📋 Ejemplo completo usando 'with'")
print("=" * 60)

print("""
La mejor práctica es usar 'with' para manejar la conexión:
""")

# Demostración con 'with'
with sqlite3.connect('datos/mi_primera_base.db') as conn:
    cur = conn.cursor()
    
    # Insertar otro saludo
    cur.execute("INSERT INTO saludos (mensaje) VALUES (?)",
                ("¡Segundo mensaje! 📝",))
    conn.commit()
    
    # Consultar todos
    cur.execute("SELECT * FROM saludos")
    todos = cur.fetchall()
    
    print("Todos los saludos en la base de datos:")
    for fila in todos:
        print(f"  [{fila[0]}] {fila[1]} - {fila[2]}")

# La conexión se cierra automáticamente al salir del 'with'

print("""
✅ El bloque 'with' cerró la conexión automáticamente

Ventajas de usar 'with':
- No puedes olvidar cerrar la conexión
- Es más limpio y pythónico
- Maneja errores automáticamente
""")

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 60)
print("📝 RESUMEN - Paso 1")
print("=" * 60)

print("""
Has aprendido:

1️⃣ Importar sqlite3:
   import sqlite3

2️⃣ Conectar a una base de datos:
   conexion = sqlite3.connect('archivo.db')

3️⃣ Crear un cursor:
   cursor = conexion.cursor()

4️⃣ Ejecutar SQL:
   cursor.execute("COMANDO SQL")

5️⃣ Guardar cambios:
   conexion.commit()

6️⃣ Obtener resultados:
   resultados = cursor.fetchall()

7️⃣ Cerrar conexión:
   conexion.close()

🎯 Siguiente paso: 02_crear_tablas.py
""")

print("✅ ¡Felicidades! Has completado el Paso 1")
print("=" * 60)
