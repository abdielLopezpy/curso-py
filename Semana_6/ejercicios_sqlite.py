# ============================================================================
# EJERCICIOS PRÁCTICOS - Semana 6: SQL y SQLite
# ============================================================================
# Practica lo aprendido completando estos ejercicios.
# Cada ejercicio tiene instrucciones claras y espacio para tu código.
# ============================================================================

import sqlite3
import os

# Crear carpeta para datos si no existe
os.makedirs('datos', exist_ok=True)

print("=" * 60)
print("✏️ EJERCICIOS PRÁCTICOS - SQL y SQLite")
print("=" * 60)

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================
# Usaremos una base de datos separada para ejercicios
DB_PATH = 'datos/ejercicios.db'


def conectar():
    """Retorna una conexión a la base de datos de ejercicios."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def reset_database():
    """Reinicia la base de datos de ejercicios."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    print("🔄 Base de datos reiniciada")


# ============================================================================
# EJERCICIO 1: Crear una tabla
# ============================================================================
print("\n" + "=" * 60)
print("📝 EJERCICIO 1: Crear una tabla de estudiantes")
print("=" * 60)

print("""
INSTRUCCIONES:
Crea una tabla llamada 'estudiantes' con las siguientes columnas:
- id: entero, clave primaria, autoincrement
- nombre: texto, no nulo
- edad: entero
- email: texto, único
- promedio: real, valor por defecto 0.0

Completa el código SQL abajo:
""")


def ejercicio_1():
    """Crea la tabla de estudiantes."""
    conn = conectar()
    cursor = conn.cursor()

    # TODO: Completa el SQL para crear la tabla
    sql = """
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        edad INTEGER,
        email TEXT UNIQUE,
        promedio REAL DEFAULT 0.0
    )
    """

    cursor.execute(sql)
    conn.commit()

    # Verificar
    cursor.execute("PRAGMA table_info(estudiantes)")
    columnas = cursor.fetchall()

    print("✅ Tabla creada. Columnas:")
    for col in columnas:
        print(f"   - {col['name']} ({col['type']})")

    conn.close()


# Ejecutar ejercicio 1
ejercicio_1()


# ============================================================================
# EJERCICIO 2: Insertar registros
# ============================================================================
print("\n" + "=" * 60)
print("📝 EJERCICIO 2: Insertar estudiantes")
print("=" * 60)

print("""
INSTRUCCIONES:
Inserta los siguientes estudiantes en la tabla:
1. María López, 20 años, maria@uni.edu, promedio 8.5
2. Juan García, 22 años, juan@uni.edu, promedio 7.8
3. Ana Torres, 19 años, ana@uni.edu, promedio 9.2
4. Carlos Ruiz, 21 años, carlos@uni.edu, promedio 6.5
5. Sofia Pérez, 20 años, sofia@uni.edu, promedio 8.9

Usa executemany() para insertar todos de una vez.
""")


def ejercicio_2():
    """Inserta estudiantes en la tabla."""
    conn = conectar()
    cursor = conn.cursor()

    # TODO: Define la lista de estudiantes
    estudiantes = [
        ("María López", 20, "maria@uni.edu", 8.5),
        ("Juan García", 22, "juan@uni.edu", 7.8),
        ("Ana Torres", 19, "ana@uni.edu", 9.2),
        ("Carlos Ruiz", 21, "carlos@uni.edu", 6.5),
        ("Sofia Pérez", 20, "sofia@uni.edu", 8.9)
    ]

    # TODO: Completa el INSERT con executemany
    sql = """
    INSERT OR IGNORE INTO estudiantes (nombre, edad, email, promedio)
    VALUES (?, ?, ?, ?)
    """

    cursor.executemany(sql, estudiantes)
    conn.commit()

    # Verificar
    cursor.execute("SELECT COUNT(*) FROM estudiantes")
    total = cursor.fetchone()[0]
    print(f"✅ {total} estudiantes insertados")

    conn.close()


# Ejecutar ejercicio 2
ejercicio_2()


# ============================================================================
# EJERCICIO 3: Consultas SELECT
# ============================================================================
print("\n" + "=" * 60)
print("📝 EJERCICIO 3: Consultas SELECT")
print("=" * 60)

