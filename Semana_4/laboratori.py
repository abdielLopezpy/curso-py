# ============================================================================
# EJEMPLO COMPLETO: PETICIONES HTTP CON BUCLES Y CONDICIONALES
#
# OBJETIVO EDUCATIVO:
# 1. Entender la Arquitectura Cliente-Servidor
# 2. Aprender qué son las Peticiones HTTP (GET)
# 3. Practicar BUCLES (for) para iterar datos
# 4. Practicar CONDICIONALES (if-else) para validar datos
# 5. Combinar conceptos en aplicaciones reales
#
# Profesor: Alejandro López
# Semana: 4 - Bucles y Condicionales
# Año: 2025
# ============================================================================

"""
📚 CONCEPTOS TEÓRICOS APLICADOS:

1. ARQUITECTURA CLIENTE-SERVIDOR
   ═══════════════════════════════════════════════════════════════════════

   ┌─────────────┐                          ┌─────────────┐
   │   CLIENTE   │  ──(HTTP GET REQUEST)──> │   SERVIDOR  │
   │ (nuestro    │                          │  (API)      │
   │  programa)  │                          │             │
   │             │  <──(JSON RESPONSE)────  │             │
   └─────────────┘                          └─────────────┘

   • CLIENTE: Tu programa Python que solicita datos
   • SERVIDOR: Servidores web que almacenan y responden datos
   • HTTP GET: Método para SOLICITAR información (no modificar)
   • JSON: Formato de datos que recibimos (diccionarios Python)
   • PETICIÓN: Tu programa pregunta al servidor
   • RESPUESTA: El servidor devuelve datos

2. FLUJO DE UNA PETICIÓN HTTP:
   ═══════════════════════════════════════════════════════════════════════

   PASO 1: Cliente prepara petición GET
   PASO 2: Cliente envía petición al servidor
   PASO 3: Servidor recibe la petición
   PASO 4: Servidor busca los datos
   PASO 5: Servidor formatea datos en JSON
   PASO 6: Servidor devuelve respuesta con código 200 (éxito)
   PASO 7: Cliente recibe los datos en JSON
   PASO 8: Cliente convierte JSON a diccionario Python
   PASO 9: Cliente procesa datos con BUCLES y CONDICIONALES
   PASO 10: Cliente imprime resultados

3. CÓDIGOS DE RESPUESTA HTTP:
   ═══════════════════════════════════════════════════════════════════════

   200 OK               → Éxito, datos disponibles
   404 Not Found        → El servidor no encontró el recurso
   500 Server Error     → Error en el servidor
   403 Forbidden        → Acceso denegado
   401 Unauthorized     → Se requiere autenticación (API key)

4. BUCLES EN PETICIONES HTTP:
   ═══════════════════════════════════════════════════════════════════════

   for indice, elemento in enumerate(datos, 1):
       # BUCLE: Procesa CADA elemento de la respuesta
       # enumerate() = proporciona índice (1,2,3...) y elemento
       # datos = array JSON del servidor

5. CONDICIONALES EN PETICIONES HTTP:
   ═══════════════════════════════════════════════════════════════════════

   if respuesta.status_code == 200:
       # CONDICIONAL: ¿Fue exitosa la petición?

   if 'campo' in usuario:
       # CONDICIONAL: ¿Existe este campo en los datos?

   if altura != "unknown":
       # CONDICIONAL: ¿El valor es válido?
"""

import requests
import json
from datetime import datetime

# ============================================================================
# ENCABEZADO DEL PROGRAMA
# ============================================================================

print("╔" + "═" * 70 + "╗")
print("║" + " " * 70 + "║")
print("║" + " " * 10 + "PETICIONES HTTP CON BUCLES Y CONDICIONALES" + " " * 17 + "║")
print("║" + " " * 10 + "Arquitectura Cliente-Servidor en Python" + " " * 20 + "║")
print("║" + " " * 70 + "║")
print("╚" + "═" * 70 + "╝\n")

print("👨‍🔬 Profesor: Alejandro López")
print("📚 Tema: Bucles y Condicionales")
print("🌐 Arquitectura: Cliente-Servidor con APIs públicas")
print("📅 Semana: 4 - Bucles y Condicionales en Python\n")

# ============================================================================
# INTRODUCCIÓN A ARQUITECTURA CLIENTE-SERVIDOR
# ============================================================================

