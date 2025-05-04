#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ejercicios prácticos sobre funciones en Python
Curso de Desarrollo Backend con Python

Este archivo contiene ejercicios interactivos para que los estudiantes 
practiquen la creación y uso de funciones en Python.
"""

def mostrar_titulo(texto):
    """Muestra un título formateado para los ejercicios"""
    longitud = len(texto)
    print("\n" + "=" * longitud)
    print(texto)
    print("=" * longitud + "\n")

def mostrar_subtitulo(texto):
    """Muestra un subtítulo formateado"""
    print("\n" + "-" * 40)
    print(texto)
    print("-" * 40)

def esperar_entrada():
    """Espera a que el usuario presione Enter para continuar"""
    input("\nPresiona Enter para continuar...")

# Ejercicio 1: Funciones simples
def ejercicio_funciones_simples():
    mostrar_titulo("EJERCICIO 1: FUNCIONES SIMPLES")
    
    print("Una función es un bloque de código reutilizable.")
    print("Veamos un ejemplo de una función simple:")
    
    # Ejemplo de función
    print("\nDefinición de la función:")
    print("def saludar():")
    print('    print("¡Hola! Bienvenido al curso de Python")')
    
    # Ejecutar el ejemplo
    print("\nResultado al llamar a la función:")
    def saludar():
        print("¡Hola! Bienvenido al curso de Python")
    
    saludar()
    
    # Parte práctica
    mostrar_subtitulo("AHORA TE TOCA A TI")
    
    print("1. Crea una función llamada 'mostrar_mensaje' que imprima:")
    print('   "Estoy aprendiendo a crear funciones en Python"')
    print("\nEscribe tu código debajo (o pulsa Enter para ver la solución):")
    
    # Espacio para que el usuario escriba su código
    respuesta = input()
    
    # Mostrar solución si no hay respuesta
    if not respuesta.strip():
        print("\nSolución:")
        print("def mostrar_mensaje():")
        print('    print("Estoy aprendiendo a crear funciones en Python")')
        print("\nLlamada a la función:")
        print("mostrar_mensaje()")
        
        # Ejecutar la solución
        def mostrar_mensaje():
            print("Estoy aprendiendo a crear funciones en Python")
        
        print("\nResultado:")
        mostrar_mensaje()
    
    esperar_entrada()

# Ejercicio 2: Funciones con parámetros
def ejercicio_funciones_parametros():
    mostrar_titulo("EJERCICIO 2: FUNCIONES CON PARÁMETROS")
    
    print("Las funciones pueden recibir datos mediante parámetros.")
    print("Veamos un ejemplo:")
    
    # Ejemplo de función con parámetros
    print("\nDefinición de la función:")
    print("def saludar_persona(nombre):")
    print('    print(f"¡Hola {nombre}! Bienvenido al curso")')
    
    # Ejecutar el ejemplo
    print("\nResultado al llamar a la función:")
    def saludar_persona(nombre):
        print(f"¡Hola {nombre}! Bienvenido al curso")
    
    saludar_persona("Juan")
    saludar_persona("María")
    
    # Parte práctica
    mostrar_subtitulo("AHORA TE TOCA A TI")
    
    print("1. Crea una función llamada 'sumar' que reciba dos números")
    print("   y muestre su suma en la pantalla.")
    print("\nEjemplo: sumar(5, 3) debe mostrar: La suma es: 8")
    print("\nEscribe tu código debajo (o pulsa Enter para ver la solución):")
    
    # Espacio para que el usuario escriba su código
    respuesta = input()
    
    # Mostrar solución si no hay respuesta
    if not respuesta.strip():
        print("\nSolución:")
        print("def sumar(a, b):")
        print("    resultado = a + b")
        print('    print(f"La suma es: {resultado}")')
        print("\nLlamada a la función:")
        print("sumar(5, 3)")
        print("sumar(10, 20)")
        
        # Ejecutar la solución
        def sumar(a, b):
            resultado = a + b
            print(f"La suma es: {resultado}")
        
        print("\nResultado:")
        sumar(5, 3)
        sumar(10, 20)
    
    esperar_entrada()

# Ejercicio 3: Funciones que devuelven valores
def ejercicio_funciones_return():
    mostrar_titulo("EJERCICIO 3: FUNCIONES QUE DEVUELVEN VALORES")
    
    print("Las funciones pueden devolver resultados con 'return'.")
    print("Veamos un ejemplo:")
    
    # Ejemplo de función con return
    print("\nDefinición de la función:")
    print("def multiplicar(a, b):")
    print("    resultado = a * b")
    print("    return resultado")
    
    # Ejecutar el ejemplo
    print("\nForma de usar la función:")
    print('producto = multiplicar(4, 5)')
    print('print(f"El resultado de multiplicar 4 x 5 es: {producto}")')
    
    def multiplicar(a, b):
        resultado = a * b
        return resultado
    
    producto = multiplicar(4, 5)
    print(f"\nResultado: El resultado de multiplicar 4 x 5 es: {producto}")
    
    # Parte práctica
    mostrar_subtitulo("AHORA TE TOCA A TI")
    
    print("1. Crea una función llamada 'es_par' que reciba un número")
    print("   y devuelva True si es par o False si es impar.")
    print("\nEjemplo: es_par(4) debe devolver: True")
    print("Ejemplo: es_par(7) debe devolver: False")
    print("\nEscribe tu código debajo (o pulsa Enter para ver la solución):")
    
    # Espacio para que el usuario escriba su código
    respuesta = input()
    
    # Mostrar solución si no hay respuesta
    if not respuesta.strip():
        print("\nSolución:")
        print("def es_par(numero):")
        print("    if numero % 2 == 0:")
        print("        return True")
        print("    else:")
        print("        return False")
        print("\n# Una forma más corta sería:")
        print("# def es_par(numero):")
        print("#     return numero % 2 == 0")
        print("\nLlamada a la función:")
        print("resultado1 = es_par(4)")
        print("resultado2 = es_par(7)")
        print('print(f"¿4 es par? {resultado1}")')
        print('print(f"¿7 es par? {resultado2}")')
        
        # Ejecutar la solución
        def es_par(numero):
            return numero % 2 == 0
        
        resultado1 = es_par(4)
        resultado2 = es_par(7)
        
        print("\nResultado:")
        print(f"¿4 es par? {resultado1}")
        print(f"¿7 es par? {resultado2}")
    
    esperar_entrada()

# Ejercicio 4: Función con parámetros por defecto
def ejercicio_parametros_defecto():
    mostrar_titulo("EJERCICIO 4: PARÁMETROS POR DEFECTO")
    
    print("Las funciones pueden tener parámetros con valores predeterminados.")
    print("Veamos un ejemplo:")
    
    # Ejemplo de función con parámetros por defecto
    print("\nDefinición de la función:")
    print("def saludar(nombre, mensaje='Bienvenido al curso'):")
    print('    print(f"Hola {nombre}, {mensaje}")')
    
    # Ejecutar el ejemplo
    print("\nForma de usar la función:")
    print('saludar("Ana")  # Usará el mensaje por defecto')
    print('saludar("Pedro", "gracias por participar")  # Cambia el mensaje por defecto')
    
    def saludar(nombre, mensaje="Bienvenido al curso"):
        print(f"Hola {nombre}, {mensaje}")
    
    print("\nResultado:")
    saludar("Ana")
    saludar("Pedro", "gracias por participar")
    
    # Parte práctica
    mostrar_subtitulo("AHORA TE TOCA A TI")
    
    print("1. Crea una función llamada 'calcular_potencia' que reciba una base y")
    print("   un exponente (que tenga 2 como valor por defecto).")
    print("   La función debe devolver la base elevada al exponente.")
    print("\nEjemplo: calcular_potencia(5) debe devolver: 25 (5 al cuadrado)")
    print("Ejemplo: calcular_potencia(2, 3) debe devolver: 8 (2 al cubo)")
    print("\nEscribe tu código debajo (o pulsa Enter para ver la solución):")
    
    # Espacio para que el usuario escriba su código
    respuesta = input()
    
    # Mostrar solución si no hay respuesta
    if not respuesta.strip():
        print("\nSolución:")
        print("def calcular_potencia(base, exponente=2):")
        print("    return base ** exponente")
        print("\nLlamada a la función:")
        print("resultado1 = calcular_potencia(5)")
        print("resultado2 = calcular_potencia(2, 3)")
        print('print(f"5 al cuadrado es: {resultado1}")')
        print('print(f"2 al cubo es: {resultado2}")')
        
        # Ejecutar la solución
        def calcular_potencia(base, exponente=2):
            return base ** exponente
        
        resultado1 = calcular_potencia(5)
        resultado2 = calcular_potencia(2, 3)
        
        print("\nResultado:")
        print(f"5 al cuadrado es: {resultado1}")
        print(f"2 al cubo es: {resultado2}")
    
    esperar_entrada()

# Ejercicio 5: Proyecto práctico: Calculadora simple
def ejercicio_proyecto_calculadora():
    mostrar_titulo("EJERCICIO 5: PROYECTO PRÁCTICO - CALCULADORA SIMPLE")
    
    print("Ahora crearemos una calculadora simple usando funciones.")
    print("Primero, veamos cómo podríamos estructurarla:")
    
    mostrar_subtitulo("DISEÑO DE LA CALCULADORA")
    
    print("1. Función para sumar dos números")
    print("2. Función para restar dos números")
    print("3. Función para multiplicar dos números")
    print("4. Función para dividir dos números")
    print("5. Función principal que muestre un menú y llame a las otras funciones")
    
    print("\nAquí está un ejemplo de implementación:")
    
    codigo_ejemplo = """