print("""
INSTRUCCIONES:
Realiza las siguientes consultas:
a) Todos los estudiantes ordenados por nombre
b) Estudiantes con promedio mayor a 8.0
c) El estudiante más joven
d) El promedio general de todos los estudiantes
""")


def ejercicio_3():
    """Realiza consultas SELECT."""
    conn = conectar()
    cursor = conn.cursor()

    # a) Todos ordenados por nombre
    print("\na) Estudiantes ordenados por nombre:")
    print("-" * 40)
    cursor.execute("SELECT nombre, promedio FROM estudiantes ORDER BY nombre")
    for row in cursor.fetchall():
        print(f"   {row['nombre']}: {row['promedio']}")

    # b) Promedio mayor a 8.0
    print("\nb) Estudiantes con promedio > 8.0:")
    print("-" * 40)
    cursor.execute(
        "SELECT nombre, promedio FROM estudiantes WHERE promedio > 8.0"
    )
    for row in cursor.fetchall():
        print(f"   {row['nombre']}: {row['promedio']}")

    # c) El más joven
    print("\nc) Estudiante más joven:")
    print("-" * 40)
    cursor.execute(
        "SELECT nombre, edad FROM estudiantes ORDER BY edad ASC LIMIT 1"
    )
    joven = cursor.fetchone()
    print(f"   {joven['nombre']} ({joven['edad']} años)")

    # d) Promedio general
    print("\nd) Promedio general:")
    print("-" * 40)
    cursor.execute("SELECT AVG(promedio) as promedio_general FROM estudiantes")
    resultado = cursor.fetchone()
    print(f"   Promedio de la clase: {resultado['promedio_general']:.2f}")

    conn.close()


# Ejecutar ejercicio 3
ejercicio_3()


# ============================================================================
# EJERCICIO 4: UPDATE y DELETE
# ============================================================================
print("\n" + "=" * 60)
print("📝 EJERCICIO 4: Actualizar y Eliminar")
print("=" * 60)

print("""
INSTRUCCIONES:
a) Aumenta en 0.5 el promedio de todos los estudiantes
b) Actualiza el email de Carlos Ruiz a 'cruiz@uni.edu'
c) Elimina estudiantes con promedio menor a 7.5 (después del aumento)
""")


def ejercicio_4():
    """Actualiza y elimina registros."""
    conn = conectar()
    cursor = conn.cursor()

    # a) Aumentar promedio en 0.5
    print("\na) Aumentando promedio de todos en 0.5...")
    cursor.execute("UPDATE estudiantes SET promedio = promedio + 0.5")
    conn.commit()
    print(f"   ✅ {cursor.rowcount} estudiantes actualizados")

    # b) Actualizar email de Carlos
    print("\nb) Actualizando email de Carlos Ruiz...")
    cursor.execute("""
        UPDATE estudiantes
        SET email = 'cruiz@uni.edu'
        WHERE nombre = 'Carlos Ruiz'
    """)
    conn.commit()
    print(f"   ✅ {cursor.rowcount} registro actualizado")

    # c) Eliminar estudiantes con promedio < 7.5
    print("\nc) Eliminando estudiantes con promedio < 7.5...")
    cursor.execute("DELETE FROM estudiantes WHERE promedio < 7.5")
    conn.commit()
    print(f"   ✅ {cursor.rowcount} estudiantes eliminados")

    # Verificar estado final
    print("\nEstudiantes restantes:")
    cursor.execute("SELECT nombre, promedio FROM estudiantes")
    for row in cursor.fetchall():
        print(f"   {row['nombre']}: {row['promedio']:.1f}")

    conn.close()


# Ejecutar ejercicio 4
ejercicio_4()


# ============================================================================
# EJERCICIO 5: Crear tablas relacionadas
# ============================================================================
print("\n" + "=" * 60)
print("📝 EJERCICIO 5: Tablas relacionadas (Cursos)")
print("=" * 60)

print("""
INSTRUCCIONES:
Crea una tabla 'cursos' y una tabla 'inscripciones':

CURSOS:
- id, nombre, creditos

INSCRIPCIONES (tabla intermedia):
- id
- estudiante_id (FK a estudiantes)
- curso_id (FK a cursos)
- calificacion

Luego inserta algunos cursos e inscripciones.
""")