print("\n" + "=" * 70)
print("🏗️  ARQUITECTURA CLIENTE-SERVIDOR - EXPLICACIÓN")
print("=" * 70)

print("""
¿QUÉ ES UNA PETICIÓN HTTP?
───────────────────────────────────────────────────────────────────────

Una PETICIÓN HTTP es cuando tu programa (CLIENTE) le pide información
a un servidor web (SERVIDOR).

EJEMPLO REAL:
  1. Tú (Cliente) vas a un restaurante
  2. Le pides al mesero (Servidor) un menú
  3. El mesero trae el menú
  4. Tú lees el menú
  5. Pides un plato

EN PROGRAMACIÓN:
  1. Tu programa (Cliente) hace una petición GET
  2. El servidor recibe la petición
  3. El servidor busca los datos
  4. El servidor responde con JSON
  5. Tu programa procesa los datos

VENTAJAS DE USAR APIs:
  ✅ No tienes que crear los datos
  ✅ Datos en tiempo real
  ✅ Fácil acceso a información
  ✅ Escalable (muchas peticiones simultáneas)
  ✅ Reutilizable (múltiples clientes)
""")

# ============================================================================
# EJEMPLO 1: PETICIÓN HTTP - USUARIOS (ReqRes)
# ============================================================================

print("EJEMPLO 1: PETICIÓN HTTP - OBTENER USUARIOS")
print("=" * 70)

print("""
📌 ARQUITECTURA EN ESTE EJEMPLO:

    Tu Programa                        Servidor ReqRes
    (Cliente)                          (Servidor)
        │                                  │
        │────── PETICIÓN GET ─────────────>│
        │  GET https://reqres.in/          │
        │  /api/users?page=1               │
        │                                  │
        │<──── RESPUESTA JSON ─────────────│
        │  {                               │
        │    "data": [                    │
        │      {"id": 1, "name": "..."}   │
        │      ...                        │
        │    ]                            │
        │  }                              │
        │                                  │
        ├─ PROCESA CON BUCLES Y CONDICIONALES
        │
        └─ IMPRIME RESULTADOS

📋 FLUJO DEL CÓDIGO:
   1. Cliente hace petición GET
   2. Servidor responde con código 200 (éxito)
   3. Cliente recibe JSON
   4. Cliente convierte JSON a diccionario Python
   5. Cliente ITERA con BUCLE FOR sobre cada usuario
   6. Cliente valida datos con CONDICIONALES
   7. Cliente imprime resultados formateados
""")

print("\n⏳ Conectando con servidor: https://reqres.in/api/users?page=1")
print("   (Esperando respuesta del servidor...)\n")

