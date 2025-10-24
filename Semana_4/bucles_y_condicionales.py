# ============================================================================
# PROGRAMA: Tutorial Interactivo - Bucles y Condicionales en Python
# AUTOR: Alejandro
# OBJETIVO: Enseñar a estudiantes sin experiencia cómo funcionan los bucles
#           y condicionales mediante ejemplos prácticos y auto-documentados
# FECHA: Mayo 2025
# CONTEXTO: Continuación del curso de Python (Semana 4)
# ============================================================================

import os
import time

# ============================================================================
# PARTE 1: CONDICIONALES (Tomar decisiones en el código)
# ============================================================================

print("=" * 70)
print("PARTE 1: CONDICIONALES - Tomando Decisiones")
print("=" * 70)

# ---------------------------------------------------------------------------
# CONCEPTO 1.1: Sentencia IF (Si)
# ---------------------------------------------------------------------------
print("\n📌 CONCEPTO 1.1: Sentencia IF (Si)")
print("-" * 70)
print("💡 EXPLICACIÓN: El IF es la decisión más básica.")
print("   Si la condición es verdadera, ejecuta el código dentro de ella.\n")

# Ejemplo 1: Validar edad para entrar a cine
edad_usuario = 16
edad_minima_peliroja = 13

print(f"Edad del usuario: {edad_usuario}")
print(f"Edad mínima requerida: {edad_minima_peliroja}")

if edad_usuario >= edad_minima_peliroja:
    print("✅ ¡Puedes ver la película!")

# Ejemplo 2: Sistema de buses - Verificar capacidad
print("\n--- Ejemplo 2: Sistema de buses ---")
pasajeros_actuales = 30
capacidad_bus = 50

print(f"Pasajeros actuales: {pasajeros_actuales}")
print(f"Capacidad máxima: {capacidad_bus}")

if pasajeros_actuales < capacidad_bus:
    print("✅ El bus tiene espacio disponible")

# ---------------------------------------------------------------------------
# CONCEPTO 1.2: Sentencia IF-ELSE (Si-Sino)
# ---------------------------------------------------------------------------
print("\n\n📌 CONCEPTO 1.2: Sentencia IF-ELSE (Si-Sino)")
print("-" * 70)
print("💡 EXPLICACIÓN: IF-ELSE permite elegir entre dos opciones.")
print("   Si la condición es verdadera → ejecuta IF")
print("   Si la condición es falsa → ejecuta ELSE\n")

# Ejemplo 1: Validar si alguien puede conducir
edad = 15

print(f"Edad: {edad}")

if edad >= 18:
    print("✅ Puedes conducir")
else:
    print("❌ No puedes conducir aún")

# Ejemplo 2: Sistema de buses - Estado del bus
print("\n--- Ejemplo 2: Estado del bus ---")
pasajeros = 0

print(f"Pasajeros en el bus: {pasajeros}")

if pasajeros > 0:
    print("🚌 El bus está en movimiento")
else:
    print("🚌 El bus está esperando en la parada")

# ---------------------------------------------------------------------------
# CONCEPTO 1.3: Sentencia IF-ELIF-ELSE (Si-O Si-Sino)
# ---------------------------------------------------------------------------
print("\n\n📌 CONCEPTO 1.3: Sentencia IF-ELIF-ELSE (Si-O Si-Sino)")
print("-" * 70)
print("💡 EXPLICACIÓN: Cuando hay MÚLTIPLES condiciones posibles.")
print("   Verifica cada condición en orden hasta encontrar una verdadera\n")

# Ejemplo 1: Clasificar calificación de un examen
calificacion = 85

print(f"Calificación del estudiante: {calificacion}")

if calificacion >= 90:
    print("🌟 Calificación: A (Excelente)")
elif calificacion >= 80:
    print("⭐ Calificación: B (Bueno)")
elif calificacion >= 70:
    print("✅ Calificación: C (Aceptable)")
elif calificacion >= 60:
    print("👍 Calificación: D (Pasable)")
else:
    print("❌ Calificación: F (Reprobado)")

# Ejemplo 2: Sistema de tarifas para buses (como en semana 3)
print("\n--- Ejemplo 2: Tarifas para buses según edad ---")
edad_pasajero = 65

print(f"Edad del pasajero: {edad_pasajero}")

if edad_pasajero < 5:
    tarifa = "Gratis (Bebé)"
