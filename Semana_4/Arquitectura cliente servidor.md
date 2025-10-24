# 🏗️ Arquitectura Cliente-Servidor - Documentación Completa

**Profesor:** Alejandro López  
**Semana:** 4 - Bucles y Condicionales  
**Tema:** Peticiones HTTP con Bucles y Condicionales  
**Año:** 2025

---

## 📚 Tabla de contenidos

1. [Conceptos Básicos](#conceptos-básicos)
2. [Arquitectura Cliente-Servidor](#arquitectura-cliente-servidor)
3. [Peticiones HTTP](#peticiones-http)
4. [Respuestas HTTP](#respuestas-http)
5. [Bucles en Peticiones](#bucles-en-peticiones)
6. [Condicionales en Peticiones](#condicionales-en-peticiones)
7. [Ejemplos Prácticos](#ejemplos-prácticos)
8. [Ejercicios](#ejercicios)

---

## 🎯 Conceptos Básicos

### ¿Qué es el Internet?

El internet es una **red de computadoras** conectadas entre sí que se comunican intercambiando datos.

### ¿Qué es una API?

Una **API** (Application Programming Interface) es:
- Un conjunto de reglas para comunicarse con un servidor
- Un servidor que proporciona datos a quien los solicita
- Una forma de **acceder a información sin crear los datos**

### ¿Qué es HTTP?

**HTTP** (HyperText Transfer Protocol) es:
- Un protocolo de comunicación en el internet
- La base del funcionamiento de la Web
- Usado para enviar **peticiones y recibir respuestas**

---

## 🏗️ Arquitectura Cliente-Servidor

### Modelo General

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│           ARQUITECTURA CLIENTE-SERVIDOR            │
│                                                     │
│  ┌─────────────┐          ┌──────────────┐        │
│  │             │          │              │        │
│  │   CLIENTE   │ ─────→   │  SERVIDOR    │        │
│  │ (Tu Program)│          │   (API)      │        │
│  │             │ ←─────   │              │        │
│  └─────────────┘          └──────────────┘        │
│      Solicita                Proporciona           │
│      datos                   datos                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Flujo de Comunicación

```
PASO 1: Cliente prepara solicitud
   └─ Define URL
   └─ Elige método (GET, POST, etc.)
   └─ Establece timeout

PASO 2: Cliente envía solicitud
   └─ A través de Internet
   └─ Al servidor especificado

PASO 3: Servidor recibe solicitud
   └─ Lee la URL
   └─ Busca los datos
   └─ Prepara respuesta

PASO 4: Servidor envía respuesta
   └─ En formato JSON
   └─ Con código de estado (200, 404, etc.)
   └─ A través de Internet

PASO 5: Cliente recibe respuesta
   └─ Verifica el código de estado
   └─ Convierte JSON a diccionario Python
   └─ Procesa los datos

PASO 6: Cliente imprime/usa los datos
   └─ Aplicando BUCLES
   └─ Aplicando CONDICIONALES
```

### Ejemplo Real: Restaurante

```
┌──────────────────────────────────────────────────────────┐
│ ANALOGÍA CON LA VIDA REAL                              │
│                                                          │
│ CLIENTE (TÚ)              SERVIDOR (RESTAURANTE)       │
│ │                        │                             │
│ ├─ Abres menú ──────────>│ Te dan menú                 │
│ │                        │                             │
│ ├─ Pides plato ─────────>│ Cocinan el plato            │
│ │                        │                             │
│ │<───── Traen plato ─────┤ Traen con código 200 (éxito)│
│ │                        │                             │
│ ├─ Comes (procesas)      │ (No participa)              │
│ │                        │                             │
│ └─ Dices si te gustó     │ (No participa)              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 📤 Peticiones HTTP

### Métodos HTTP

| Método | Significado | Ejemplo | Código |
|--------|------------|---------|--------|
| **GET** | Obtener datos | Pedir información | `requests.get(url)` |
| **POST** | Crear datos | Enviar formulario | `requests.post(url, data)` |
| **PUT** | Actualizar datos | Modificar usuario | `requests.put(url, data)` |
| **DELETE** | Eliminar datos | Borrar usuario | `requests.delete(url)` |

### GET - Obtener Datos

GET es el método que usamos para **obtener información** sin modificar nada en el servidor.

```python
# SINTAXIS BÁSICA
import requests

respuesta = requests.get(URL, timeout=10)
```

**Parámetros:**
- `URL`: Dirección del servidor + ruta específica
- `timeout`: Máximo de segundos a esperar

**Ejemplo:**
```python
respuesta = requests.get(
    "https://reqres.in/api/users?page=1",
    timeout=10
)
```

### Estructura de una URL

```
https://reqres.in/api/users?page=1
│      │     │   │    │      │
│      │     │   │    │      └─ Parámetro: page=1
│      │     │   │    └─ Ruta: /api/users
│      │     │   └─ Dominio: reqres.in
│      │     └─ Protocolo: https
│      └─ Subdominio: (ninguno)
└─ Protocolo completo: https
```

### Parámetros en la URL

```python
# Parámetros en la URL
url = "https://jsonplaceholder.typicode.com/posts?userId=1&limit=5"
#                                              └──────────────────
#                                              Parámetros de consulta
```

---

## 📥 Respuestas HTTP

### Códigos de Estado HTTP

```python
respuesta.status_code  # Número de código
respuesta.text         # Contenido en texto
respuesta.json()       # Contenido en JSON (diccionario)
```

### Códigos Comunes

| Código | Significado | Ejemplo |
|--------|------------|---------|
| **200** | OK - Éxito | Datos disponibles |
| **201** | Creado | Se creó un registro |
| **204** | Sin contenido | Operación exitosa sin datos |
| **400** | Solicitud inválida | URL incorrecta |
| **401** | No autorizado | API key incorrecta |
| **403** | Prohibido | Acceso denegado |
| **404** | No encontrado | Recurso no existe |
| **500** | Error del servidor | Problema en el servidor |
| **503** | Servicio no disponible | Servidor sobrecarh |

### Estructura de Respuesta JSON

```json
{
  "data": [
    {
      "id": 1,
      "first_name": "George",
      "last_name": "Bluth",
      "email": "george.bluth@reqres.in",
      "avatar": "https://..."
    },
    {
      "id": 2,
      "first_name": "Janet",
      "last_name": "Weaver",
      "email": "janet.weaver@reqres.in",
      "avatar": "https://..."
    }
  ],
  "page": 1,
  "per_page": 6,
  "total": 12,
  "total_pages": 2
}
```

### Convertir JSON a Diccionario Python

```python
respuesta = requests.get(url)

# Convertir JSON a diccionario
datos = respuesta.json()

# Ahora puedes acceder como diccionario
print(datos['data'])        # Lista de usuarios
print(datos['page'])         # Página actual
print(datos['per_page'])     # Usuarios por página
```

---

## 🔄 Bucles en Peticiones

### Bucle FOR Básico

```python
for usuario in datos['data']:
    print(usuario['first_name'])
```

**Ejecución:**
```
Iteración 1: usuario = {id: 1, first_name: 'George', ...}
Iteración 2: usuario = {id: 2, first_name: 'Janet', ...}
Iteración 3: usuario = {id: 3, first_name: 'Emma', ...}
...
```

### enumerate() - Obtener Índice

```python
for indice, usuario in enumerate(datos['data'], 1):
    print(f"{indice}. {usuario['first_name']}")
```

**Ejecución:**
```
Iteración 1: indice=1, usuario={...}  → "1. George"
Iteración 2: indice=2, usuario={...}  → "2. Janet"
Iteración 3: indice=3, usuario={...}  → "3. Emma"
```

### Bucle WHILE

```python
indice = 0
while indice < len(datos['data']):
    usuario = datos['data'][indice]
    print(usuario['first_name'])
    indice += 1
```

### break - Salir del Bucle

```python
for indice, pub in enumerate(publicaciones, 1):
    if indice <= 3:
        print(pub['title'])
    else:
        break  # Salir del bucle
```

---

## ❓ Condicionales en Peticiones

### Verificar Código de Estado

```python
if respuesta.status_code == 200:
    print("✅ Éxito - Datos disponibles")
else:
    print("❌ Error - No se pudieron obtener datos")
```

### Validar Campo Existe

```python
usuario = {'id': 1, 'name': 'John'}

if 'email' in usuario:
    print(usuario['email'])
else:
    print("Email no disponible")
```

### Validar Valor No es "unknown"

```python
altura = personaje.get('height', 'unknown')

if altura != "unknown":
    print(f"Altura: {altura} cm")
else:
    print("Altura no disponible")
```

### Condicionales Complejos

```python
if 'first_name' in usuario and 'last_name' in usuario:
    nombre = f"{usuario['first_name']} {usuario['last_name']}"
    print(nombre)
```

### if-elif-else

```python
for indice, pub in enumerate(publicaciones, 1):
    if indice <= 3:
        print(pub['title'])
    elif indice == 4:
        print(f"... y {len(publicaciones) - 3} más")
        break
    else:
        pass  # No hacer nada
```

---

## 💻 Ejemplos Prácticos

### Ejemplo 1: Obtener y Procesar Usuarios

```python
import requests

# 1. Hacer petición
respuesta = requests.get("https://reqres.in/api/users?page=1")

# 2. Validar respuesta
if respuesta.status_code == 200:
    datos = respuesta.json()
    
    # 3. Bucle para procesar cada usuario
    for usuario in datos['data']:
        # 4. Condicionales para validar datos
        if 'first_name' in usuario and 'email' in usuario:
            nombre = usuario['first_name']
            email = usuario['email']
            print(f"{nombre}: {email}")
```

**Salida:**
```
George: george.bluth@reqres.in
Janet: janet.weaver@reqres.in
Emma: emma.wong@reqres.in
```

### Ejemplo 2: Filtrar Datos

```python
# Obtener Pokémon que contienen 'a' en su nombre
respuesta = requests.get("https://pokeapi.co/api/v2/pokemon?limit=10")

if respuesta.status_code == 200:
    datos = respuesta.json()
    
    for pokemon in datos['results']:
        nombre = pokemon['name'].lower()
        
        # Condicional: ¿Contiene 'a'?
        if 'a' in nombre:
            print(nombre.upper())
```

### Ejemplo 3: Contar Elementos

```python
respuesta = requests.get("https://jsonplaceholder.typicode.com/posts?userId=1")

if respuesta.status_code == 200:
    posts = respuesta.json()
    contador = 0
    
    for post in posts:
        contador += 1
    
    print(f"Total de posts: {contador}")
```

### Ejemplo 4: Encontrar Elemento Específico

```python
respuesta = requests.get("https://reqres.in/api/users?page=1")

if respuesta.status_code == 200:
    datos = respuesta.json()
    
    for usuario in datos['data']:
        if usuario['id'] == 2:  # Encontrar usuario con ID=2
            print(f"Encontrado: {usuario['first_name']}")
            break  # Salir del bucle
```

---

## 📖 Ejercicios

### Nivel 1 - Básico

**Ejercicio 1.1:** Contar usuarios
```python
# Obtener usuarios y contar cuántos hay
# (Pista: usa len())
```

**Ejercicio 1.2:** Mostrar primer usuario
```python
# Obtener usuarios y mostrar solo el primero
# (Pista: usa datos['data'][0])
```

**Ejercicio 1.3:** Filtrar por ID
```python
# Obtener usuarios y mostrar solo el usuario con ID=1
# (Pista: usa if usuario['id'] == 1)
```

### Nivel 2 - Intermedio

**Ejercicio 2.1:** Tabla formateada
```python
# Obtener usuarios y crear una tabla:
# ID  Nombre          Email
# 1   George Bluth    george.bluth@reqres.in
# 2   Janet Weaver    janet.weaver@reqres.in
```

**Ejercicio 2.2:** Buscar Pokémon
```python
# Obtener Pokémon que contengan 'a' en su nombre
# Mostrar: nombre y URL
```

**Ejercicio 2.3:** Validar altura
```python
# Obtener personajes de Star Wars
# Mostrar solo los que tengan altura > 170 cm
```

### Nivel 3 - Avanzado

**Ejercicio 3.1:** Múltiples peticiones
```python
# Obtener 3 páginas de usuarios
# Mostrar el nombre del usuario con ID más alto
```

**Ejercicio 3.2:** Combinar datos
```python
# Obtener Pokémon y publicaciones
# Mostrar: "Pokemon X tiene Y posts"
```

**Ejercicio 3.3:** Crear estadísticas
```python
# Obtener personajes de Star Wars
# Mostrar: promedio de altura, total de personajes, etc.
```

---

## 🎓 Resumen

### Conceptos Clave

✅ **Arquitectura Cliente-Servidor:**
- Cliente (tu programa) solicita datos
- Servidor (API) proporciona datos
- Comunicación a través de HTTP

✅ **Peticiones HTTP:**
- GET: obtener información
- URL: dirección del servidor
- timeout: máximo de espera

✅ **Respuestas HTTP:**
- status_code: 200 = éxito
- JSON: formato de datos
- diccionario: estructura en Python

✅ **Bucles:**
- for: iterar sobre cada elemento
- enumerate(): obtener índice
- break: salir del bucle

✅ **Condicionales:**
- if: verificar condición
- in: ¿existe el campo?
- !=: ¿no es igual?

---

**Profesor:** Alejandro López  
**Semana:** 4 - Bucles y Condicionales  
**Año:** 2025