try:
    # ═════════════════════════════════════════════════════════════════
    # PASO 1: CLIENTE HACE PETICIÓN GET AL SERVIDOR
    # ═════════════════════════════════════════════════════════════════

    print("📤 CLIENTE: Enviando petición GET al servidor...")
    print("   └─ URL: https://reqres.in/api/users?page=1")
    print("   └─ Método: GET")
    print("   └─ Timeout: 10 segundos")
    print("   └─ Esperando respuesta...\n")

    respuesta = requests.get("https://reqres.in/api/users?page=1", timeout=10)

    # ═════════════════════════════════════════════════════════════════
    # PASO 2: CLIENTE RECIBE RESPUESTA DEL SERVIDOR
    # ═════════════════════════════════════════════════════════════════

    print("📥 SERVIDOR: Respuesta recibida")
    print(f"   └─ Código de estado HTTP: {respuesta.status_code}")
    print(f"   └─ Tamaño: {len(respuesta.text)} caracteres")
    print(f"   └─ Tipo de contenido: {respuesta.headers.get('content-type', 'Desconocido')}\n")

    # ═════════════════════════════════════════════════════════════════
    # PASO 3: CONDICIONAL - VERIFICAR SI LA RESPUESTA FUE EXITOSA
    # ═════════════════════════════════════════════════════════════════

    print("✓ CONDICIONAL 1: ¿La respuesta fue exitosa?")
    print(f"  if respuesta.status_code == 200:")

    if respuesta.status_code == 200:
        print(f"     └─ ✅ SÍ (Código {respuesta.status_code} = Éxito)\n")

        # ═════════════════════════════════════════════════════════════
        # PASO 4: CONVERTIR JSON A DICCIONARIO PYTHON
        # ═════════════════════════════════════════════════════════════

        print("🔄 Convirtiendo JSON a diccionario Python...")
        datos = respuesta.json()
        print(f"   └─ Tipo de datos: {type(datos)}")
        print(f"   └─ Claves disponibles: {list(datos.keys())}\n")

        # ═════════════════════════════════════════════════════════════
        # INFORMACIÓN GENERAL
        # ═════════════════════════════════════════════════════════════

        print(f"📊 Información de la respuesta:")
        print(f"   └─ Total de usuarios en esta página: {datos['per_page']}")
        print(f"   └─ Página actual: {datos['page']}")
        print(f"   └─ Total de usuarios (todas las páginas): {datos['total']}\n")

        # ═════════════════════════════════════════════════════════════
        # PASO 5: BUCLE FOR - ITERAR SOBRE CADA USUARIO
        # ═════════════════════════════════════════════════════════════

        print("👥 LISTA DE USUARIOS:")
        print("-" * 70)
        print("✓ BUCLE FOR: for indice, usuario in enumerate(datos['data'], 1):")
        print("  └─ Iterará sobre CADA usuario en la lista\n")

        for indice, usuario in enumerate(datos['data'], 1):
            print(f"📍 ITERACIÓN {indice} del BUCLE:")
            print(f"   Usuario recibido del servidor: {usuario}\n")

            # ═════════════════════════════════════════════════════
            # CONDICIONAL 2: VALIDAR CAMPOS EXISTE EN DICCIONARIO
            # ═════════════════════════════════════════════════════

            print(f"   ✓ CONDICIONAL 2: ¿Existen los campos requeridos?")
            print(f"     if 'first_name' in usuario and 'last_name' in usuario:")

            if 'first_name' in usuario and 'last_name' in usuario:
                print(f"        └─ ✅ SÍ (Campos encontrados)\n")

                # Extraer datos
                nombre_completo = f"{usuario['first_name']} {usuario['last_name']}"
                email = usuario.get('email', 'Sin email')
                user_id = usuario['id']
                avatar = usuario.get('avatar', 'Sin avatar')

                # Imprimir formateado
                print(f"   ✓ DATOS PROCESADOS:")
                print(f"      {indice}. {nombre_completo}")
                print(f"         📧 Email: {email}")
                print(f"         🆔 ID: {user_id}")
                print(f"         📷 Avatar: {avatar[:50]}...\n")
            else:
                print(f"        └─ ❌ NO (Campos no encontrados)\n")
    else:
        # ═════════════════════════════════════════════════════════════
        # SI LA RESPUESTA NO FUE EXITOSA
        # ═════════════════════════════════════════════════════════════

        print(f"     └─ ❌ NO (Código {respuesta.status_code} ≠ 200)")
        print(f"❌ Error: El servidor devolvió un error")

except requests.exceptions.Timeout:
    print("❌ Error: TIMEOUT")
    print("   El servidor tardó más de 10 segundos en responder")
    print("   (Posible: servidor lento, internet lento, o servidor caído)")

except requests.exceptions.ConnectionError:
    print("❌ Error: NO HAY CONEXIÓN")
    print("   No se pudo conectar con el servidor")
    print("   (Posible: sin internet, servidor caído, URL incorrecta)")

except Exception as e:
    print(f"❌ Error inesperado: {str(e)}")

# ============================================================================
# EJEMPLO 2: PETICIÓN HTTP - POKÉMON (PokéAPI)
# ============================================================================

print("\n" + "=" * 70)
print("EJEMPLO 2: PETICIÓN HTTP - OBTENER POKÉMON")
print("=" * 70)

print("""
📌 ARQUITECTURA:

    Tu Programa                    Servidor PokéAPI
    (Cliente)                      (Servidor)
        │                              │
        │──── PETICIÓN GET ──────────> │
        │  GET pokeapi.co/             │
        │  /api/v2/pokemon?limit=5     │
        │                              │
        │ <──── RESPUESTA JSON ────────│
        │  {                           │
        │    "results": [              │
        │      {"name": "bulbasaur"}   │
        │      ...                     │
        │    ]                         │
        │  }                           │
        │                              │
        └─ PROCESA CON BUCLES

✓ CONDICIONALES APLICADOS:
   • if respuesta.status_code == 200
   • if len(nombre) > 0
   • if nombre válido
""")