elif edad_pasajero >= 5 and edad_pasajero < 12:
    tarifa = "$0.50 (Niño)"
elif edad_pasajero >= 12 and edad_pasajero < 18:
    tarifa = "$0.75 (Adolescente)"
elif edad_pasajero >= 18 and edad_pasajero < 65:
    tarifa = "$1.50 (Adulto)"
else:
    tarifa = "$0.75 (Adulto Mayor)"

print(f"Tarifa aplicada: {tarifa}")

# ---------------------------------------------------------------------------
# CONCEPTO 1.4: Operadores de Comparación
# ---------------------------------------------------------------------------
print("\n\n📌 CONCEPTO 1.4: Operadores de Comparación")
print("-" * 70)
print("💡 EXPLICACIÓN: Los condicionales usan operadores para comparar valores\n")

print("Tabla de operadores:")
print("  ==  : Igual a")
print("  !=  : No igual a")
print("  >   : Mayor que")
print("  <   : Menor que")
print("  >=  : Mayor o igual que")
print("  <=  : Menor o igual que\n")

velocidad = 60
limite_velocidad = 55

print(f"Velocidad del bus: {velocidad} km/h")
print(f"Límite de velocidad: {limite_velocidad} km/h")

if velocidad > limite_velocidad:
    exceso = velocidad - limite_velocidad
    print(f"⚠️ ¡Excediste el límite por {exceso} km/h!")
elif velocidad == limite_velocidad:
    print("✅ Vas exactamente al límite de velocidad")
else:
    print("✅ Vas dentro del límite de velocidad")

# ---------------------------------------------------------------------------
# CONCEPTO 1.5: Operadores Lógicos (AND, OR, NOT)
# ---------------------------------------------------------------------------
print("\n\n📌 CONCEPTO 1.5: Operadores Lógicos (AND, OR, NOT)")
print("-" * 70)
print("💡 EXPLICACIÓN: Combinan múltiples condiciones\n")
print("  and (Y)   : Ambas condiciones deben ser verdaderas")
print("  or (O)    : Al menos una condición debe ser verdadera")
print("  not (NO)  : Invierte el resultado\n")

# Ejemplo 1: Operador AND
print("--- Operador AND (Y) ---")
edad = 25
tiene_licencia = True

print(f"Edad: {edad}")
print(f"Tiene licencia: {tiene_licencia}")

if edad >= 18 and tiene_licencia:
    print("✅ Puedes conducir el bus")
else:
    print("❌ No puedes conducir el bus")

# Ejemplo 2: Operador OR
print("\n--- Operador OR (O) ---")
es_fin_de_semana = True
es_festivo = False

print(f"¿Es fin de semana? {es_fin_de_semana}")
print(f"¿Es festivo? {es_festivo}")

if es_fin_de_semana or es_festivo:
    print("🎉 ¡No hay clases hoy!")
else:
    print("📚 Hay clases hoy")

# Ejemplo 3: Operador NOT
print("\n--- Operador NOT (NO) ---")
lluvia = False

print(f"¿Hay lluvia? {lluvia}")

if not lluvia:
    print("☀️ Es un buen día para salir")
else:
    print("🌧️ Mejor quedarse adentro")

# ============================================================================
# PARTE 2: BUCLES (Repetir acciones)
# ============================================================================

print("\n\n" + "=" * 70)
print("PARTE 2: BUCLES - Repetir Acciones")
print("=" * 70)

# ---------------------------------------------------------------------------
# CONCEPTO 2.1: Bucle WHILE (Mientras)
# ---------------------------------------------------------------------------
print("\n📌 CONCEPTO 2.1: Bucle WHILE (Mientras)")
print("-" * 70)
print("💡 EXPLICACIÓN: Repite un bloque de código MIENTRAS una condición sea verdadera\n")

# Ejemplo 1: Contar hasta 5
print("--- Ejemplo 1: Contar hasta 5 ---")
print("Código:")
print("""
contador = 1
while contador <= 5:
    print(f"Número: {contador}")
    contador = contador + 1
""")
print("Salida:")

contador = 1
while contador <= 5:
    print(f"  Número: {contador}")
    contador = contador + 1

# Ejemplo 2: Pasajeros subiendo al bus
print("\n--- Ejemplo 2: Pasajeros subiendo al bus ---")
pasajeros_en_bus = 0
capacidad_bus = 3

