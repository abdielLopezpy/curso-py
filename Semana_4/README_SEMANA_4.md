# 📚 Semana 4: Bucles y Condicionales en Python

## 🎯 Objetivo de la Semana

Aprender a controlar el flujo de un programa mediante **condicionales** (tomar decisiones) y **bucles** (repetir acciones). Estos son conceptos fundamentales que permiten que los programas reaccionen ante diferentes situaciones y realicen tareas repetitivas sin escribir código redundante.

> 💡 **Analogía del mundo real:** Los condicionales son como las decisiones que tomas en la vida ("Si llueve, llevo paraguas; si no, no lo llevo"). Los bucles son como las tareas repetitivas ("Mientras haya platos en el lavabo, lava un plato").

---

## 📖 Tabla de Contenidos

1. [Condicionales](#condicionales)
2. [Bucles](#bucles)
3. [Combinación de Condicionales y Bucles](#combinación)
4. [Mejores Prácticas](#mejores-prácticas)
5. [Ejercicios](#ejercicios)

---

## 🔀 CONDICIONALES

### ¿Qué son los Condicionales?

Los **condicionales** son estructuras que permiten que el programa tome **decisiones** basadas en condiciones. Si una condición es verdadera, ejecuta un bloque de código; si es falsa, puede ejecutar otro bloque.

**Analogía:** Es como un semáforo. Si la luz es roja, esperas. Si es verde, cruzas.

---

### Sentencia `if` (Si)

La forma más básica de condicional. Se ejecuta solo si la condición es verdadera.

```python
# Sintaxis básica
if condición:
    # Este código se ejecuta si la condición es verdadera
    print("La condición se cumplió")
```

#### Ejemplo 1: Verificar si un número es positivo

```python
edad = 25

if edad >= 18:
    print("Eres mayor de edad")
```

**Salida:** `Eres mayor de edad`

#### Ejemplo 2: En un sistema de transporte (como en semana 3)

```python
# Simulador de buses - Verificar si hay espacio
pasajeros_actuales = 45
capacidad_maxima = 50

if pasajeros_actuales < capacidad_maxima:
    print("✅ El bus tiene espacio disponible")
```

**Salida:** `✅ El bus tiene espacio disponible`

---

### Sentencia `if-else` (Si-Sino)

Cuando queremos ejecutar código diferente según si la condición es verdadera o falsa.

```python
# Sintaxis
if condición:
    # Se ejecuta si es verdadero
else:
    # Se ejecuta si es falso
```

#### Ejemplo 1: Validar acceso a una película

```python
edad_usuario = 15
edad_minima = 13

if edad_usuario >= edad_minima:
    print("✅ Puedes ver esta película")
else:
    print("❌ No puedes ver esta película, eres muy joven")
```

**Salida:** `✅ Puedes ver esta película`

#### Ejemplo 2: Estado de un bus (como en semana 3)

```python
pasajeros = 0

if pasajeros > 0:
    print("🚌 El bus está en movimiento")
else:
    print("🚌 El bus está esperando en la parada")
```

**Salida:** `🚌 El bus está esperando en la parada`

---

### Sentencia `if-elif-else` (Si-O Si-Sino)

Cuando hay múltiples condiciones posibles.

```python
# Sintaxis
if condición1:
    # Se ejecuta si condición1 es verdadera
elif condición2:
    # Se ejecuta si condición1 es falsa pero condición2 es verdadera
elif condición3:
    # Se ejecuta si condición1 y condición2 son falsas pero condición3 es verdadera
else:
    # Se ejecuta si todas las anteriores son falsas
```

#### Ejemplo: Clasificar calificaciones

```python
calificacion = 85

if calificacion >= 90:
    print("A - Excelente")
elif calificacion >= 80:
    print("B - Bueno")
elif calificacion >= 70:
    print("C - Aceptable")
elif calificacion >= 60:
    print("D - Pasable")
else:
    print("F - Reprobado")
```

**Salida:** `B - Bueno`

#### Ejemplo: Sistema de tarifas para buses

```python
edad = 65

if edad < 5:
    tarifa = "Gratis"
elif edad >= 5 and edad < 18:
    tarifa = "Tarifa infantil: $0.50"
elif edad >= 18 and edad < 65:
    tarifa = "Tarifa adulto: $1.00"
else:
    tarifa = "Tarifa adulto mayor: $0.50"

print(f"Tu tarifa es: {tarifa}")
```

**Salida:** `Tu tarifa es: Tarifa adulto mayor: $0.50`

---

### Operadores de Comparación

Los condicionales usan **operadores de comparación** para evaluar condiciones:

| Operador | Significado | Ejemplo | Resultado |
|----------|-------------|---------|-----------|
| `==` | Igual a | `5 == 5` | `True` |
| `!=` | No igual a | `5 != 3` | `True` |
| `>` | Mayor que | `5 > 3` | `True` |
| `<` | Menor que | `5 < 10` | `True` |
| `>=` | Mayor o igual que | `5 >= 5` | `True` |
| `<=` | Menor o igual que | `5 <= 10` | `True` |

#### Ejemplos prácticos

```python
# Comparación numérica
velocidad = 60
limite = 55

if velocidad > limite:
    print("Excediste el límite de velocidad")

# Comparación de cadenas
nombre = "José"

if nombre == "José":
    print(f"¡Hola, {nombre}!")

# Comparación con booleanos
es_mayor_de_edad = True

if es_mayor_de_edad:
    print("Puedes conducir")
```

---

### Operadores Lógicos

Para combinar múltiples condiciones:

| Operador | Significado | Ejemplo |
|----------|-------------|---------|
| `and` | Y (ambas deben ser verdaderas) | `edad > 18 and tiene_licencia` |
| `or` | O (al menos una debe ser verdadera) | `es_lluvia or es_nieve` |
| `not` | NO (invierte el resultado) | `not es_nocturno` |

#### Ejemplos

```python
# Operador AND (Y)
edad = 25
tiene_licencia = True

if edad >= 18 and tiene_licencia:
    print("✅ Puedes conducir")
else:
    print("❌ No puedes conducir")

# Resultado: ✅ Puedes conducir
```

```python
# Operador OR (O)
es_fin_de_semana = True
es_festivo = False

if es_fin_de_semana or es_festivo:
    print("🎉 ¡No hay trabajo hoy!")
else:
    print("💼 Día de trabajo")

# Resultado: 🎉 ¡No hay trabajo hoy!
```

```python
# Operador NOT (NO)
lluvia = False

if not lluvia:
    print("☀️ Es un buen día para salir")
else:
    print("🌧️ Mejor quedarse adentro")

# Resultado: ☀️ Es un buen día para salir
```

---

## 🔁 BUCLES

### ¿Qué son los Bucles?

Los **bucles** son estructuras que **repiten un bloque de código** mientras se cumpla una condición o para cada elemento en una colección.

**Analogía:** Lavar platos es un bucle: mientras haya platos sucios, lavas uno.

---

### Bucle `while` (Mientras)

Repite un bloque de código **mientras** una condición sea verdadera.

```python
# Sintaxis
while condición:
    # Este código se repite mientras la condición sea verdadera
```

#### Ejemplo 1: Contar hasta 5

```python
contador = 1

while contador <= 5:
    print(f"Número: {contador}")
    contador = contador + 1
```

**Salida:**
```
Número: 1
Número: 2
Número: 3
Número: 4
Número: 5
```

**¿Cómo funciona?**
1. `contador = 1`: Empezamos en 1
2. ¿`1 <= 5`? Sí → Imprimimos "Número: 1"
3. `contador = 2`: Incrementamos contador
4. ¿`2 <= 5`? Sí → Imprimimos "Número: 2"
5. ... (se repite hasta que contador sea 6)
6. ¿`6 <= 5`? No → El bucle termina

#### Ejemplo 2: Sistema de ingreso en transporte

```python
# Simular pasajeros entrando al bus
pasajeros_en_bus = 0
capacidad = 5

while pasajeros_en_bus < capacidad:
    print(f"Pasajero subiendo... ({pasajeros_en_bus + 1}/{capacidad})")
    pasajeros_en_bus = pasajeros_en_bus + 1

print("🚌 Bus lleno, cerrando puertas")
```

**Salida:**
```
Pasajero subiendo... (1/5)
Pasajero subiendo... (2/5)
Pasajero subiendo... (3/5)
Pasajero subiendo... (4/5)
Pasajero subiendo... (5/5)
🚌 Bus lleno, cerrando puertas
```

#### ⚠️ ADVERTENCIA: Bucles Infinitos

Si la condición nunca se vuelve falsa, el bucle se ejecutará infinitamente.

```python
# ❌ MALO - Esto es un bucle infinito
contador = 1
while contador <= 5:
    print(f"Número: {contador}")
    # PROBLEMA: contador nunca aumenta, ¡siempre será 1!
```

**Cómo evitarlo:** Asegúrate de que algo en el bucle cambie la condición.

```python
# ✅ CORRECTO
contador = 1
while contador <= 5:
    print(f"Número: {contador}")
    contador = contador + 1  # Aquí aumentamos contador
```

---

### Bucle `for` (Para)

Repite un bloque de código para **cada elemento** en una colección (lista, rango, cadena, etc.).

```python
# Sintaxis
for variable in colección:
    # Este código se ejecuta para cada elemento en la colección
```

#### Ejemplo 1: Iterar sobre un rango

```python
# Usar range() para generar una secuencia de números
for numero in range(1, 6):  # Números del 1 al 5
    print(f"Número: {numero}")
```

**Salida:**
```
Número: 1
Número: 2
Número: 3
Número: 4
Número: 5
```

**¿Cómo funciona `range()`?**
- `range(1, 6)`: Genera números desde 1 hasta 5 (el 6 no se incluye)
- `range(5)`: Genera números 0, 1, 2, 3, 4 (si omites el inicio, comienza en 0)
- `range(0, 10, 2)`: Genera 0, 2, 4, 6, 8 (cada 2 números, esto es el "paso")

#### Ejemplo 2: Iterar sobre una lista

```python
buses = ["B-123", "B-456", "B-789"]

for bus in buses:
    print(f"Bus: {bus}")
```

**Salida:**
```
Bus: B-123
Bus: B-456
Bus: B-789
```

#### Ejemplo 3: Iterar sobre caracteres en una cadena

```python
palabra = "HOLA"

for letra in palabra:
    print(f"Letra: {letra}")
```

**Salida:**
```
Letra: H
Letra: O
Letra: L
Letra: A
```

#### Ejemplo 4: Sistema de registro de pasajeros

```python
# Registrar pasajeros en un bus
pasajeros = ["Carlos", "María", "José", "Ana"]

for pasajero in pasajeros:
    print(f"✅ {pasajero} subió al bus")
```

**Salida:**
```
✅ Carlos subió al bus
✅ María subió al bus
✅ José subió al bus
✅ Ana subió al bus
```

---

### `while` vs `for`: ¿Cuándo usar cada uno?

| Situación | Usar |
|-----------|------|
| Sabes cuántas veces repetir | `for` (más limpio) |
| No sabes cuántas veces repetir | `while` |
| Iterar sobre una lista/rango | `for` |
| Repetir hasta que algo ocurra | `while` |

#### Ejemplo: Los dos hacen lo mismo

```python
# Versión con for
print("=== Usando for ===")
for numero in range(1, 4):
    print(f"Número: {numero}")

# Versión con while
print("\n=== Usando while ===")
numero = 1
while numero < 4:
    print(f"Número: {numero}")
    numero = numero + 1
```

**Salida:**
```
=== Usando for ===
Número: 1
Número: 2
Número: 3

=== Usando while ===
Número: 1
Número: 2
Número: 3
```

---

### Sentencias de Control de Bucles

#### `break` - Salir del bucle

Detiene el bucle inmediatamente, sin importar la condición.

```python
# Ejemplo: Buscar a un pasajero específico
pasajeros = ["Carlos", "María", "José", "Ana"]

for pasajero in pasajeros:
    print(f"Buscando a {pasajero}...")
    if pasajero == "José":
        print("¡Encontrado!")
        break  # Salir del bucle cuando lo encontramos
```

**Salida:**
```
Buscando a Carlos...
Buscando a María...
Buscando a José...
¡Encontrado!
```

#### `continue` - Saltar a la siguiente iteración

Salta el resto del código en la iteración actual y va a la siguiente.

```python
# Ejemplo: Procesar solo a los pasajeros VIP
pasajeros = ["Carlos", "VIP-María", "José", "VIP-Ana"]

for pasajero in pasajeros:
    if not pasajero.startswith("VIP"):
        continue  # Saltamos los no-VIP
    print(f"✨ Tratamiento especial para {pasajero}")
```

**Salida:**
```
✨ Tratamiento especial para VIP-María
✨ Tratamiento especial para VIP-Ana
```

---

## 🔗 COMBINACIÓN DE CONDICIONALES Y BUCLES

La verdadera potencia viene cuando combinamos condicionales y bucles.

#### Ejemplo 1: Validar edades en una lista

```python
edades = [15, 25, 12, 30, 18]

for edad in edades:
    if edad >= 18:
        print(f"✅ Persona con {edad} años: Mayor de edad")
    else:
        print(f"❌ Persona con {edad} años: Menor de edad")
```

**Salida:**
```
❌ Persona con 15 años: Menor de edad
✅ Persona con 25 años: Mayor de edad
❌ Persona con 12 años: Menor de edad
✅ Persona con 30 años: Mayor de edad
✅ Persona con 18 años: Mayor de edad
```

#### Ejemplo 2: Sistema de compra de boletos (como en transporte)

```python
# Cliente quiere comprar múltiples boletos
dinero_disponible = 10
precio_boleto = 1.50
boletos_comprados = 0

while dinero_disponible >= precio_boleto:
    print(f"Compraste un boleto. Dinero restante: ${dinero_disponible - precio_boleto:.2f}")
    dinero_disponible = dinero_disponible - precio_boleto
    boletos_comprados = boletos_comprados + 1

print(f"\n📊 Boletos comprados: {boletos_comprados}")
print(f"💰 Dinero restante: ${dinero_disponible:.2f}")
```

**Salida:**
```
Compraste un boleto. Dinero restante: $8.50
Compraste un boleto. Dinero restante: $7.00
Compraste un boleto. Dinero restante: $5.50
Compraste un boleto. Dinero restante: $4.00
Compraste un boleto. Dinero restante: $2.50
Compraste un boleto. Dinero restante: $1.00

📊 Boletos comprados: 6
💰 Dinero restante: $1.00
```

#### Ejemplo 3: Filtrar datos (como búsqueda de buses)

```python
buses = [
    {"numero": "B-123", "ruta": "Ruta 1", "pasajeros": 45},
    {"numero": "B-456", "ruta": "Ruta 2", "pasajeros": 30},
    {"numero": "B-789", "ruta": "Ruta 1", "pasajeros": 50},
]

# Encontrar todos los buses con menos de 40 pasajeros
print("Buses disponibles (menos de 40 pasajeros):")
for bus in buses:
    if bus["pasajeros"] < 40:
        print(f"  - {bus['numero']} ({bus['ruta']}): {bus['pasajeros']} pasajeros")
```

**Salida:**
```
Buses disponibles (menos de 40 pasajeros):
  - B-456 (Ruta 2): 30 pasajeros
```

---

## ✅ MEJORES PRÁCTICAS

### 1. Usa nombres descriptivos para variables

```python
# ❌ Malo
for i in range(10):
    print(i)

# ✅ Bueno
for numero_intentos in range(10):
    print(numero_intentos)
```

### 2. Mantén tu código legible con indentación

```python
# ❌ Confuso
for bus in buses:
    if bus["pasajeros"] < 50:
        if bus["ruta"] == "Ruta 1":
            print(bus["numero"])

# ✅ Más legible
for bus in buses:
    if bus["pasajeros"] < 50:
        if bus["ruta"] == "Ruta 1":
            print(bus["numero"])
```

### 3. Evita bucles infinitos

```python
# ❌ Peligroso
while True:
    print("Esto se ejecuta infinitamente")

# ✅ Mejor
contador = 0
while contador < 10:
    print(f"Iteración {contador}")
    contador = contador + 1
```

### 4. Usa `for` en lugar de `while` cuando sea posible

```python
# ❌ Más complejo
contador = 0
while contador < 5:
    print(f"Número: {contador}")
    contador = contador + 1

# ✅ Más simple
for numero in range(5):
    print(f"Número: {numero}")
```

---

## 🎯 EJERCICIOS

### Ejercicio 1: Tabla de multiplicar

```python
# Escribe un programa que imprima la tabla de multiplicar del 5
# Uso: Bucle for, condicionales (opcional)
# Salida esperada:
# 5 x 1 = 5
# 5 x 2 = 10
# ...
# 5 x 10 = 50
```

### Ejercicio 2: Encontrar el número mayor

```python
# Dado una lista de números, encuentra el mayor
numeros = [23, 45, 12, 67, 34]
# Pista: Usa un bucle y condicionales
# Salida esperada: 67
```

### Ejercicio 3: Validar entrada del usuario

```python
# Crea un programa que pida un número entre 1 y 10
# Si el usuario ingresa algo fuera de ese rango, pide de nuevo
# Usa: while, condicionales
```

### Ejercicio 4: Contar vocales

```python
# Dado una palabra, cuenta cuántas vocales tiene
palabra = "programacion"
# Pista: Usa un bucle for para iterar cada letra
# Salida esperada: 5
```

### Ejercicio 5: Sistema de login

```python
# Crea un sistema de login que:
# - Pide usuario y contraseña
# - Permite 3 intentos
# - Si es correcto, muestra "Bienvenido"
# - Si fallan los 3 intentos, muestra "Acceso denegado"
# Usa: while, condicionales, contador
```

---

## 📚 Recursos Adicionales

- [Documentación oficial de Python - Control de Flujo](https://docs.python.org/es/3/tutorial/controlflow.html)
- [W3Schools - Python If...Else](https://www.w3schools.com/python/python_conditions.asp)
- [W3Schools - Python Loops](https://www.w3schools.com/python/python_while_loops.asp)

---

## 🎓 Resumen

| Concepto | Qué es | Ejemplo |
|----------|--------|---------|
| **if** | Toma una decisión | `if edad >= 18:` |
| **else** | Alternativa si la condición es falsa | `else:` |
| **elif** | Múltiples condiciones | `elif edad >= 13:` |
| **while** | Repite mientras algo sea verdadero | `while contador < 5:` |
| **for** | Repite para cada elemento | `for num in range(5):` |
| **break** | Sale del bucle | `break` |
| **continue** | Salta a la siguiente iteración | `continue` |

---

**Desarrollado por:** Alejandro López - Curso de Python  
**Fecha:** Mayo 2025  
**Nivel:** Principiantes