print("\n⏳ Conectando con servidor: https://pokeapi.co/api/v2/pokemon?limit=5")
print("   (Esperando respuesta del servidor...)\n")

try:
    print("📤 CLIENTE: Enviando petición GET...")
    respuesta = requests.get("https://pokeapi.co/api/v2/pokemon?limit=5", timeout=10)

    print("📥 SERVIDOR: Respuesta recibida\n")
    print(f"✓ CONDICIONAL: if respuesta.status_code == 200:")

    if respuesta.status_code == 200:
        print(f"   └─ ✅ SÍ (Código 200)\n")

        datos = respuesta.json()
        total = datos['count']
        resultados = len(datos['results'])

        print(f"📊 Información:")
        print(f"   └─ Total de Pokémon en la API: {total}")
        print(f"   └─ Pokémon a mostrar: {resultados}\n")

        print("🎮 POKÉMON ENCONTRADOS:")
        print("-" * 70)
        print("✓ BUCLE FOR: for indice, pokemon in enumerate(datos['results'], 1):\n")

        for indice, pokemon in enumerate(datos['results'], 1):
            nombre = pokemon['name'].upper()
            url = pokemon['url']

            print(f"📍 ITERACIÓN {indice}:")
            print(f"   ✓ CONDICIONAL: if len(nombre) > 0:")

            if len(nombre) > 0:
                print(f"      └─ ✅ SÍ (Nombre válido: '{nombre}')\n")
                print(f"   {indice}. {nombre}")
                print(f"      🔗 URL: {url}")
                print(f"      📊 Longitud del nombre: {len(nombre)} caracteres\n")
            else:
                print(f"      └─ ❌ NO (Nombre vacío)\n")
    else:
        print(f"   └─ ❌ NO (Código {respuesta.status_code})")

except Exception as e:
    print(f"❌ Error: {str(e)}")

# ============================================================================
# EJEMPLO 3: PETICIÓN HTTP - STAR WARS (SWAPI)
# ============================================================================

print("\n" + "=" * 70)
print("EJEMPLO 3: PETICIÓN HTTP - PERSONAJES STAR WARS")
print("=" * 70)

print("""
📌 ARQUITECTURA:

    Tu Programa                    Servidor SWAPI
    (Cliente)                      (Servidor)
        │                              │
        │──── PETICIÓN GET ──────────> │
        │  GET swapi.dev/              │
        │  /api/people/?page=1         │
        │                              │
        │ <──── RESPUESTA JSON ────────│
        │  {                           │
        │    "results": [              │
        │      {                       │
        │        "name": "Luke",       │
        │        "height": "172",      │
        │        "mass": "77"          │
        │      }                       │
        │      ...                     │
        │    ]                         │
        │  }                           │
        │                              │
        └─ PROCESA CON CONDICIONALES

✓ CONDICIONALES COMPLEJOS APLICADOS:
   • if respuesta.status_code == 200
   • if altura != "unknown"
   • else (para valores desconocidos)
   • if masa != "unknown"
   • else (para valores desconocidos)
""")

print("\n⏳ Conectando con servidor: https://swapi.dev/api/people/?page=1")
print("   (Esperando respuesta del servidor...)\n")

try:
    print("📤 CLIENTE: Enviando petición GET...")
    respuesta = requests.get("https://swapi.dev/api/people/?page=1", timeout=10)

    print("📥 SERVIDOR: Respuesta recibida\n")
    print(f"✓ CONDICIONAL: if respuesta.status_code == 200:")

    if respuesta.status_code == 200:
        print(f"   └─ ✅ SÍ (Código 200)\n")

        datos = respuesta.json()

        print(f"📊 Información:")
        print(f"   └─ Total de personajes: {datos['count']}")
        print(f"   └─ En esta página: {len(datos['results'])}\n")

        print("⭐ PERSONAJES STAR WARS:")
        print("-" * 70)
        print("✓ BUCLE FOR: for indice, personaje in enumerate(datos['results'], 1):\n")

        for indice, personaje in enumerate(datos['results'], 1):
            nombre = personaje['name']
            altura = personaje.get('height', 'unknown')
            masa = personaje.get('mass', 'unknown')

            print(f"📍 ITERACIÓN {indice}: {nombre}")

            # CONDICIONAL PARA ALTURA
            print(f"   ✓ CONDICIONAL 1: if altura != 'unknown':")
            if altura != "unknown":
                altura_info = f"{altura} cm"
                print(f"      └─ ✅ SÍ (Altura válida)")
            else:
                altura_info = "Desconocida"
                print(f"      └─ ❌ NO (Altura no disponible)")

            # CONDICIONAL PARA MASA
            print(f"   ✓ CONDICIONAL 2: if masa != 'unknown':")
            if masa != "unknown":
                masa_info = f"{masa} kg"
                print(f"      └─ ✅ SÍ (Masa válida)")
            else:
                masa_info = "Desconocida"
                print(f"      └─ ❌ NO (Masa no disponible)")

            print(f"\n   Resultado procesado:")
            print(f"      {indice}. {nombre}")
            print(f"         📏 Altura: {altura_info}")
            print(f"         ⚖️  Masa: {masa_info}\n")
    else:
        print(f"   └─ ❌ NO (Código {respuesta.status_code})")