print(f"Capacidad del bus: {capacidad_bus}")
print("Proceso:")

while pasajeros_en_bus < capacidad_bus:
    pasajeros_en_bus = pasajeros_en_bus + 1
    print(f"  ✅ Pasajero {pasajeros_en_bus} subió al bus ({pasajeros_en_bus}/{capacidad_bus})")

print("🚌 Bus lleno, cerrando puertas")

# Ejemplo 3: Validar entrada del usuario
print("\n--- Ejemplo 3: Sistema de acceso con contraseña ---")
print("Código:")
print("""
intentos = 0
while intentos < 3:
    contraseña = input("Ingresa la contraseña: ")
    if contraseña == "1234":
        print("✅ Acceso correcto")
        break
    else:
        intentos = intentos + 1
        print(f"❌ Contraseña incorrecta. Intentos restantes: {3 - intentos}")
""")
print("(Ejemplo simulado, sin entrada interactiva)")

# ---------------------------------------------------------------------------
# CONCEPTO 2.2: Bucle FOR (Para)
# ---------------------------------------------------------------------------
print("\n\n📌 CONCEPTO 2.2: Bucle FOR (Para)")
print("-" * 70)
print("💡 EXPLICACIÓN: Repite un bloque de código para CADA elemento en una colección\n")

# Ejemplo 1: Usar range()
print("--- Ejemplo 1: Números del 1 al 5 usando range() ---")
print("Código:")
print("""
for numero in range(1, 6):
    print(f"Número: {numero}")
""")
print("Salida:")

for numero in range(1, 6):
    print(f"  Número: {numero}")

# Ejemplo 2: Iterar sobre una lista
print("\n--- Ejemplo 2: Iterar sobre una lista de buses ---")
buses = ["B-123", "B-456", "B-789", "B-101"]
print(f"Lista de buses: {buses}\n")
print("Código:")
print("""
for bus in buses:
    print(f"Bus: {bus}")
""")
print("Salida:")

for bus in buses:
    print(f"  🚌 Bus: {bus}")

# Ejemplo 3: Iterar sobre caracteres en una cadena
print("\n--- Ejemplo 3: Iterar sobre caracteres ---")
palabra = "BUSES"
print(f"Palabra: {palabra}\n")
print("Código:")
print("""
for letra in palabra:
    print(f"Letra: {letra}")
""")
print("Salida:")

for letra in palabra:
    print(f"  📝 Letra: {letra}")

# Ejemplo 4: Lista de pasajeros
print("\n--- Ejemplo 4: Registrar pasajeros que suben al bus ---")
pasajeros = ["Carlos", "María", "José", "Ana", "Pedro"]
print(f"Pasajeros: {pasajeros}\n")

for idx, pasajero in enumerate(pasajeros, 1):  # enumerate cuenta desde 1
    print(f"  ✅ Pasajero {idx}: {pasajero} subió al bus")

# ---------------------------------------------------------------------------
# CONCEPTO 2.3: BREAK - Salir del bucle
# ---------------------------------------------------------------------------
print("\n\n📌 CONCEPTO 2.3: BREAK - Salir del Bucle")
print("-" * 70)
print("💡 EXPLICACIÓN: Detiene el bucle inmediatamente\n")

print("--- Ejemplo: Buscar un pasajero específico ---")
pasajeros = ["Carlos", "María", "José", "Ana"]
buscando = "José"

print(f"Buscando a: {buscando}\n")

for pasajero in pasajeros:
    print(f"  🔍 Verificando: {pasajero}")
    if pasajero == buscando:
        print(f"  ✅ ¡Encontrado!")
        break  # Salimos del bucle cuando lo encontramos
    else:
        print(f"  No es él, continuamos...")

# ---------------------------------------------------------------------------
# CONCEPTO 2.4: CONTINUE - Saltar a siguiente iteración
# ---------------------------------------------------------------------------
print("\n\n📌 CONCEPTO 2.4: CONTINUE - Saltar a Siguiente Iteración")
print("-" * 70)
print("💡 EXPLICACIÓN: Salta el resto del código y va a la siguiente iteración\n")

print("--- Ejemplo: Procesar solo pasajeros VIP ---")
pasajeros = ["Carlos", "VIP-María", "José", "VIP-Ana", "Pedro"]

print(f"Pasajeros: {pasajeros}\n")

