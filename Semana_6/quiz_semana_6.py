# ============================================================================
# QUIZ INTERACTIVO - Semana 6: SQL y SQLite
# ============================================================================
# Evalúa tu conocimiento sobre SQL y SQLite con Python
# ============================================================================

import os


def limpiar_pantalla():
    """Limpia la pantalla de la terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


# Base de datos de preguntas
preguntas = [
    {
        "numero": 1,
        "tipo": "conceptos",
        "pregunta": "¿Qué significa SQL?",
        "opciones": [
            "A) Simple Query Language",
            "B) Structured Query Language",
            "C) System Query Logic",
            "D) Standard Query Library"
        ],
        "respuesta_correcta": "B",
        "explicacion": "SQL significa Structured Query Language "
                       "(Lenguaje de Consulta Estructurado)"
    },
    {
        "numero": 2,
        "tipo": "sqlite",
        "pregunta": "¿Cuál es la ventaja principal de SQLite?",
        "opciones": [
            "A) Es más rápido que PostgreSQL",
            "B) Viene incluido en Python, no requiere instalación",
            "C) Soporta más usuarios simultáneos",
            "D) Tiene mejor interfaz gráfica"
        ],
        "respuesta_correcta": "B",
        "explicacion": "SQLite viene incluido en la librería estándar "
                       "de Python (import sqlite3)"
    },
    {
        "numero": 3,
        "tipo": "codigo",
        "pregunta": "¿Qué hace este código?\n\n"
                    "conexion = sqlite3.connect('datos.db')",
        "opciones": [
            "A) Solo abre una base de datos existente",
            "B) Solo crea una base de datos nueva",
            "C) Abre la BD si existe, o la crea si no existe",
            "D) Genera un error si la BD no existe"
        ],
        "respuesta_correcta": "C",
        "explicacion": "sqlite3.connect() abre el archivo si existe, "
                       "o lo crea vacío si no existe"
    },
    {
        "numero": 4,
        "tipo": "sql",
        "pregunta": "¿Cuál comando SQL crea una nueva tabla?",
        "opciones": [
            "A) NEW TABLE usuarios",
            "B) MAKE TABLE usuarios",
            "C) CREATE TABLE usuarios",
            "D) ADD TABLE usuarios"
        ],
        "respuesta_correcta": "C",
        "explicacion": "CREATE TABLE es el comando SQL para crear tablas"
    },
    {
        "numero": 5,
        "tipo": "sql",
        "pregunta": "¿Qué hace PRIMARY KEY AUTOINCREMENT?",
        "opciones": [
            "A) Crea una contraseña automática",
            "B) Genera un ID único que se incrementa solo",
            "C) Encripta los datos de la columna",
            "D) Ordena los registros automáticamente"
        ],
        "respuesta_correcta": "B",
        "explicacion": "AUTOINCREMENT genera IDs únicos automáticamente: "
                       "1, 2, 3, 4..."
    },
    {
        "numero": 6,
        "tipo": "sql",
        "pregunta": "¿Qué restricción impide valores repetidos?",
        "opciones": [
            "A) NOT NULL",
            "B) PRIMARY KEY (para cualquier columna)",
            "C) UNIQUE",
            "D) CHECK"
        ],
        "respuesta_correcta": "C",
        "explicacion": "UNIQUE asegura que no haya valores duplicados "
                       "en esa columna"
    },
    {
        "numero": 7,
        "tipo": "crud",
        "pregunta": "¿Qué operación CRUD representa INSERT?",
        "opciones": [
            "A) Create (Crear)",
            "B) Read (Leer)",
            "C) Update (Actualizar)",
            "D) Delete (Eliminar)"
        ],
        "respuesta_correcta": "A",
        "explicacion": "INSERT = Create. Las 4 operaciones son: "
                       "Create, Read, Update, Delete"
    },
    {
        "numero": 8,
        "tipo": "codigo",
        "pregunta": "¿Por qué usamos cursor.execute('...', (valor,)) "
                    "con ? en lugar de f-strings?",
        "opciones": [
            "A) Es más rápido",
            "B) Previene inyección SQL (más seguro)",
            "C) Ocupa menos memoria",
            "D) Es obligatorio en SQLite"
        ],
        "respuesta_correcta": "B",
        "explicacion": "Los placeholders (?) previenen ataques de "
                       "inyección SQL escapando caracteres peligrosos"
    },
    {
        "numero": 9,
        "tipo": "sql",
        "pregunta": "¿Qué hace SELECT * FROM productos WHERE precio > 50?",
        "opciones": [
            "A) Muestra solo productos con precio exacto de 50",
            "B) Muestra productos con precio mayor a 50",
            "C) Actualiza precios mayores a 50",
            "D) Elimina productos con precio > 50"
        ],
        "respuesta_correcta": "B",
        "explicacion": "SELECT consulta datos, WHERE filtra. "
                       "Muestra productos donde precio es mayor que 50"
    },
    {
        "numero": 10,
        "tipo": "sql",
        "pregunta": "¿Cuál es la diferencia entre DELETE y DROP?",
        "opciones": [
            "A) Son lo mismo",
            "B) DELETE borra registros, DROP borra la tabla completa",
            "C) DROP borra registros, DELETE borra la tabla",
            "D) DELETE es más rápido que DROP"
        ],
        "respuesta_correcta": "B",
        "explicacion": "DELETE FROM tabla borra filas. "
                       "DROP TABLE elimina la tabla entera"
    },
    {
        "numero": 11,
        "tipo": "sql",
        "pregunta": "¿Qué pasa si ejecutas UPDATE productos SET precio = 0 "
                    "SIN WHERE?",
        "opciones": [
            "A) Da error",
            "B) No hace nada",
            "C) Actualiza TODOS los productos a precio 0",
            "D) Solo actualiza el primer registro"
        ],
        "respuesta_correcta": "C",
        "explicacion": "¡PELIGRO! Sin WHERE, UPDATE afecta TODAS las filas. "
                       "Siempre usa WHERE para limitar"
    },
    {
        "numero": 12,
        "tipo": "codigo",
        "pregunta": "¿Para qué sirve conexion.commit()?",
        "opciones": [
            "A) Cierra la conexión",
            "B) Guarda los cambios en la base de datos",
            "C) Crea una nueva tabla",
            "D) Ejecuta una consulta"
        ],
        "respuesta_correcta": "B",
        "explicacion": "commit() confirma y guarda los cambios. "
                       "Sin commit(), los INSERT/UPDATE/DELETE no se guardan"
    },
    {
        "numero": 13,
        "tipo": "sql",
        "pregunta": "¿Qué hace ORDER BY nombre DESC?",
        "opciones": [
            "A) Ordena por nombre de A a Z",
            "B) Ordena por nombre de Z a A",
            "C) Agrupa por nombre",
            "D) Filtra por nombre"
        ],
        "respuesta_correcta": "B",
        "explicacion": "ORDER BY ordena resultados. "
                       "DESC = descendente (Z-A), ASC = ascendente (A-Z)"
    },
    {
        "numero": 14,
        "tipo": "sql",
        "pregunta": "¿Qué hace LIMIT 5 en una consulta SELECT?",
        "opciones": [
            "A) Filtra registros con valor 5",
            "B) Devuelve solo los primeros 5 registros",
            "C) Salta los primeros 5 registros",
            "D) Multiplica los resultados por 5"
        ],
        "respuesta_correcta": "B",
        "explicacion": "LIMIT n devuelve máximo n registros. "
                       "Útil para paginación y previews"
    },
    {
        "numero": 15,
        "tipo": "sql",
        "pregunta": "¿Qué función cuenta el número de registros?",
        "opciones": [
            "A) SUM()",
            "B) AVG()",
            "C) COUNT()",
            "D) TOTAL()"
        ],
        "respuesta_correcta": "C",
        "explicacion": "COUNT(*) cuenta registros. "
                       "SUM suma valores, AVG calcula promedio"
    },
    {
        "numero": 16,
        "tipo": "joins",
        "pregunta": "¿Qué tipo de JOIN devuelve SOLO las filas "
                    "que coinciden en ambas tablas?",
        "opciones": [
            "A) LEFT JOIN",
            "B) RIGHT JOIN",
            "C) INNER JOIN",
            "D) FULL JOIN"
        ],
        "respuesta_correcta": "C",
        "explicacion": "INNER JOIN devuelve solo filas con "
                       "coincidencias en ambas tablas"
    },
    {
        "numero": 17,
        "tipo": "joins",
        "pregunta": "¿Qué es una FOREIGN KEY (clave foránea)?",
        "opciones": [
            "A) Una contraseña para la base de datos",
            "B) Una columna que referencia la clave primaria de otra tabla",
            "C) El primer registro de una tabla",
            "D) Un tipo de dato especial"
        ],
        "respuesta_correcta": "B",
        "explicacion": "La clave foránea conecta tablas. "
                       "Ej: productos.categoria_id → categorias.id"
    },
    {
        "numero": 18,
        "tipo": "codigo",
        "pregunta": "¿Qué método obtiene UN solo registro del cursor?",
        "opciones": [
            "A) cursor.fetchall()",
            "B) cursor.fetchone()",
            "C) cursor.fetchmany()",
            "D) cursor.get()"
        ],
        "respuesta_correcta": "B",
        "explicacion": "fetchone() = 1 registro, "
                       "fetchall() = todos, fetchmany(n) = n registros"
    },
    {
        "numero": 19,
        "tipo": "sql",
        "pregunta": "¿Qué hace WHERE nombre LIKE '%ana%'?",
        "opciones": [
            "A) Busca nombres que sean exactamente 'ana'",
            "B) Busca nombres que contengan 'ana' en cualquier parte",
            "C) Busca nombres que empiecen con 'ana'",
            "D) Busca nombres que terminen con 'ana'"
        ],
        "respuesta_correcta": "B",
        "explicacion": "% es comodín para cualquier cantidad de caracteres. "
                       "%ana% = contiene 'ana'"
    },
    {
        "numero": 20,
        "tipo": "transacciones",
        "pregunta": "¿Qué hace conexion.rollback()?",
        "opciones": [
            "A) Guarda los cambios",
            "B) Cierra la conexión",
            "C) Deshace los cambios no confirmados",
            "D) Crea un backup"
        ],
        "respuesta_correcta": "C",
        "explicacion": "rollback() revierte todos los cambios "
                       "desde el último commit()"
    }
]


def mostrar_pregunta(pregunta):
    """Muestra una pregunta y retorna si fue correcta."""
    print(f"\n{'='*60}")
    print(f"📝 Pregunta {pregunta['numero']} - [{pregunta['tipo'].upper()}]")
    print("="*60)
    print(f"\n{pregunta['pregunta']}\n")

    for opcion in pregunta['opciones']:
        print(f"   {opcion}")

    while True:
        respuesta = input("\n👉 Tu respuesta (A/B/C/D): ").strip().upper()
        if respuesta in ['A', 'B', 'C', 'D']:
            break
        print("❌ Por favor ingresa A, B, C o D")

    if respuesta == pregunta['respuesta_correcta']:
        print("\n✅ ¡CORRECTO!")
        print(f"💡 {pregunta['explicacion']}")
        return True
    else:
        print(f"\n❌ Incorrecto. La respuesta correcta es: "
              f"{pregunta['respuesta_correcta']}")
        print(f"💡 {pregunta['explicacion']}")
        return False


def ejecutar_quiz():
    """Ejecuta el quiz completo."""
    limpiar_pantalla()

    print("=" * 60)
    print("🎮 QUIZ SEMANA 6: SQL y SQLite con Python")
    print("=" * 60)
    print("""
