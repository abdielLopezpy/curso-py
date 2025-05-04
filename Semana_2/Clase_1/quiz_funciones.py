#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quiz sobre funciones en Python
Curso de Desarrollo Backend con Python

Este archivo contiene un quiz interactivo para evaluar
el conocimiento sobre funciones en Python.
"""

import random
import time

def limpiar_pantalla():
    """Limpia la pantalla imprimiendo varias líneas en blanco"""
    print("\n" * 40)

def mostrar_titulo():
    """Muestra el título del quiz"""
    titulo = "QUIZ DE FUNCIONES EN PYTHON"
    print("\n" + "=" * 50)
    print(titulo.center(50))
    print("=" * 50 + "\n")

def mostrar_instrucciones():
    """Muestra las instrucciones del quiz"""
    print("INSTRUCCIONES:")
    print("- Este quiz consta de preguntas de opción múltiple sobre funciones en Python")
    print("- Selecciona la respuesta correcta escribiendo la letra correspondiente")
    print("- Al final obtendrás tu puntuación total\n")
    input("Presiona Enter para comenzar...")

def mostrar_pregunta(numero, pregunta, opciones):
    """Muestra una pregunta con sus opciones"""
    print(f"\nPregunta {numero}:")
    print(f"{pregunta}\n")
    
    for letra, opcion in opciones.items():
        print(f"{letra}) {opcion}")
    
    return input("\nTu respuesta (a, b, c o d): ").lower()

def mostrar_resultado(correctas, total):
    """Muestra el resultado final del quiz"""
    porcentaje = (correctas / total) * 100
    
    print("\n" + "=" * 50)
    print("RESULTADO FINAL".center(50))
    print("=" * 50)
    
    print(f"\nRespuestas correctas: {correctas}/{total}")
    print(f"Porcentaje: {porcentaje:.1f}%")
    
    if porcentaje >= 90:
        mensaje = "¡Excelente! Dominas el tema de funciones."
    elif porcentaje >= 70:
        mensaje = "¡Muy bien! Tienes un buen conocimiento sobre funciones."
    elif porcentaje >= 50:
        mensaje = "Bien. Repasa los conceptos en los que has fallado."
    else:
        mensaje = "Necesitas estudiar más sobre funciones. ¡No te rindas!"
    
    print(f"\n{mensaje}")
    print("\n" + "=" * 50)

def realizar_quiz():
    """Ejecuta el quiz completo"""
    limpiar_pantalla()
    mostrar_titulo()
    mostrar_instrucciones()
    
    preguntas = [
        {
            "pregunta": "¿Qué palabra clave se usa para definir una función en Python?",
            "opciones": {
                "a": "function",
                "b": "def",
                "c": "fun",
                "d": "define"
            },
            "respuesta": "b"
        },
        {
            "pregunta": "¿Cuál es el propósito principal de usar funciones en programación?",
            "opciones": {
                "a": "Hacer que el programa sea más lento",
                "b": "Aumentar la cantidad de código",
                "c": "Reutilización de código y mejor organización",
                "d": "Usar más memoria del sistema"
            },
            "respuesta": "c"
        },
        {
            "pregunta": "¿Qué hace la siguiente función?\ndef suma(a, b=5):\n    return a + b",
            "opciones": {
                "a": "Suma dos números, con b teniendo un valor por defecto de 5",
                "b": "Suma siempre a + 5",
                "c": "Es un error de sintaxis",
                "d": "Resta a - b, con b siendo 5 si no se especifica"
            },
            "respuesta": "a"
        },
        {
            "pregunta": "¿Qué devuelve la siguiente función si se llama con multiplicar(3, 4)?\ndef multiplicar(x, y):\n    resultado = x * y\n    return resultado",
            "opciones": {
                "a": "7",
                "b": "12",
                "c": "3 * 4",
                "d": "No devuelve nada"
            },
            "respuesta": "b"
        },
        {
            "pregunta": "¿Cuál de los siguientes es un ejemplo de una llamada a función correcta?",
            "opciones": {
                "a": "mi_funcion",
                "b": "mi_funcion{}",
                "c": "mi_funcion()",
                "d": "llamar mi_funcion"
            },
            "respuesta": "c"
        },
        {
            "pregunta": "¿Qué significa 'return' en una función?",
            "opciones": {
                "a": "Termina la ejecución del programa completo",
                "b": "Imprime un valor en pantalla",
                "c": "Finaliza la función y devuelve un valor",
                "d": "Regresa al inicio de la función"
            },
            "respuesta": "c"
        },
        {
            "pregunta": "¿Qué sucede si una función no tiene una declaración 'return'?",
            "opciones": {
                "a": "La función da error",
                "b": "La función devuelve None",
                "c": "La función devuelve 0",
                "d": "La función repite su ejecución"
            },
            "respuesta": "b"
        },
        {
            "pregunta": "¿Cómo se llama a los datos que se pasan a una función?",
            "opciones": {
                "a": "Variables",
                "b": "Parámetros o argumentos",
                "c": "Métodos",
                "d": "Atributos"
            },
            "respuesta": "b"
        },
        {
            "pregunta": "¿Qué es el ámbito (scope) de una variable en una función?",
            "opciones": {
                "a": "El número de caracteres permitidos en el nombre de la variable",
                "b": "La región del programa donde la variable es visible y puede ser usada",
                "c": "El tipo de datos que puede almacenar la variable",
                "d": "La cantidad de memoria que ocupa la variable"
            },
            "respuesta": "b"
        },
        {
            "pregunta": "¿Cuál es el resultado de la siguiente función con la llamada test(5)?\ndef test(n):\n    if n <= 0:\n        return 0\n    return n + test(n-1)",
            "opciones": {
                "a": "5",
                "b": "10",
                "c": "15",
                "d": "Un error por recursión infinita"
            },
            "respuesta": "c"
        }
    ]
    
    # Mezclar las preguntas
    random.shuffle(preguntas)
    
    # Limitar a 5 preguntas para no hacer el quiz muy largo
    preguntas = preguntas[:5]
    
    correctas = 0
    
    for i, pregunta_data in enumerate(preguntas, 1):
        limpiar_pantalla()
        mostrar_titulo()
        
        respuesta_usuario = mostrar_pregunta(
            i, 
            pregunta_data["pregunta"], 
            pregunta_data["opciones"]
        )
        
        if respuesta_usuario == pregunta_data["respuesta"]:
            print("\n¡Correcto! 🎉")
            correctas += 1
        else:
            letra_correcta = pregunta_data["respuesta"]
            respuesta_correcta = pregunta_data["opciones"][letra_correcta]
            print(f"\nIncorrecto. La respuesta correcta es: {letra_correcta}) {respuesta_correcta}")
        
        time.sleep(1.5)
    
    limpiar_pantalla()
    mostrar_titulo()
    mostrar_resultado(correctas, len(preguntas))

if __name__ == "__main__":
    realizar_quiz()
    input("\nPresiona Enter para finalizar...")