for pasajero in pasajeros:
    if not pasajero.startswith("VIP"):
        continue  # Saltamos los no-VIP
    print(f"  ✨ Tratamiento especial para: {pasajero}")

# ============================================================================
# PARTE 3: COMBINANDO CONDICIONALES Y BUCLES
# ============================================================================

print("\n\n" + "=" * 70)
print("PARTE 3: Combinando Condicionales y Bucles")
print("=" * 70)

# Ejemplo 1: Validar edades en una lista
print("\n📌 Ejemplo 1: Validar Edades")
print("-" * 70)
edades = [15, 25, 12, 30, 18, 10]

print(f"Edades: {edades}\n")

for edad in edades:
    if edad >= 18:
        print(f"  ✅ Edad {edad}: Mayor de edad")
    else:
        print(f"  ❌ Edad {edad}: Menor de edad")

# Ejemplo 2: Sistema de compra de boletos
print("\n\n📌 Ejemplo 2: Sistema de Compra de Boletos")
print("-" * 70)
dinero = 10.00
precio_boleto = 1.50
boletos_comprados = 0

print(f"Dinero disponible: ${dinero:.2f}")
print(f"Precio por boleto: ${precio_boleto:.2f}\n")

while dinero >= precio_boleto:
    dinero = dinero - precio_boleto
    boletos_comprados = boletos_comprados + 1
    print(f"  🎫 Boleto {boletos_comprados} comprado. Dinero restante: ${dinero:.2f}")

print(f"\n📊 Resumen:")
print(f"  Total de boletos comprados: {boletos_comprados}")
print(f"  Dinero restante: ${dinero:.2f}")

# Ejemplo 3: Filtrar datos
print("\n\n📌 Ejemplo 3: Filtrar Datos - Buses Disponibles")
print("-" * 70)
buses_info = [
    {"numero": "B-123", "ruta": "Ruta 1", "pasajeros": 45},
    {"numero": "B-456", "ruta": "Ruta 2", "pasajeros": 30},
    {"numero": "B-789", "ruta": "Ruta 1", "pasajeros": 50},
    {"numero": "B-101", "ruta": "Ruta 3", "pasajeros": 15},
]

print("Buses en el sistema:")
for bus in buses_info:
    print(f"  {bus['numero']} - {bus['ruta']}: {bus['pasajeros']} pasajeros")

print(f"\nBuses disponibles (menos de 40 pasajeros):")
for bus in buses_info:
    if bus["pasajeros"] < 40:
        print(f"  ✅ {bus['numero']} ({bus['ruta']}): {bus['pasajeros']}/50 pasajeros")

# Ejemplo 4: Tabla de multiplicar con condicionales
print("\n\n📌 Ejemplo 4: Tabla de Multiplicar (solo números pares)")
print("-" * 70)
numero = 5
print(f"Tabla de multiplicar del {numero} (solo multiplicadores pares):\n")

for multiplicador in range(1, 11):
    if multiplicador % 2 == 0:  # % es el operador módulo (resto)
        resultado = numero * multiplicador
        print(f"  {numero} × {multiplicador} = {resultado}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("\n\n" + "=" * 70)
print("RESUMEN - Conceptos Clave")
print("=" * 70)

resumen = """
📚 CONDICIONALES (Tomar decisiones):
   • if       : Si la condición es verdadera, ejecuta el código
   • else     : Si la condición es falsa, ejecuta este código
   • elif     : Otra condición más (Si no... pero si...)

🔁 BUCLES (Repetir código):
   • while    : Repite MIENTRAS una condición sea verdadera
   • for      : Repite PARA CADA elemento en una colección

🎮 CONTROL DE BUCLES:
   • break    : Sale del bucle inmediatamente
   • continue : Salta al siguiente elemento del bucle

⚙️ OPERADORES:
   • Comparación : ==, !=, >, <, >=, <=
   • Lógicos     : and, or, not

💡 REGLA DE ORO:
   • Usa FOR cuando conoces cuántas veces repetir
   • Usa WHILE cuando necesitas repetir hasta que algo ocurra
   • Combina condicionales y bucles para programas poderosos
"""

print(resumen)

print("=" * 70)
print("✅ FIN DEL TUTORIAL")
print("=" * 70)
print("\n🎓 Próximo paso: Prueba los ejercicios en 'quiz_semana_4.py'")
print("🚀 Proyecto: Abre 'laboratorio_nasa.py' para un desafío espectacular")