¡Bienvenido al quiz de la Semana 6!

📚 Temas evaluados:
   • Conceptos básicos de SQL
   • SQLite y conexión con Python
   • Operaciones CRUD
   • Consultas y filtros
   • Relaciones y JOINs
   • Transacciones

📝 Total de preguntas: 20
⏱️  Sin límite de tiempo

¡Buena suerte! 🍀
    """)

    input("Presiona ENTER para comenzar...")

    correctas = 0
    total = len(preguntas)

    for pregunta in preguntas:
        limpiar_pantalla()
        if mostrar_pregunta(pregunta):
            correctas += 1
        input("\nPresiona ENTER para continuar...")

    # Mostrar resultados
    limpiar_pantalla()
    porcentaje = (correctas / total) * 100

    print("\n" + "=" * 60)
    print("🏆 RESULTADOS DEL QUIZ")
    print("=" * 60)
    print(f"\n   Respuestas correctas: {correctas}/{total}")
    print(f"   Porcentaje: {porcentaje:.1f}%")

    # Calificación
    if porcentaje >= 90:
        print("\n   🌟 ¡EXCELENTE! Dominas SQL y SQLite")
        emoji = "🏆"
    elif porcentaje >= 70:
        print("\n   👍 ¡MUY BIEN! Buen dominio del tema")
        emoji = "🥈"
    elif porcentaje >= 50:
        print("\n   📚 APROBADO. Repasa algunos conceptos")
        emoji = "🥉"
    else:
        print("\n   📖 Necesitas repasar el material")
        emoji = "📚"

    print(f"\n   {emoji} Tu calificación: {porcentaje:.0f}/100")

    # Recomendaciones
    print("\n" + "-" * 60)
    print("📖 Recomendaciones:")
    if porcentaje < 70:
        print("   • Repasa los archivos 01 al 07 de la Semana 6")
        print("   • Practica con ejercicios_sqlite.py")
        print("   • Lee CONCEPTOS_SQL.md para reforzar teoría")
    if porcentaje < 90:
        print("   • Construye tu propio proyecto con SQLite")
        print("   • Experimenta con JOINs y subconsultas")
    else:
        print("   • ¡Estás listo para el siguiente nivel!")
        print("   • Considera aprender PostgreSQL o MySQL")

    print("\n" + "=" * 60)
    print("✅ ¡Gracias por completar el quiz!")
    print("=" * 60)


# Punto de entrada
if __name__ == "__main__":
    ejecutar_quiz()
