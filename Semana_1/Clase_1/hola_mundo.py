#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Primer script Python del curso de Desarrollo Backend con Python, Django y PostgreSQL.
Este es un ejemplo simple que muestra la sintaxis básica de Python.
"""

# Función básica en Python
def saludar(nombre):
    """Retorna un mensaje de saludo personalizado."""
    return f"¡Hola, {nombre}! Bienvenido al curso de desarrollo backend."

# Función principal de ejecución
def main():
    """Función principal del programa."""
    print("Bienvenido al curso de Desarrollo Backend con Python, Django y PostgreSQL")
    
    # Solicitar entrada al usuario
    nombre = input("Por favor, introduce tu nombre: ")
    
    # Llamar a la función de saludo
    mensaje = saludar(nombre)
    print(mensaje)
    
    # Mostrar información sobre Python
    print("\nInformación sobre Python:")
    print("1. Python es un lenguaje interpretado de alto nivel")
    print("2. Es ideal para desarrollo backend debido a su simplicidad y potencia")
    print("3. Tiene un gran ecosistema de bibliotecas y frameworks")
    
    # Ejemplos de variables y tipos de datos
    entero = 10
    flotante = 3.14
    cadena = "Python"
    booleano = True
    lista = [1, 2, 3, 4, 5]
    diccionario = {"nombre": "Python", "tipo": "lenguaje", "año": 1991}
    
    # Mostrar tipos de datos
    print("\nEjemplos de tipos de datos en Python:")
    print(f"Entero: {entero}, tipo: {type(entero)}")
    print(f"Flotante: {flotante}, tipo: {type(flotante)}")
    print(f"Cadena: {cadena}, tipo: {type(cadena)}")
    print(f"Booleano: {booleano}, tipo: {type(booleano)}")
    print(f"Lista: {lista}, tipo: {type(lista)}")
    print(f"Diccionario: {diccionario}, tipo: {type(diccionario)}")
    
    print("\n¡Estás listo para comenzar a aprender desarrollo backend!")

# Punto de entrada estándar para scripts Python
if __name__ == "__main__":
    main()