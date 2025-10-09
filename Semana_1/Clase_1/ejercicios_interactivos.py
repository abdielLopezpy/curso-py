#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ejercicios Interactivos de Programación Básica en Python
Curso de Desarrollo Backend con Python

Este archivo contiene ejercicios interactivos para que los estudiantes practiquen
los conceptos básicos de Python como variables, tipos de datos, operaciones y estructuras.
"""

def mostrar_separador(titulo):
    """Muestra un separador visual con el título del ejercicio"""
    print("\n" + "*" * 60)
    print(f"{titulo.center(60)}")
    print("*" * 60 + "\n")

def ejercicio_variables():
    """Ejercicio para practicar variables y tipos de datos básicos"""
    mostrar_separador("EJERCICIO 1: VARIABLES Y TIPOS DE DATOS")
    
    print("En Python, las variables se crean asignando un valor:")
    print("  nombre = 'Juan'  # crea una variable de tipo string")
    print("  edad = 25        # crea una variable de tipo entero\n")
    
    print("📝 TAREA: Crea las siguientes variables:")
    print("1. 'ciudad' con el nombre de tu ciudad")
    print("2. 'año_nacimiento' con tu año de nacimiento")
    print("3. 'es_estudiante' con un valor booleano (True/False)")
    print("4. 'altura' con un valor decimal\n")
    
    # Espacio para que el estudiante escriba su código
    print("--- Escribe tu código aquí abajo ---")
    ciudad = "Madrid"
    año_nacimiento = 2000
    es_estudiante = True
    altura = 1.75
    
    
    print("\n--- Para verificar, descomenta las siguientes líneas: ---")
    print(f"Ciudad: {ciudad} (tipo: {type(ciudad)})")
    print(f"Año de nacimiento: {año_nacimiento} (tipo: {type(año_nacimiento)})")
    print(f"¿Es estudiante?: {es_estudiante} (tipo: {type(es_estudiante)})")
    print(f"Altura: {altura} (tipo: {type(altura)})")

def ejercicio_operaciones():
    """Ejercicio para practicar operaciones básicas"""
    mostrar_separador("EJERCICIO 2: OPERACIONES BÁSICAS")
    
    print("Python puede realizar diferentes operaciones matemáticas:")
    print("  suma = 5 + 3         # 8")
    print("  resta = 10 - 4       # 6")
    print("  multiplicacion = 3 * 4  # 12")
    print("  division = 8 / 2     # 4.0\n")
    
    # Valores para practicar
    x = 10
    y = 3
    
    print(f"📝 TAREA: Realiza operaciones con x = {x} e y = {y}:")
    print("1. Calcula la suma y guárdala en 'suma'")
    print("2. Calcula la resta y guárdala en 'resta'")
    print("3. Calcula la multiplicación y guárdala en 'producto'")
    print("4. Calcula la división y guárdala en 'division'")
    print("5. Calcula el módulo (resto de la división) y guárdalo en 'resto'")
    print("6. Calcula x elevado a y y guárdalo en 'potencia'\n")
    
    # Espacio para que el estudiante escriba su código
    print("--- Escribe tu código aquí abajo ---")
    suma = x + y
    resta = x - y
    producto = x * y
    division = x / y
    resto = x % y
    potencia = x ** y
    
    print("\n--- Para verificar, descomenta las siguientes líneas: ---")
    print(f"Suma: {suma}")
    print(f"Resta: {resta}")
    print(f"Producto: {producto}")
    print(f"División: {division}")
    print(f"Resto: {resto}")
    print(f"Potencia: {potencia}")

def ejercicio_strings():
    """Ejercicio para practicar operaciones con strings"""
    mostrar_separador("EJERCICIO 3: TRABAJANDO CON STRINGS")
    
    print("Los strings (cadenas de texto) tienen operaciones especiales:")
    print("  nombre = 'Ana'")
    print("  apellido = 'García'")
    print("  nombre_completo = nombre + ' ' + apellido  # 'Ana García'")
    print("  mayusculas = nombre.upper()  # 'ANA'\n")
    
    # Strings para practicar
    lenguaje = "Python"
    frase = "es un lenguaje de programación"
    
    print(f"📝 TAREA: Trabaja con los strings: '{lenguaje}' y '{frase}':")
    print("1. Une los strings con un espacio en medio y guárdalos en 'mensaje'")
    print("2. Convierte 'mensaje' a mayúsculas y guárdalo en 'mensaje_mayusculas'")
    print("3. Convierte 'mensaje' a minúsculas y guárdalo en 'mensaje_minusculas'")
    print("4. Reemplaza 'programación' por 'desarrollo' en 'mensaje' y guárdalo en 'nuevo_mensaje'")
    print("5. Cuenta cuántas veces aparece la letra 'a' en 'mensaje' y guárdalo en 'contador_a'\n")
    
    # Espacio para que el estudiante escriba su código
    print("--- Escribe tu código aquí abajo ---")
    mensaje = lenguaje + " " + frase
    mensaje_mayusculas = mensaje.upper()
    mensaje_minusculas = mensaje.lower()
    nuevo_mensaje = mensaje.replace("programación", "desarrollo")
    contador_a = mensaje.count("a")
    
    print("\n--- Para verificar, descomenta las siguientes líneas: ---")
    print(f"Mensaje: {mensaje}")
    print(f"En mayúsculas: {mensaje_mayusculas}")
    print(f"En minúsculas: {mensaje_minusculas}")
    print(f"Nuevo mensaje: {nuevo_mensaje}")
    print(f"Contador de 'a': {contador_a}")

def ejercicio_listas():
    """Ejercicio para practicar con listas"""
    mostrar_separador("EJERCICIO 4: TRABAJANDO CON LISTAS")
    
    print("Las listas son colecciones ordenadas y modificables:")
    print("  numeros = [1, 2, 3, 4, 5]")
    print("  numeros.append(6)     # Añade un elemento: [1, 2, 3, 4, 5, 6]")
    print("  primer_elemento = numeros[0]  # Accede al primer elemento: 1\n")
    
    # Lista para practicar
    colores = ["rojo", "verde", "azul", "amarillo"]
    
    print(f"📝 TAREA: Trabaja con la lista de colores: {colores}")
    print("1. Añade 'morado' al final de la lista")
    print("2. Inserta 'naranja' en la posición 2")
    print("3. Elimina 'verde' de la lista")
    print("4. Ordena la lista alfabéticamente")
    print("5. Invierte el orden de la lista")
    print("6. Crea una sublista 'colores_primarios' con los primeros 3 elementos\n")
    
    # Espacio para que el estudiante escriba su código
    print("--- Escribe tu código aquí abajo ---")
    # colores.append("morado")
    # colores.insert(2, "naranja")
    # colores.remove("verde")
    # colores.sort()
    # colores.reverse()
    # colores_primarios = colores[:3]
    
    print("\n--- Para verificar, descomenta las siguientes líneas: ---")
    # print(f"Lista modificada: {colores}")
    # print(f"Colores primarios: {colores_primarios}")

def ejercicio_diccionarios():
    """Ejercicio para practicar con diccionarios"""
    mostrar_separador("EJERCICIO 5: TRABAJANDO CON DICCIONARIOS")
    
    print("Los diccionarios almacenan pares clave-valor:")
    print("  persona = {'nombre': 'Luis', 'edad': 30}")
    print("  persona['ciudad'] = 'Madrid'  # Añade un nuevo par clave-valor")
    print("  edad = persona['edad']       # Accede al valor: 30\n")
    
    # Diccionario para practicar
    producto = {
        "nombre": "Laptop",
        "precio": 1200,
        "marca": "TechBrand"
    }
    
    print(f"📝 TAREA: Trabaja con el diccionario: {producto}")
    print("1. Añade la clave 'disponible' con el valor True")
    print("2. Modifica el precio a 1100")
    print("3. Añade una clave 'características' con una lista de 3 características")
    print("4. Elimina la clave 'marca'")
    print("5. Verifica si la clave 'color' existe y guarda el resultado en 'existe_color'\n")
    
    # Espacio para que el estudiante escriba su código
    print("--- Escribe tu código aquí abajo ---")
    # producto["disponible"] = True
    # producto["precio"] = 1100
    # producto["características"] = ["Procesador i7", "16GB RAM", "SSD 512GB"]
    # del producto["marca"]
    # existe_color = "color" in producto
    
    print("\n--- Para verificar, descomenta las siguientes líneas: ---")
    # print(f"Producto actualizado: {producto}")
    # print(f"¿Existe 'color'?: {existe_color}")

def menu_principal():
    """Muestra el menú principal de ejercicios"""
    while True:
        mostrar_separador("MENU DE EJERCICIOS INTERACTIVOS DE PYTHON")

        print("1. Variables y Tipos de Datos")
        print("2. Operaciones Básicas")
        print("3. Trabajando con Strings")
        print("4. Trabajando con Listas")
        print("5. Trabajando con Diccionarios")
        print("0. Salir")
        
        opcion = input("\nSelecciona un ejercicio (0-5): ")
        
        if opcion == "1":
            ejercicio_variables()
        elif opcion == "2":
            ejercicio_operaciones()
        elif opcion == "3":
            ejercicio_strings()
        elif opcion == "4":
            ejercicio_listas()
        elif opcion == "5":
            ejercicio_diccionarios()
        elif opcion == "0":
            print("\n¡Gracias por practicar Python! ¡Hasta la próxima!")
            break
        else:
            print("\nOpción no válida. Por favor, intenta de nuevo.")
        
        input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    print("¡Bienvenido a los Ejercicios Interactivos de Python!")
    print("Estos ejercicios te ayudarán a practicar los conceptos básicos de Python.")
    print("En cada ejercicio, lee las instrucciones y completa el código solicitado.")
    print("Para verificar tus resultados, descomenta las líneas de verificación.")
    input("\nPresiona Enter para comenzar...")
    
    menu_principal()
