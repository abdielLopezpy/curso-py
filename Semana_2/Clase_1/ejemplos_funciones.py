#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ejemplos prácticos de funciones en Python
Curso de Desarrollo Backend con Python

Este archivo contiene ejemplos de diferentes tipos de funciones
para uso de referencia y práctica.
"""

print("=" * 60)
print("EJEMPLOS PRÁCTICOS DE FUNCIONES EN PYTHON".center(60))
print("=" * 60)
print("\nEste archivo muestra diferentes tipos de funciones en Python.")
print("Puedes ejecutarlo para ver los resultados o revisarlo como referencia.")
print("\nPuedes quitar el comentario de la sección que quieras probar.")
print("-" * 60)

# Ejemplo 1: Función simple sin parámetros
print("\n1. FUNCIÓN SIMPLE SIN PARÁMETROS")
print("-" * 30)

def mostrar_fecha():
    """Muestra la fecha y hora actual"""
    import datetime
    fecha_actual = datetime.datetime.now()
    print(f"Fecha actual: {fecha_actual.strftime('%d/%m/%Y')}")
    print(f"Hora actual: {fecha_actual.strftime('%H:%M:%S')}")

print("Definición de la función:")
print("def mostrar_fecha():")
print('    """Muestra la fecha y hora actual"""')
print("    import datetime")
print("    fecha_actual = datetime.datetime.now()")
print('    print(f"Fecha actual: {fecha_actual.strftime(\'%d/%m/%Y\')}")')
print('    print(f"Hora actual: {fecha_actual.strftime(\'%H:%M:%S\')}")')

print("\nLlamada a la función:")
print("mostrar_fecha()")

print("\nResultado:")
mostrar_fecha()

# Ejemplo 2: Función con parámetros
print("\n\n2. FUNCIÓN CON PARÁMETROS")
print("-" * 30)

def calcular_precio_con_impuesto(precio_base, porcentaje_impuesto):
    """Calcula el precio final con impuesto"""
    impuesto = precio_base * (porcentaje_impuesto / 100)
    precio_final = precio_base + impuesto
    print(f"Precio base: ${precio_base}")
    print(f"Impuesto ({porcentaje_impuesto}%): ${impuesto:.2f}")
    print(f"Precio final: ${precio_final:.2f}")

print("Definición de la función:")
print("def calcular_precio_con_impuesto(precio_base, porcentaje_impuesto):")
print('    """Calcula el precio final con impuesto"""')
print("    impuesto = precio_base * (porcentaje_impuesto / 100)")
print("    precio_final = precio_base + impuesto")
print('    print(f"Precio base: ${precio_base}")')
print('    print(f"Impuesto ({porcentaje_impuesto}%): ${impuesto:.2f}")')
print('    print(f"Precio final: ${precio_final:.2f}")')

print("\nLlamada a la función:")
print("calcular_precio_con_impuesto(100, 16)")

print("\nResultado:")
calcular_precio_con_impuesto(100, 16)

# Ejemplo 3: Función que devuelve un valor
print("\n\n3. FUNCIÓN QUE DEVUELVE UN VALOR")
print("-" * 30)

def calcular_area_triangulo(base, altura):
    """Calcula y devuelve el área de un triángulo"""
    area = (base * altura) / 2
    return area

print("Definición de la función:")
print("def calcular_area_triangulo(base, altura):")
print('    """Calcula y devuelve el área de un triángulo"""')
print("    area = (base * altura) / 2")
print("    return area")

print("\nLlamada a la función:")
print("area1 = calcular_area_triangulo(5, 3)")
print("area2 = calcular_area_triangulo(10, 8)")
print('print(f"Área del primer triángulo: {area1}")')
print('print(f"Área del segundo triángulo: {area2}")')
print('print(f"Suma de las áreas: {area1 + area2}")')

print("\nResultado:")
area1 = calcular_area_triangulo(5, 3)
area2 = calcular_area_triangulo(10, 8)
print(f"Área del primer triángulo: {area1}")
print(f"Área del segundo triángulo: {area2}")
print(f"Suma de las áreas: {area1 + area2}")

# Ejemplo 4: Función con parámetros por defecto
print("\n\n4. FUNCIÓN CON PARÁMETROS POR DEFECTO")
print("-" * 30)

def crear_perfil(nombre, edad, profesion="No especificada", ciudad="No especificada"):
    """Crea y muestra un perfil de usuario con valores por defecto"""
    print("Perfil de Usuario:")
    print(f"- Nombre: {nombre}")
    print(f"- Edad: {edad} años")
    print(f"- Profesión: {profesion}")
    print(f"- Ciudad: {ciudad}")

print("Definición de la función:")
print('def crear_perfil(nombre, edad, profesion="No especificada", ciudad="No especificada"):')
print('    """Crea y muestra un perfil de usuario con valores por defecto"""')
print('    print("Perfil de Usuario:")')
print('    print(f"- Nombre: {nombre}")')
print('    print(f"- Edad: {edad} años")')
print('    print(f"- Profesión: {profesion}")')
print('    print(f"- Ciudad: {ciudad}")')

print("\nLlamadas a la función:")
print('crear_perfil("Ana", 28)  # Usando valores por defecto')
print('crear_perfil("Carlos", 35, "Ingeniero")  # Especificando profesión')
print('crear_perfil("María", 41, "Doctora", "Madrid")  # Especificando todo')

print("\nResultado:")
crear_perfil("Ana", 28)  # Usando valores por defecto
print("")
crear_perfil("Carlos", 35, "Ingeniero")  # Especificando profesión
print("")
crear_perfil("María", 41, "Doctora", "Madrid")  # Especificando todo

# Ejemplo 5: Función que llama a otra función
print("\n\n5. FUNCIÓN QUE LLAMA A OTRA FUNCIÓN")
print("-" * 30)

def calcular_iva(monto, porcentaje=21):
    """Calcula el IVA de un monto"""
    return monto * (porcentaje / 100)

def calcular_total(monto, porcentaje_iva=21):
    """Calcula el total incluyendo IVA usando la función calcular_iva"""
    iva = calcular_iva(monto, porcentaje_iva)
    return monto + iva

print("Definición de las funciones:")
print("def calcular_iva(monto, porcentaje=21):")
print('    """Calcula el IVA de un monto"""')
print("    return monto * (porcentaje / 100)")
print("")
print("def calcular_total(monto, porcentaje_iva=21):")
print('    """Calcula el total incluyendo IVA usando la función calcular_iva"""')
print("    iva = calcular_iva(monto, porcentaje_iva)")
print("    return monto + iva")

print("\nLlamada a las funciones:")
print("precio = 100")
print("iva = calcular_iva(precio)")
print("total = calcular_total(precio)")
print('print(f"Precio sin IVA: ${precio}")')
print('print(f"IVA (21%): ${iva}")')
print('print(f"Precio con IVA: ${total}")')

print("\nResultado:")
precio = 100
iva = calcular_iva(precio)
total = calcular_total(precio)
print(f"Precio sin IVA: ${precio}")
print(f"IVA (21%): ${iva}")
print(f"Precio con IVA: ${total}")

# Ejemplo 6: Función con número variable de argumentos
print("\n\n6. FUNCIÓN CON NÚMERO VARIABLE DE ARGUMENTOS")
print("-" * 30)

def calcular_promedio(*numeros):
    """Calcula el promedio de un conjunto variable de números"""
    if not numeros:  # Si no se pasan argumentos
        return 0
    
    suma = sum(numeros)
    cantidad = len(numeros)
    return suma / cantidad

print("Definición de la función:")
print("def calcular_promedio(*numeros):")
print('    """Calcula el promedio de un conjunto variable de números"""')
print("    if not numeros:  # Si no se pasan argumentos")
print("        return 0")
print("    ")
print("    suma = sum(numeros)")
print("    cantidad = len(numeros)")
print("    return suma / cantidad")

print("\nLlamadas a la función:")
print("prom1 = calcular_promedio(5, 10, 15)")
print("prom2 = calcular_promedio(8, 8, 8, 8, 8)")
print("prom3 = calcular_promedio(3)")
print('print(f"Promedio 1: {prom1}")')
print('print(f"Promedio 2: {prom2}")')
print('print(f"Promedio 3: {prom3}")')

print("\nResultado:")
prom1 = calcular_promedio(5, 10, 15)
prom2 = calcular_promedio(8, 8, 8, 8, 8)
prom3 = calcular_promedio(3)
print(f"Promedio 1: {prom1}")
print(f"Promedio 2: {prom2}")
print(f"Promedio 3: {prom3}")

# Ejemplo 7: Función que trabaja con listas
print("\n\n7. FUNCIÓN QUE TRABAJA CON LISTAS")
print("-" * 30)

def contar_positivos_negativos(numeros):
    """Cuenta cuántos números positivos y negativos hay en una lista"""
    positivos = 0
    negativos = 0
    
    for numero in numeros:
        if numero > 0:
            positivos += 1
        elif numero < 0:
            negativos += 1
    
    return positivos, negativos  # Devuelve una tupla con dos valores

print("Definición de la función:")
print("def contar_positivos_negativos(numeros):")
print('    """Cuenta cuántos números positivos y negativos hay en una lista"""')
print("    positivos = 0")
print("    negativos = 0")
print("    ")
print("    for numero in numeros:")
print("        if numero > 0:")
print("            positivos += 1")
print("        elif numero < 0:")
print("            negativos += 1")
print("    ")
print("    return positivos, negativos  # Devuelve una tupla con dos valores")

print("\nLlamada a la función:")
print("lista_numeros = [5, -3, 10, -8, 0, 7, -2, 1]")
print("pos, neg = contar_positivos_negativos(lista_numeros)")
print('print(f"Lista: {lista_numeros}")')
print('print(f"Números positivos: {pos}")')
print('print(f"Números negativos: {neg}")')

print("\nResultado:")
lista_numeros = [5, -3, 10, -8, 0, 7, -2, 1]
pos, neg = contar_positivos_negativos(lista_numeros)
print(f"Lista: {lista_numeros}")
print(f"Números positivos: {pos}")
print(f"Números negativos: {neg}")

print("\n" + "=" * 60)
print("FIN DE LOS EJEMPLOS".center(60))
print("=" * 60)
print("\nPuedes usar estos ejemplos como referencia para crear tus propias funciones.")
print("Recuerda que la práctica es clave para dominar las funciones en Python.")