def sumar(a, b):
    return a + b

def restar(a, b):
    return a - b

def multiplicar(a, b):
    return a * b

def dividir(a, b):
    if b != 0:
        return a / b
    else:
        return "Error: No se puede dividir entre cero"

def calculadora():
    print("\\n===== CALCULADORA SIMPLE =====")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")
    print("5. Salir")
    
    opcion = input("\\nSelecciona una operación (1-5): ")
    
    if opcion == "5":
        print("¡Hasta pronto!")
        return
    
    num1 = float(input("Ingresa el primer número: "))
    num2 = float(input("Ingresa el segundo número: "))
    
    if opcion == "1":
        print(f"Resultado: {num1} + {num2} = {sumar(num1, num2)}")
    elif opcion == "2":
        print(f"Resultado: {num1} - {num2} = {restar(num1, num2)}")
    elif opcion == "3":
        print(f"Resultado: {num1} * {num2} = {multiplicar(num1, num2)}")
    elif opcion == "4":
        print(f"Resultado: {num1} / {num2} = {dividir(num1, num2)}")
    else:
        print("Opción no válida")
    
    calculadora()  # Volvemos a mostrar la calculadora

# Iniciar la calculadora
calculadora()
"""
    
    print(codigo_ejemplo)
    
    mostrar_subtitulo("PROBEMOS LA CALCULADORA")
    
    print("Vamos a probar una versión simplificada de la calculadora:")
    
    # Funciones de la calculadora
    def sumar(a, b):
        return a + b

    def restar(a, b):
        return a - b

    def multiplicar(a, b):
        return a * b

    def dividir(a, b):
        if b != 0:
            return a / b
        else:
            return "Error: No se puede dividir entre cero"
    
    # Versión simplificada para el ejemplo
    print("\nCalculadora de ejemplo (un solo uso):")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")
    
    try:
        opcion = input("\nSelecciona una operación (1-4): ")
        
        if opcion in ["1", "2", "3", "4"]:
            num1 = float(input("Ingresa el primer número: "))
            num2 = float(input("Ingresa el segundo número: "))
            
            if opcion == "1":
                print(f"Resultado: {num1} + {num2} = {sumar(num1, num2)}")
            elif opcion == "2":
                print(f"Resultado: {num1} - {num2} = {restar(num1, num2)}")
            elif opcion == "3":
                print(f"Resultado: {num1} * {num2} = {multiplicar(num1, num2)}")
            elif opcion == "4":
                print(f"Resultado: {num1} / {num2} = {dividir(num1, num2)}")
        else:
            print("Opción no válida")
    except ValueError:
        print("Error: Ingresa solo números")
    
    print("\nEste es un ejemplo básico de cómo puedes usar funciones para crear")
    print("una aplicación más compleja. Para practicar, intenta mejorar esta calculadora")
    print("añadiendo más operaciones o mejorando su interfaz.")
    
    esperar_entrada()

def menu_principal():
    """Muestra el menú principal de ejercicios"""
    while True:
        mostrar_titulo("EJERCICIOS PRÁCTICOS DE FUNCIONES EN PYTHON")
        
        print("Selecciona un ejercicio para practicar:")
        print("1. Funciones simples")
        print("2. Funciones con parámetros")
        print("3. Funciones que devuelven valores (return)")
        print("4. Funciones con parámetros por defecto")
        print("5. Proyecto práctico: Calculadora simple")
        print("0. Salir")
        
        opcion = input("\nSelecciona una opción (0-5): ")
        
        if opcion == "1":
            ejercicio_funciones_simples()
        elif opcion == "2":
            ejercicio_funciones_parametros()
        elif opcion == "3":
            ejercicio_funciones_return()
        elif opcion == "4":
            ejercicio_parametros_defecto()
        elif opcion == "5":
            ejercicio_proyecto_calculadora()
        elif opcion == "0":
            mostrar_titulo("¡GRACIAS POR PRACTICAR!")
            print("Recuerda que la práctica constante es la clave para dominar la programación.")
            print("¡Hasta la próxima lección!")
            break
        else:
            print("\nOpción no válida. Por favor, intenta de nuevo.")
            esperar_entrada()

if __name__ == "__main__":
    print("¡Bienvenido a los ejercicios prácticos de funciones en Python!")
    print("En esta práctica aprenderás a crear y utilizar funciones.")
    print("Las funciones son la base para escribir código organizado y reutilizable.")
    input("\nPresiona Enter para comenzar...")
    
    menu_principal()