except Exception as e:
    print(f"❌ Error: {str(e)}")

# ============================================================================
# EJEMPLO 4: PETICIÓN HTTP - PUBLICACIONES (JSONPlaceholder)
# ============================================================================

print("\n" + "=" * 70)
print("EJEMPLO 4: PETICIÓN HTTP - PUBLICACIONES")
print("=" * 70)

print("""
📌 ARQUITECTURA:

    Tu Programa                        Servidor JSONPlaceholder
    (Cliente)                          (Servidor)
        │                                  │
        │──── PETICIÓN GET ────────────────> │
        │  GET jsonplaceholder.typicode/    │
        │  com/posts?userId=1               │
        │                                  │
        │ <──── RESPUESTA JSON ─────────────│
        │  [                               │
        │    {"id": 1, "title": "..."}    │
        │    {"id": 2, "title": "..."}    │
        │    ...                          │
        │  ]                              │
        │                                  │
        └─ PROCESA CON BREAK + IF-ELIF

✓ CONDICIONALES Y CONTROL DE FLUJO APLICADOS:
   • if indice <= 3 (mostrar solo los primeros 3)
   • elif indice > 3 (si hay más de 3)
   • break (salir del bucle antes de terminar)
""")

print("\n⏳ Conectando con servidor...")
print("   URL: https://jsonplaceholder.typicode.com/posts?userId=1")
print("   (Esperando respuesta del servidor...)\n")

try:
    print("📤 CLIENTE: Enviando petición GET...")
    respuesta = requests.get("https://jsonplaceholder.typicode.com/posts?userId=1", timeout=10)

    print("📥 SERVIDOR: Respuesta recibida\n")
    print(f"✓ CONDICIONAL: if respuesta.status_code == 200:")

    if respuesta.status_code == 200:
        print(f"   └─ ✅ SÍ (Código 200)\n")

        publicaciones = respuesta.json()
        total = len(publicaciones)

        print(f"📊 Información:")
        print(f"   └─ Total de publicaciones del usuario 1: {total}\n")

        print("📝 PUBLICACIONES:")
        print("-" * 70)
        print("""✓ BUCLE FOR CON CONDICIONALES:
   for indice, pub in enumerate(publicaciones, 1):
       if indice <= 3:           ← Mostrar solo primeros 3
           print(pub)
       elif indice > 3:          ← Si hay más de 3
           print(f"... y {total - 3} más")
           break                 ← Salir del bucle
""")
        print()

        for indice, pub in enumerate(publicaciones, 1):
            titulo = pub['title']
            user_id = pub['userId']
            post_id = pub['id']
            body = pub['body'][:60]

            print(f"📍 ITERACIÓN {indice}:")
            print(f"   ✓ CONDICIONAL: if indice <= 3:")

            if indice <= 3:
                print(f"      └─ ✅ SÍ (mostrar este elemento)\n")
                print(f"   {indice}. {titulo}")
                print(f"      Usuario ID: {user_id}")
                print(f"      Post ID: {post_id}")
                print(f"      Contenido: {body}...\n")

            elif indice > 3:
                print(f"      └─ ❌ NO (saltar al elif)\n")
                print(f"   ✓ CONDICIONAL: elif indice > 3:")
                print(f"      └─ ✅ SÍ (mostrar resumen)\n")
                print(f"   ... y {total - 3} publicaciones más")
                print(f"   ✓ STATEMENT: break (salir del bucle)\n")
                break
    else:
        print(f"   └─ ❌ NO (Código {respuesta.status_code})")