def ejercicio_5():
    """Crea tablas relacionadas."""
    conn = conectar()
    cursor = conn.cursor()

    # Crear tabla cursos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            creditos INTEGER DEFAULT 3
        )
    """)

    # Crear tabla inscripciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inscripciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER NOT NULL,
            curso_id INTEGER NOT NULL,
            calificacion REAL,
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
        )
    """)
    conn.commit()
    print("✅ Tablas 'cursos' e 'inscripciones' creadas")

    # Insertar cursos
    cursos = [
        ("Programación Python", 4),
        ("Base de Datos", 3),
        ("Desarrollo Web", 4),
        ("Algoritmos", 3)
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO cursos (nombre, creditos) VALUES (?, ?)",
        cursos
    )
    conn.commit()
    print(f"✅ {len(cursos)} cursos insertados")

    # Obtener IDs de estudiantes y cursos
    cursor.execute("SELECT id FROM estudiantes LIMIT 3")
    estudiantes = [row['id'] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM cursos")
    cursos_ids = [row['id'] for row in cursor.fetchall()]

    # Crear inscripciones
    inscripciones = []
    for est_id in estudiantes:
        for cur_id in cursos_ids[:2]:  # Inscribir en 2 cursos
            inscripciones.append((est_id, cur_id, 8.0 + (est_id * 0.3)))

    cursor.executemany("""
        INSERT OR IGNORE INTO inscripciones
        (estudiante_id, curso_id, calificacion)
        VALUES (?, ?, ?)
    """, inscripciones)
    conn.commit()
    print(f"✅ {len(inscripciones)} inscripciones creadas")

    conn.close()


# Ejecutar ejercicio 5
ejercicio_5()


# ============================================================================
# EJERCICIO 6: JOINs
# ============================================================================
print("\n" + "=" * 60)
print("📝 EJERCICIO 6: Consultas con JOIN")
print("=" * 60)

print("""
INSTRUCCIONES:
Realiza consultas que combinen las tablas:
a) Listar estudiantes con sus cursos
b) Contar cuántos estudiantes hay en cada curso
c) Mostrar el promedio de calificaciones por curso
""")


def ejercicio_6():
    """Consultas con JOIN."""
    conn = conectar()
    cursor = conn.cursor()

    # a) Estudiantes con sus cursos
    print("\na) Estudiantes y sus cursos:")
    print("-" * 50)
    cursor.execute("""
        SELECT e.nombre as estudiante, c.nombre as curso, i.calificacion
        FROM inscripciones i
        INNER JOIN estudiantes e ON i.estudiante_id = e.id
        INNER JOIN cursos c ON i.curso_id = c.id
        ORDER BY e.nombre, c.nombre
    """)
    for row in cursor.fetchall():
        print(f"   {row['estudiante']:<15} | {row['curso']:<20} | "
              f"{row['calificacion']:.1f}")

    # b) Estudiantes por curso
    print("\nb) Cantidad de estudiantes por curso:")
    print("-" * 40)
    cursor.execute("""
        SELECT c.nombre, COUNT(i.estudiante_id) as total_estudiantes
        FROM cursos c
        LEFT JOIN inscripciones i ON c.id = i.curso_id
        GROUP BY c.id
    """)
    for row in cursor.fetchall():
        print(f"   {row['nombre']:<25} {row['total_estudiantes']} estudiantes")

    # c) Promedio por curso
    print("\nc) Promedio de calificaciones por curso:")
    print("-" * 40)
    cursor.execute("""
        SELECT c.nombre, AVG(i.calificacion) as promedio
        FROM cursos c
        INNER JOIN inscripciones i ON c.id = i.curso_id
        GROUP BY c.id
    """)
    for row in cursor.fetchall():
        prom = row['promedio'] if row['promedio'] else 0
        print(f"   {row['nombre']:<25} {prom:.2f}")

    conn.close()


# Ejecutar ejercicio 6
ejercicio_6()


# ============================================================================
# EJERCICIO 7: Desafío Final
# ============================================================================
print("\n" + "=" * 60)
print("🏆 EJERCICIO 7: DESAFÍO FINAL")
print("=" * 60)

print("""
INSTRUCCIONES:
Crea un mini sistema de biblioteca con:

1. Tabla 'libros': id, titulo, autor, año, disponible (bool)
2. Tabla 'prestamos': id, libro_id (FK), fecha_prestamo, fecha_devolucion

Implementa:
a) Agregar 5 libros
b) Registrar 2 préstamos
c) Consulta que muestre libros disponibles
d) Consulta que muestre libros prestados con fechas

¡Intenta hacerlo sin ver las soluciones anteriores!
""")


def ejercicio_7():
    """Desafío final: Sistema de biblioteca."""
    conn = conectar()
    cursor = conn.cursor()

    # 1. Crear tablas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            anio INTEGER,
            disponible INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            libro_id INTEGER NOT NULL,
            fecha_prestamo TEXT DEFAULT CURRENT_DATE,
            fecha_devolucion TEXT,
            FOREIGN KEY (libro_id) REFERENCES libros(id)
        )
    """)
    conn.commit()
    print("✅ Tablas de biblioteca creadas")

    # 2. Agregar libros
    libros = [
        ("Cien Años de Soledad", "Gabriel García Márquez", 1967),
        ("Don Quijote", "Miguel de Cervantes", 1605),
        ("1984", "George Orwell", 1949),
        ("El Principito", "Antoine de Saint-Exupéry", 1943),
        ("Crónica de una Muerte Anunciada", "Gabriel García Márquez", 1981)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO libros (titulo, autor, anio)
        VALUES (?, ?, ?)
    """, libros)
    conn.commit()
    print(f"✅ {len(libros)} libros agregados")

    # 3. Registrar préstamos
    # Marcar libros 1 y 3 como prestados
    cursor.execute("UPDATE libros SET disponible = 0 WHERE id IN (1, 3)")

    prestamos = [
        (1, "2026-01-05"),
        (3, "2026-01-07")
    ]
    cursor.executemany("""
        INSERT OR IGNORE INTO prestamos (libro_id, fecha_prestamo)
        VALUES (?, ?)
    """, prestamos)
    conn.commit()
    print("✅ 2 préstamos registrados")

    # 4. Consultar libros disponibles
    print("\n📚 Libros DISPONIBLES:")
    print("-" * 50)
    cursor.execute("""
        SELECT titulo, autor, anio
        FROM libros
        WHERE disponible = 1
    """)
    for row in cursor.fetchall():
        print(f"   📖 {row['titulo']} - {row['autor']} ({row['anio']})")

    # 5. Consultar libros prestados
    print("\n📕 Libros PRESTADOS:")
    print("-" * 50)
    cursor.execute("""
        SELECT l.titulo, l.autor, p.fecha_prestamo
        FROM libros l
        INNER JOIN prestamos p ON l.id = p.libro_id
        WHERE l.disponible = 0 AND p.fecha_devolucion IS NULL
    """)
    for row in cursor.fetchall():
        print(f"   📕 {row['titulo']} - Prestado: {row['fecha_prestamo']}")

    conn.close()
    print("\n🏆 ¡Desafío completado!")


# Ejecutar desafío
ejercicio_7()


# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "=" * 60)
print("✅ EJERCICIOS COMPLETADOS")
print("=" * 60)

print("""
Has practicado:

1️⃣ Crear tablas con restricciones
2️⃣ Insertar registros con executemany()
3️⃣ Consultas SELECT con WHERE, ORDER BY
4️⃣ UPDATE y DELETE con condiciones
5️⃣ Tablas relacionadas con FOREIGN KEY
6️⃣ Consultas con JOIN
7️⃣ Sistema completo (biblioteca)

📁 Base de datos de ejercicios: datos/ejercicios.db

💡 SUGERENCIAS PARA SEGUIR PRACTICANDO:
   • Modifica los ejercicios con tus propios datos
   • Agrega más funcionalidades al sistema de biblioteca
   • Crea tu propio proyecto (inventario, contactos, etc.)
   • Experimenta con subconsultas y funciones de agregación

¡Excelente trabajo! 🎉
""")
