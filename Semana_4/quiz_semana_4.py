# ============================================================================
# PROGRAMA: Quiz Interactivo - Semana 4: Bucles y Condicionales
# AUTOR: Alejandro (Profesor)
# OBJETIVO: Evaluar y reforzar el aprendizaje sobre bucles y condicionales
#           de forma interactiva y divertida
# FECHA: Mayo 2025
# CONTEXTO: Evaluación formativa para la Semana 4 del curso de Python
# ============================================================================

import os

# Limpiar pantalla
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# Base de datos de preguntas
preguntas = [
    {
        "numero": 1,
        "tipo": "condicional",
        "pregunta": "¿Qué imprime este código?\n\nedad = 20\nif edad >= 18:\n    print('Mayor de edad')\nelse:\n    print('Menor de edad')",
        "opciones": [
            "A) Mayor de edad",
            "B) Menor de edad",
            "C) No imprime nada",
            "D) Error de sintaxis"
        ],
        "respuesta_correcta": "A",
        "explicacion": "Como edad es 20 y 20 >= 18 es verdadero, ejecuta el bloque if y imprime 'Mayor de edad'"
    },
    
    {
        "numero": 2,
        "tipo": "condicional",
        "pregunta": "¿Cuál es la salida de este código?\n\ncalificacion = 75\nif calificacion >= 90:\n    print('A')\nelif calificacion >= 80:\n    print('B')\nelif calificacion >= 70:\n    print('C')\nelse:\n    print('D')",
        "opciones": [
            "A) A",
            "B) B",
            "C) C",
            "D) D"
        ],
        "respuesta_correcta": "C",
        "explicacion": "75 no es >= 90, ni >= 80, pero SÍ es >= 70, por lo que imprime 'C'"
    },
    
    {
        "numero": 3,
        "tipo": "operadores",
        "pregunta": "¿Qué imprime este código?\n\nedad = 25\ntiene_licencia = True\nif edad >= 18 and tiene_licencia:\n    print('Puedes conducir')\nelse:\n    print('No puedes conducir')",
        "opciones": [
            "A) Puedes conducir",
            "B) No puedes conducir",
            "C) No imprime nada",
            "D) Error de sintaxis"
        ],
        "respuesta_correcta": "A",
        "explicacion": "Ambas condiciones son verdaderas (edad >= 18 es True Y tiene_licencia es True), por lo que imprime 'Puedes conducir'"
    },
    
    {
        "numero": 4,
        "tipo": "bucle_while",
        "pregunta": "¿Cuántas veces se ejecuta este bucle?\n\ncontador = 0\nwhile contador < 5:\n    print(contador)\n    contador = contador + 1",
        "opciones": [
            "A) 4 veces",
            "B) 5 veces",
            "C) 6 veces",
            "D) De forma infinita"
        ],
        "respuesta_correcta": "B",
        "explicacion": "El bucle se ejecuta con contador = 0, 1, 2, 3, 4. Total: 5 veces. Cuando contador = 5, la condición es falsa y se detiene"
    },
    
    {
        "numero": 5,
        "tipo": "bucle_while",
        "pregunta": "¿Cuál es el problema con este código?\n\ncontador = 1\nwhile contador <= 5:\n    print(contador)",
        "opciones": [
            "A) No hay problema",
            "B) Es un bucle infinito",
            "C) Falta indentación",
            "D) Sintaxis incorrecta"
        ],
        "respuesta_correcta": "B",
        "explicacion": "contador nunca se incrementa, por lo que siempre será 1 y la condición nunca será falsa. Es un bucle infinito"
    },
    
    {
        "numero": 6,
        "tipo": "bucle_for",
        "pregunta": "¿Qué imprime este código?\n\nfor numero in range(3):\n    print(numero)",
        "opciones": [
            "A) 0 1 2 3",
            "B) 1 2 3",
            "C) 0 1 2",
            "D) 3"
        ],
        "respuesta_correcta": "C",
        "explicacion": "range(3) genera los números 0, 1, 2. El 3 NO se incluye. La salida es: 0\\n1\\n2"
    },
    
    {
        "numero": 7,
        "tipo": "bucle_for",
        "pregunta": "¿Cuál es la salida de este código?\n\npalabra = 'HOLA'\nfor letra in palabra:\n    print(letra)",
        "opciones": [
            "A) HOLA",
            "B) H O L A",
            "C) H\\nO\\nL\\nA",
            "D) Error - no se puede iterar una cadena"
        ],
        "respuesta_correcta": "C",
        "explicacion": "El bucle itera sobre cada letra de la cadena. Cada print() imprime en una línea diferente: H, O, L, A"
    },
    
    {
        "numero": 8,
        "tipo": "condicionales_y_bucles",
        "pregunta": "¿Cuántas veces se imprime 'Número par'?\n\nfor numero in range(1, 6):\n    if numero % 2 == 0:\n        print('Número par')",
        "opciones": [
            "A) 0 veces",
            "B) 2 veces",
            "C) 3 veces",
            "D) 5 veces"
        ],
        "respuesta_correcta": "B",
        "explicacion": "Los números pares entre 1 y 5 son: 2 y 4. Por lo tanto, se imprime 'Número par' 2 veces"
    },
    
    {
        "numero": 9,
        "tipo": "break_continue",
        "pregunta": "¿Cuál es la salida de este código?\n\nfor numero in range(1, 6):\n    if numero == 3:\n        break\n    print(numero)",
        "opciones": [
            "A) 1 2 3 4 5",
            "B) 1 2",
            "C) 1 2 3",
            "D) 3 4 5"
        ],
        "respuesta_correcta": "B",
        "explicacion": "Cuando numero == 3, el break detiene el bucle inmediatamente sin ejecutar el print(). Solo se imprimen 1 y 2"
    },
    
    {
        "numero": 10,
        "tipo": "break_continue",
        "pregunta": "¿Cuál es la salida de este código?\n\nfor numero in range(1, 6):\n    if numero == 3:\n        continue\n    print(numero)",
        "opciones": [
            "A) 1 2 3 4 5",
            "B) 1 2 4 5",
            "C) 1 2",
            "D) 3 4 5"
        ],
        "respuesta_correcta": "B",
        "explicacion": "Cuando numero == 3, continue salta esa iteración (no imprime). Se imprimen: 1, 2, 4, 5"
    },
    
    {
        "numero": 11,
        "tipo": "operadores",
        "pregunta": "¿Qué imprime este código?\n\nes_fin_de_semana = True\nes_festivo = False\nif es_fin_de_semana or es_festivo:\n    print('No hay clases')\nelse:\n    print('Hay clases')",
        "opciones": [
            "A) No hay clases",
            "B) Hay clases",
            "C) No imprime nada",
            "D) Error de sintaxis"
        ],
        "respuesta_correcta": "A",
        "explicacion": "El operador OR solo necesita UNA condición verdadera. es_fin_de_semana es True, por lo que imprime 'No hay clases'"
    },
    
    {
        "numero": 12,
        "tipo": "operadores",
        "pregunta": "¿Qué imprime este código?\n\nlluvia = False\nif not lluvia:\n    print('Es un buen día')\nelse:\n    print('Está lloviendo')",
        "opciones": [
            "A) Es un buen día",
            "B) Está lloviendo",
            "C) No imprime nada",
            "D) Error de sintaxis"
        ],
        "respuesta_correcta": "A",
        "explicacion": "El operador NOT invierte el valor. lluvia es False, pero NOT False es True, por lo que imprime 'Es un buen día'"
    },
    
    {
        "numero": 13,
        "tipo": "bucle_for",
        "pregunta": "¿Cuál es la salida de este código?\n\nbuses = ['B-123', 'B-456', 'B-789']\nfor bus in buses:\n    print(bus)",
        "opciones": [
            "A) ['B-123', 'B-456', 'B-789']",
            "B) B-123 B-456 B-789",
            "C) B-123\\nB-456\\nB-789",
            "D) buses"
        ],
        "respuesta_correcta": "C",
        "explicacion": "El bucle itera sobre cada elemento de la lista. Cada print() imprime en una línea diferente"
    },
    
    {
        "numero": 14,
        "tipo": "condicionales_y_bucles",
        "pregunta": "¿Qué hace este código?\n\nfor numero in range(1, 11):\n    if numero % 2 == 0:\n        continue\n    print(numero)",
        "opciones": [
            "A) Imprime todos los números del 1 al 10",
            "B) Imprime solo los números pares",
            "C) Imprime solo los números impares",
            "D) No imprime nada"
        ],
        "respuesta_correcta": "C",
        "explicacion": "Si el número es par (numero % 2 == 0), se salta con continue. Solo se imprimen los impares: 1, 3, 5, 7, 9"
    },
    
    {
        "numero": 15,
        "tipo": "bucle_while",
        "pregunta": "Completa este código para que imprima números del 1 al 3:\n\ncontador = 1\nwhile contador <= ___:\n    print(contador)\n    contador = contador + 1",
        "opciones": [
            "A) 1",
            "B) 2",
            "C) 3",
            "D) 4"
        ],
        "respuesta_correcta": "C",
        "explicacion": "Para imprimir 1, 2, 3, el bucle debe ejecutarse mientras contador <= 3"
    }
]

