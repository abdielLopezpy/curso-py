# ============================================================================
# QUIZ SEMANA 7: ORM con SQLAlchemy
# ============================================================================
# Este quiz evalúa tu comprensión de ORM y SQLAlchemy.
# ============================================================================

import random


def limpiar_pantalla():
    """Limpia la pantalla."""
    print("\n" * 2)


def mostrar_pregunta(numero, pregunta, opciones):
    """Muestra una pregunta con sus opciones."""
    print(f"\n{'=' * 60}")
    print(f"PREGUNTA {numero}")
    print("=" * 60)
    print(f"\n{pregunta}\n")

    for letra, opcion in opciones.items():
        print(f"  {letra}) {opcion}")

    print()


def evaluar_respuesta(respuesta, correcta, explicacion):
    """Evalúa la respuesta del usuario."""
    if respuesta.upper() == correcta:
        print("✅ ¡CORRECTO!")
        print(f"   {explicacion}")
        return True
    else:
        print(f"❌ Incorrecto. La respuesta correcta es: {correcta}")
        print(f"   {explicacion}")
        return False


def ejecutar_quiz():
    """Ejecuta el quiz completo."""
    preguntas = [
        {
            "pregunta": "¿Qué significa ORM?",
            "opciones": {
                "A": "Object-Relational Mapping",
                "B": "Object-Request Model",
                "C": "Only Read Mode",
                "D": "Organized Resource Management"
            },
            "correcta": "A",
            "explicacion": "ORM = Object-Relational Mapping, mapea objetos Python a tablas de base de datos."
        },
        {
            "pregunta": "¿Cuál es la principal ventaja de usar un ORM?",
            "opciones": {
                "A": "Es más rápido que SQL puro",
                "B": "No necesitas escribir SQL manualmente",
                "C": "Solo funciona con SQLite",
                "D": "Usa menos memoria"
            },
            "correcta": "B",
            "explicacion": "El ORM genera el SQL por ti, permitiéndote trabajar con objetos Python."
        },
        {
            "pregunta": "¿Cómo se define un modelo en SQLAlchemy?",
            "opciones": {
                "A": "Con una función",
                "B": "Con un diccionario",
                "C": "Con una clase que hereda de Base",
                "D": "Con un archivo JSON"
            },
            "correcta": "C",
            "explicacion": "Los modelos son clases Python que heredan de declarative_base()."
        },
        {
            "pregunta": "¿Qué hace session.add(producto)?",
            "opciones": {
                "A": "Elimina el producto",
                "B": "Marca el producto para ser insertado en la BD",
                "C": "Actualiza el producto",
                "D": "Busca el producto"
            },
            "correcta": "B",
            "explicacion": "session.add() marca un objeto para ser insertado. session.commit() lo guarda."
        },
        {
            "pregunta": "¿Cómo se obtiene un registro por ID con ORM?",
            "opciones": {
                "A": "session.find(Producto, 1)",
                "B": "session.query(Producto, 1)",
                "C": "session.get(Producto, 1)",
                "D": "session.select(Producto, 1)"
            },
            "correcta": "C",
            "explicacion": "session.get(Modelo, id) es la forma directa de obtener un registro por su clave primaria."
        },
        {
            "pregunta": "¿Cómo se filtran productos con precio menor a 100?",
            "opciones": {
                "A": "session.query(Producto).where(precio < 100)",
                "B": "session.query(Producto).filter(Producto.precio < 100)",
                "C": "session.filter(Producto.precio < 100)",
                "D": "Producto.filter(precio < 100)"
            },
            "correcta": "B",
            "explicacion": "Se usa session.query(Modelo).filter(condicion) para filtrar resultados."
        },
        {
            "pregunta": "¿Cómo se actualiza un producto con ORM?",
            "opciones": {
                "A": "session.update(producto)",
                "B": "producto.update(campo=valor)",
                "C": "Modificar el atributo y hacer session.commit()",
                "D": "session.modify(producto)"
            },
            "correcta": "C",
            "explicacion": "Solo modificas producto.precio = 99 y llamas session.commit(). ¡Así de fácil!"
        },
        {
            "pregunta": "¿Qué hace Column(Integer, primary_key=True)?",
            "opciones": {
                "A": "Crea una columna de texto",
                "B": "Crea una clave foránea",
                "C": "Crea la clave primaria autoincremental",
                "D": "Crea un índice"
            },
            "correcta": "C",
            "explicacion": "primary_key=True define la columna como clave primaria (y autoincrement en SQLite)."
        },
        {
            "pregunta": "¿Cómo se define una relación uno-a-muchos en el lado 'uno'?",
            "opciones": {
                "A": "Column(ForeignKey('tabla.id'))",
                "B": "relationship('OtroModelo', back_populates='campo')",
                "C": "OneToMany('OtroModelo')",
                "D": "has_many('OtroModelo')"
            },
            "correcta": "B",
            "explicacion": "relationship() define la relación. En el lado 'muchos' va la ForeignKey."
        },
        {
            "pregunta": "Si tienes: producto.categoria.nombre, ¿qué tipo de relación es?",
            "opciones": {
                "A": "Uno-a-uno",
                "B": "Muchos-a-muchos",
                "C": "Muchos-a-uno (producto pertenece a categoría)",
                "D": "No es una relación"
            },
            "correcta": "C",
            "explicacion": "Un producto pertenece a una categoría (muchos productos, una categoría)."
        },
        {
            "pregunta": "¿Cómo se ordenan los productos por precio descendente?",
            "opciones": {
                "A": ".order_by(Producto.precio)",
                "B": ".order_by(desc(Producto.precio))",
                "C": ".sort_by(Producto.precio, 'desc')",
                "D": ".order(Producto.precio, reverse=True)"
            },
            "correcta": "B",
            "explicacion": "desc() de sqlalchemy indica orden descendente. Sin él, es ascendente."
        },
        {
            "pregunta": "¿Cómo se cuenta el número de productos?",
            "opciones": {
                "A": "session.query(Producto).len()",
                "B": "session.count(Producto)",
                "C": "session.query(func.count(Producto.id)).scalar()",
                "D": "len(session.query(Producto))"
            },
            "correcta": "C",
            "explicacion": "func.count() es la función de agregación. .scalar() devuelve el valor único."
        },
        {
            "pregunta": "¿Qué pasa si NO llamas session.commit()?",
            "opciones": {
                "A": "Los cambios se guardan automáticamente",
                "B": "Los cambios NO se guardan en la base de datos",
                "C": "Se genera un error",
                "D": "Los cambios se guardan pero más lento"
            },
            "correcta": "B",
            "explicacion": "Sin commit(), los cambios quedan pendientes y se pierden al cerrar la sesión."
        },
        {
            "pregunta": "¿Qué hace ForeignKey('categorias.id')?",
            "opciones": {
                "A": "Crea una tabla nueva",
                "B": "Define una clave foránea que referencia la tabla categorias",
                "C": "Crea un índice",
                "D": "Elimina la columna id"
            },
            "correcta": "B",
            "explicacion": "ForeignKey define la relación a nivel de base de datos con otra tabla."
        },
        {
            "pregunta": "¿Cuál es la ventaja de usar ORM sobre SQL manual para relaciones?",
            "opciones": {
                "A": "No hay ventaja",
                "B": "Puedes navegar relaciones como atributos (producto.categoria)",
                "C": "Es obligatorio usar ORM para relaciones",
                "D": "Las relaciones son más rápidas"
            },
            "correcta": "B",
            "explicacion": "Con ORM accedes a relaciones directamente: producto.categoria.nombre, sin JOINs."
        },
    ]

    # Mezclar preguntas
    random.shuffle(preguntas)

    print("=" * 60)
    print("QUIZ SEMANA 7: ORM CON SQLALCHEMY")
    print("=" * 60)
    print(f"\nEste quiz tiene {len(preguntas)} preguntas.")
    print("Responde con la letra de la opción correcta (A, B, C o D).")
    print("\nPresiona Enter para comenzar...")
    input()

    correctas = 0
    total = len(preguntas)

    for i, pregunta in enumerate(preguntas, 1):
        mostrar_pregunta(
            i,
            pregunta["pregunta"],
            pregunta["opciones"]
        )

        while True:
            respuesta = input("Tu respuesta: ").strip().upper()
            if respuesta in ['A', 'B', 'C', 'D']:
                break
            print("Por favor, ingresa A, B, C o D")

        if evaluar_respuesta(
            respuesta,
            pregunta["correcta"],
            pregunta["explicacion"]
        ):
            correctas += 1

        if i < total:
            input("\nPresiona Enter para continuar...")

    # Resultado final
    porcentaje = (correctas / total) * 100

    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    print(f"\nRespuestas correctas: {correctas}/{total}")
    print(f"Porcentaje: {porcentaje:.1f}%")

    if porcentaje >= 90:
        print("\n🏆 ¡EXCELENTE! Dominas el ORM perfectamente.")
    elif porcentaje >= 70:
        print("\n✅ ¡MUY BIEN! Tienes un buen entendimiento del ORM.")
    elif porcentaje >= 50:
        print("\n📚 APROBADO. Repasa los conceptos que fallaste.")
    else:
        print("\n📖 Necesitas repasar. Vuelve a estudiar los archivos de la semana.")

    print("\n" + "-" * 60)
    print("TEMAS A REPASAR:")
    print("-" * 60)
    print("""
    - 01_intro_orm.py: Conceptos básicos de ORM
    - 02_modelos_basicos.py: Definición de modelos
    - 03_crud_simple.py: Operaciones CRUD
    - 04_relaciones.py: Relaciones entre modelos
    - 05_consultas_avanzadas.py: Filtros y agregaciones
    - COMPARATIVA_SQL_VS_ORM.md: Diferencias con SQL manual
    """)


if __name__ == "__main__":
    ejecutar_quiz()