except Exception as e:
    print(f"❌ Error: {str(e)}")

# ============================================================================
# RESUMEN FINAL Y CONCLUSIONES
# ============================================================================

print("\n" + "=" * 70)
print("📚 RESUMEN: CONCEPTOS APLICADOS")
print("=" * 70)

print("""
✅ ARQUITECTURA CLIENTE-SERVIDOR DEMOSTRADA:

1. CLIENTE (Tu programa Python)
   ├─ Prepara una petición GET
   ├─ Especifica la URL del servidor
   ├─ Define timeout (máximo de espera)
   └─ Envía la petición al servidor

2. SERVIDOR (API pública)
   ├─ Recibe la petición GET
   ├─ Busca los datos solicitados
   ├─ Formatea los datos en JSON
   └─ Devuelve la respuesta con código HTTP

3. CLIENTE (recibe y procesa)
   ├─ Recibe la respuesta
   ├─ Verifica el código HTTP (200 = éxito)
   ├─ Convierte JSON a diccionario Python
   └─ Procesa datos con BUCLES Y CONDICIONALES

════════════════════════════════════════════════════════════════════════

✅ PETICIONES HTTP DEMOSTRADAS:

CONDICIONALES (if-else):
   ✓ Verificar status_code == 200
   ✓ Validar que los campos existan con 'in'
   ✓ Comparar valores con != "unknown"
   ✓ Condicionales complejos con if-elif-else

BUCLES (for):
   ✓ Iterar sobre arrays con for
   ✓ Usar enumerate() para obtener índice
   ✓ Acceder a diccionarios dentro de bucles
   ✓ break para salir antes del final

COMBINACIÓN:
   ✓ Bucles + Condicionales para filtrar
   ✓ Validar datos antes de procesar
   ✓ Procesar respuestas HTTP complejas

════════════════════════════════════════════════════════════════════════

✅ APIS PÚBLICAS UTILIZADAS (SIN AUTENTICACIÓN):

   1. ReqRes:          https://reqres.in/api/users
   2. PokéAPI:         https://pokeapi.co/api/v2/pokemon
   3. SWAPI:           https://swapi.dev/api/people
   4. JSONPlaceholder: https://jsonplaceholder.typicode.com/posts

════════════════════════════════════════════════════════════════════════

✅ CONCEPTOS CLAVE APRENDIDOS:

1. CLIENTE ENVÍA → PETICIÓN GET
   └─ "Me gustaría información de usuarios"

2. SERVIDOR RESPONDE → JSON CON CÓDIGO 200
   └─ "Aquí están los datos que pediste"

3. CLIENTE RECIBE → VALIDA CON CONDICIONAL
   └─ "¿La respuesta fue exitosa?"

4. CLIENTE PROCESA → CON BUCLE FOR
   └─ "Procesar cada usuario"

5. CLIENTE VALIDA → CON CONDICIONALES
   └─ "¿Este usuario tiene todos los campos?"

6. CLIENTE IMPRIME → RESULTADO
   └─ "Mostrar el usuario procesado"

════════════════════════════════════════════════════════════════════════

✅ FLUJO TÉCNICO COMPLETO:

   requests.get(URL)
      ↓
   respuesta = objeto HTTP
      ↓
   if respuesta.status_code == 200:
      ↓
   datos = respuesta.json()
      ↓
   for elemento in datos['array']:
      ↓
   if 'campo' in elemento:
      ↓
   procesar y imprimir

════════════════════════════════════════════════════════════════════════

🎓 PRÓXIMA LECCIÓN:

   Semana 5: FUNCIONES
   ├─ Reutilizar este código en funciones
   ├─ Parámetros para diferentes URLs
   ├─ Retornar datos procesados
   └─ Modularidad en aplicaciones

════════════════════════════════════════════════════════════════════════
""")

print("=" * 70)
print("\n✅ Programa completado exitosamente")
print("👨‍🔬 Profesor: Alejandro López")
print("📚 Semana: 4 - Bucles y Condicionales")
print("🌐 Arquitectura Cliente-Servidor con APIs públicas")
print("\n" + "=" * 70 + "\n")