class Quiz:
    def __init__(self):
        self.puntuacion = 0
        self.total_preguntas = len(preguntas)
        self.respuestas_usuario = []
    
    def mostrar_encabezado(self):
        limpiar_pantalla()
        print("=" * 70)
        print("🎓 QUIZ INTERACTIVO - SEMANA 4")
        print("Bucles y Condicionales en Python")
        print("=" * 70)
        print(f"\n👤 profesor: Alejandro López López")
        print(f"📚 Total de preguntas: {self.total_preguntas}")
        print(f"⏱️  Tiempo: Sin límite")
        print("\n" + "=" * 70 + "\n")
    
    def hacer_pregunta(self, pregunta):
        limpiar_pantalla()
        
        # Mostrar progreso
        num_pregunta = pregunta["numero"]
        print("=" * 70)
        print(f"Pregunta {num_pregunta} de {self.total_preguntas}")
        print(f"Puntuación actual: {self.puntuacion}/{num_pregunta - 1}")
        print("=" * 70)
        
        # Mostrar tipo de pregunta
        tipos = {
            "condicional": "❓ CONDICIONAL",
            "operadores": "🔀 OPERADORES LÓGICOS",
            "bucle_while": "🔄 BUCLE WHILE",
            "bucle_for": "➡️ BUCLE FOR",
            "break_continue": "⛔ BREAK Y CONTINUE",
            "condicionales_y_bucles": "🔀🔁 COMBINACIÓN"
        }
        print(f"\n{tipos.get(pregunta['tipo'], 'PREGUNTA')}\n")
        
        # Mostrar pregunta
        print(pregunta["pregunta"])
        print("\n" + "-" * 70)
        
        # Mostrar opciones
        for opcion in pregunta["opciones"]:
            print(f"  {opcion}")
        
        print("-" * 70 + "\n")
        
        # Obtener respuesta del usuario
        respuesta_valida = False
        while not respuesta_valida:
            respuesta = input("Tu respuesta (A/B/C/D): ").strip().upper()
            if respuesta in ["A", "B", "C", "D"]:
                respuesta_valida = True
            else:
                print("❌ Respuesta inválida. Por favor, ingresa A, B, C o D")
        
        # Verificar respuesta
        es_correcta = respuesta == pregunta["respuesta_correcta"]
        self.respuestas_usuario.append({
            "numero": num_pregunta,
            "respuesta_usuario": respuesta,
            "respuesta_correcta": pregunta["respuesta_correcta"],
            "es_correcta": es_correcta,
            "explicacion": pregunta["explicacion"]
        })
        
        if es_correcta:
            self.puntuacion += 1
            print("\n✅ ¡CORRECTO!")
        else:
            print(f"\n❌ INCORRECTO")
            print(f"   Respuesta correcta: {pregunta['respuesta_correcta']}")
        
        print(f"\n📖 Explicación: {pregunta['explicacion']}")
        
        input("\n(Presiona Enter para continuar...)")
    
    def mostrar_resultados(self):
        limpiar_pantalla()
        
        porcentaje = (self.puntuacion / self.total_preguntas) * 100
        
        print("=" * 70)
        print("🏆 RESULTADOS DEL QUIZ")
        print("=" * 70)
        print(f"\n📊 Puntuación: {self.puntuacion}/{self.total_preguntas}")
        print(f"📈 Porcentaje: {porcentaje:.1f}%")
        
        # Mostrar calificación
        if porcentaje >= 90:
            print("\n🌟 ¡EXCELENTE! Has dominado este tema")
        elif porcentaje >= 80:
            print("\n⭐ ¡MUY BIEN! Tienes una buena comprensión")
        elif porcentaje >= 70:
            print("\n✅ ¡BIEN! Necesitas practicar más")
        elif porcentaje >= 60:
            print("\n👍 ¡ACEPTABLE! Repasa los conceptos principales")
        else:
            print("\n📚 Necesitas estudiar más este tema")
        
        print("\n" + "=" * 70)
        print("Detalles por pregunta:")
        print("=" * 70 + "\n")
        
        # Mostrar detalles de cada respuesta
        for respuesta in self.respuestas_usuario:
            simbolo = "✅" if respuesta["es_correcta"] else "❌"
            print(f"{simbolo} Pregunta {respuesta['numero']}")
            print(f"   Tu respuesta: {respuesta['respuesta_usuario']}")
            if not respuesta["es_correcta"]:
                print(f"   Respuesta correcta: {respuesta['respuesta_correcta']}")
            print()
        
        print("=" * 70)
    
    def ejecutar(self):
        self.mostrar_encabezado()
        
        # Hacer todas las preguntas
        for pregunta in preguntas:
            self.hacer_pregunta(pregunta)
        
        # Mostrar resultados
        self.mostrar_resultados()
        
        # Preguntar si quiere repetir
        print("\n¿Deseas repetir el quiz? (s/n): ", end="")
        if input().strip().lower() == "s":
            self.puntuacion = 0
            self.respuestas_usuario = []
            self.ejecutar()
        else:
            limpiar_pantalla()
            print("=" * 70)
            print("Gracias por completar el quiz")
            print("=" * 70)
            print("\n💡 Recomendaciones:")
            print("   • Revisa el archivo README_SEMANA_4.md para más información")
            print("   • Ejecuta bucles_y_condicionales.py para ver ejemplos prácticos")
            print("   • Completa el laboratorio_nasa.py para aplicar lo aprendido")
            print("\n¡Buena suerte! 🚀\n")

# Función principal
def main():
    quiz = Quiz()
    quiz.ejecutar()

if __name__ == "__main__":
    main()