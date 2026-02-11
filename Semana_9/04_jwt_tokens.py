# ============================================================================
# SEMANA 9 - PARTE 4: JSON Web Tokens (JWT) - Explicación Completa
# ============================================================================
#
# JWT es un estándar para transmitir información de forma segura
# entre dos partes como un objeto JSON firmado digitalmente.
#
# SESIONES vs JWT:
# ┌──────────────────────────────────────────────────────────────────────┐
# │ SESIONES (Semana 9)              │ JWT                              │
# ├──────────────────────────────────────────────────────────────────────┤
# │ Estado en el SERVIDOR            │ Estado en el CLIENTE (token)     │
# │ Cookie con ID de sesión          │ Token completo en cada petición  │
# │ Ideal para apps web (HTML)       │ Ideal para APIs (móviles, SPAs) │
# │ El servidor "recuerda" al user   │ El servidor NO guarda nada       │
# │ Más simple de implementar        │ Más escalable                    │
# └──────────────────────────────────────────────────────────────────────┘
#
# INSTALAR: pip install PyJWT
# ============================================================================

import json
import base64
import hmac
import hashlib
import time
from datetime import datetime, timedelta

# ============================================================================
# PASO 1: ¿QUÉ ES UN JWT?
# ============================================================================

print("=" * 70)
print(" PASO 1: ¿QUÉ ES UN JWT?")
print("=" * 70)

print("""
Un JWT es una cadena de texto con TRES partes separadas por puntos:

    eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiQW5hIn0.firma_aqui
    ├──── HEADER ────┤ ├──── PAYLOAD ────┤ ├─ SIGNATURE ─┤

    HEADER    → Tipo de token y algoritmo de firma
    PAYLOAD   → Los datos (usuario, rol, expiración, etc.)
    SIGNATURE → Firma que garantiza que nadie modificó el token

Cada parte está codificada en Base64URL (legible pero NO encriptada).
""")

input(">>> Presiona Enter para continuar...\n")

# ============================================================================
# PASO 2: CONSTRUYENDO UN JWT DESDE CERO (sin librerías)
# ============================================================================

print("=" * 70)
print(" PASO 2: CONSTRUYENDO UN JWT PASO A PASO")
print("=" * 70)

# ── Función auxiliar para Base64URL ──────────────────────────────────────
def base64url_encode(data: bytes) -> str:
    """
    Codifica bytes a Base64URL (sin padding =).

    Base64URL es como Base64 pero:
    - Reemplaza + por -
    - Reemplaza / por _
    - Elimina los = del final
    """
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('utf-8')

def base64url_decode(data: str) -> bytes:
    """Decodifica Base64URL a bytes."""
    # Agregar padding que fue removido
    padding = 4 - len(data) % 4
    if padding != 4:
        data += '=' * padding
    return base64.urlsafe_b64decode(data)


# ── PARTE A: El Header ──────────────────────────────────────────────────
print("\n── A) HEADER (Encabezado) ──────────────────────────────────────")

header = {
    "alg": "HS256",   # Algoritmo: HMAC con SHA-256
    "typ": "JWT"      # Tipo: JSON Web Token
}

header_json = json.dumps(header, separators=(',', ':'))
header_b64 = base64url_encode(header_json.encode('utf-8'))

print(f"""
El HEADER indica qué algoritmo se usa para firmar:

   Header (JSON):    {header_json}
   Header (Base64):  {header_b64}

   "alg": "HS256" → Algoritmo HMAC-SHA256 (simétrico, usa una clave secreta)
   "typ": "JWT"   → Tipo de token

   NOTA: Base64 NO es encriptación. Cualquiera puede decodificarlo:
   {header_b64} → {header_json}
""")

input(">>> Presiona Enter para continuar...\n")

# ── PARTE B: El Payload ─────────────────────────────────────────────────
print("── B) PAYLOAD (Datos / Claims) ─────────────────────────────────")

ahora = int(time.time())
expiracion = ahora + 3600  # 1 hora desde ahora

payload = {
    "sub": 42,                          # Subject: ID del usuario
    "nombre": "Ana García",             # Dato personalizado
    "email": "ana@email.com",           # Dato personalizado
    "rol": "admin",                     # Dato personalizado
    "iat": ahora,                       # Issued At: cuándo se creó
    "exp": expiracion                   # Expiration: cuándo expira
}

payload_json = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
payload_b64 = base64url_encode(payload_json.encode('utf-8'))

print(f"""
El PAYLOAD contiene los DATOS (llamados "claims"):

   Payload (JSON):
   {json.dumps(payload, indent=4, ensure_ascii=False)}

   Payload (Base64):
   {payload_b64}

   CLAIMS ESTÁNDAR (registrados):
   ┌────────────────────────────────────────────────────────────────┐
   │ Claim │ Nombre         │ Descripción                          │
   ├────────────────────────────────────────────────────────────────┤
   │ sub   │ Subject        │ Identificador del usuario            │
   │ iat   │ Issued At      │ Timestamp de creación                │
   │ exp   │ Expiration     │ Timestamp de expiración              │
   │ iss   │ Issuer         │ Quién emitió el token                │
   │ aud   │ Audience       │ Para quién es el token               │
   │ nbf   │ Not Before     │ No válido antes de esta fecha        │
   └────────────────────────────────────────────────────────────────┘

   También puedes agregar claims PERSONALIZADOS:
   "nombre", "email", "rol", etc.

   IMPORTANTE: El payload es LEGIBLE (Base64 ≠ encriptación).
   ¡NUNCA pongas contraseñas o datos sensibles en el payload!

   Creado:  {datetime.fromtimestamp(ahora).strftime('%d/%m/%Y %H:%M:%S')}
   Expira:  {datetime.fromtimestamp(expiracion).strftime('%d/%m/%Y %H:%M:%S')}
""")

input(">>> Presiona Enter para continuar...\n")

# ── PARTE C: La Firma ───────────────────────────────────────────────────
print("── C) SIGNATURE (Firma) ────────────────────────────────────────")

SECRET_KEY = "mi-clave-secreta-super-segura-2024"

# La firma se calcula así:
# HMAC-SHA256(header_b64 + "." + payload_b64, SECRET_KEY)
mensaje_a_firmar = f"{header_b64}.{payload_b64}"
firma_bytes = hmac.new(
    SECRET_KEY.encode('utf-8'),
    mensaje_a_firmar.encode('utf-8'),
    hashlib.sha256
).digest()
firma_b64 = base64url_encode(firma_bytes)

print(f"""
La FIRMA garantiza que nadie modificó el header ni el payload.

   Clave secreta:  {SECRET_KEY}

   Se firma:       HMAC-SHA256(header_b64 + "." + payload_b64, clave)

   Mensaje:        {mensaje_a_firmar[:50]}...
   Firma (bytes):  {firma_bytes.hex()[:50]}...
   Firma (Base64): {firma_b64}

   ¿CÓMO PROTEGE?
   Si alguien modifica el payload (ej: cambiar rol a "admin"),
   la firma ya no coincidirá → el servidor rechaza el token.

   Solo quien tiene la SECRET_KEY puede crear firmas válidas.
""")

input(">>> Presiona Enter para continuar...\n")

# ── PARTE D: Token completo ─────────────────────────────────────────────
print("── D) TOKEN JWT COMPLETO ───────────────────────────────────────")

token = f"{header_b64}.{payload_b64}.{firma_b64}"

print(f"""
TOKEN = header.payload.firma

{token}

Desglose visual:
┌─────────────────────────────────────────────────────────────────────┐
│ HEADER (rojo)                                                       │
│ {header_b64:<67} │
├─────────────────────────────────────────────────────────────────────┤
│ PAYLOAD (azul)                                                      │
│ {payload_b64[:67]:<67} │
├─────────────────────────────────────────────────────────────────────┤
│ FIRMA (verde)                                                       │
│ {firma_b64:<67} │
└─────────────────────────────────────────────────────────────────────┘

Longitud total: {len(token)} caracteres
""")

input(">>> Presiona Enter para continuar...\n")

# ============================================================================
# PASO 3: DECODIFICANDO UN JWT (leyendo sin verificar)
# ============================================================================

print("=" * 70)
print(" PASO 3: DECODIFICANDO UN JWT")
print("=" * 70)

def decodificar_jwt(token_str):
    """
    Decodifica un JWT mostrando cada parte.
    NOTA: Esto NO verifica la firma, solo lee el contenido.
    """
    partes = token_str.split('.')
    if len(partes) != 3:
        print("   [ERROR] Token inválido: debe tener 3 partes separadas por puntos")
        return None, None, None

    header_dec = json.loads(base64url_decode(partes[0]))
    payload_dec = json.loads(base64url_decode(partes[1]))
    firma_dec = partes[2]

    return header_dec, payload_dec, firma_dec

header_dec, payload_dec, firma_dec = decodificar_jwt(token)

print(f"""
Cualquiera puede LEER un JWT (Base64 es reversible):

   HEADER decodificado:
   {json.dumps(header_dec, indent=4)}

   PAYLOAD decodificado:
   {json.dumps(payload_dec, indent=4, ensure_ascii=False)}

   FIRMA (Base64): {firma_dec}

   ¿Cuándo expira?
   Timestamp {payload_dec['exp']} → {datetime.fromtimestamp(payload_dec['exp']).strftime('%d/%m/%Y %H:%M:%S')}

   LECCIÓN: JWT NO es encriptación. Los datos son LEGIBLES.
   La firma solo garantiza INTEGRIDAD (que no fueron modificados).
""")

input(">>> Presiona Enter para continuar...\n")

# ============================================================================
# PASO 4: VERIFICANDO UN JWT (validación completa)
# ============================================================================

print("=" * 70)
print(" PASO 4: VERIFICANDO UN JWT (Validación Completa)")
print("=" * 70)

def verificar_jwt(token_str, clave_secreta):
    """
    Verifica un JWT paso a paso:
    1. Estructura correcta (3 partes)
    2. Header válido
    3. Firma válida
    4. No expirado
    """
    print("   Iniciando verificación del token...")
    print()

    # ── Paso 1: Verificar estructura ─────────────────────────────────
    partes = token_str.split('.')
    if len(partes) != 3:
        print("   [PASO 1] FALLO - El token no tiene 3 partes")
        return False

    print(f"   [PASO 1] OK - Estructura válida (3 partes separadas por '.')")

    header_parte, payload_parte, firma_parte = partes

    # ── Paso 2: Decodificar header ───────────────────────────────────
    try:
        header_json = json.loads(base64url_decode(header_parte))
        alg = header_json.get('alg', '')
        print(f"   [PASO 2] OK - Header decodificado: algoritmo = {alg}")
    except Exception as e:
        print(f"   [PASO 2] FALLO - Header no es JSON válido: {e}")
        return False

    if alg != 'HS256':
        print(f"   [PASO 2] FALLO - Algoritmo '{alg}' no soportado")
        return False

    # ── Paso 3: Decodificar payload ──────────────────────────────────
    try:
        payload_json = json.loads(base64url_decode(payload_parte))
        print(f"   [PASO 3] OK - Payload decodificado: usuario = {payload_json.get('nombre', '?')}")
    except Exception as e:
        print(f"   [PASO 3] FALLO - Payload no es JSON válido: {e}")
        return False

    # ── Paso 4: Verificar firma ──────────────────────────────────────
    mensaje = f"{header_parte}.{payload_parte}"
    firma_esperada = base64url_encode(
        hmac.new(
            clave_secreta.encode('utf-8'),
            mensaje.encode('utf-8'),
            hashlib.sha256
        ).digest()
    )

    firma_valida = hmac.compare_digest(firma_esperada, firma_parte)

    if firma_valida:
        print(f"   [PASO 4] OK - Firma válida")
        print(f"             Firma recibida:  {firma_parte[:30]}...")
        print(f"             Firma calculada: {firma_esperada[:30]}...")
    else:
        print(f"   [PASO 4] FALLO - Firma inválida")
        print(f"             Firma recibida:  {firma_parte[:30]}...")
        print(f"             Firma esperada:  {firma_esperada[:30]}...")
        print(f"             ¡Alguien modificó el token!")
        return False

    # ── Paso 5: Verificar expiración ─────────────────────────────────
    exp = payload_json.get('exp')
    if exp:
        ahora = int(time.time())
        if ahora > exp:
            vencido_hace = ahora - exp
            print(f"   [PASO 5] FALLO - Token expirado hace {vencido_hace} segundos")
            return False
        else:
            resta = exp - ahora
            minutos = resta // 60
            print(f"   [PASO 5] OK - Token válido por {minutos} minutos más")
    else:
        print(f"   [PASO 5] OK - Sin expiración (token permanente)")

    print()
    print("   ========================================")
    print("   TOKEN VÁLIDO - Autenticación exitosa")
    print("   ========================================")
    return True

# Verificar nuestro token
verificar_jwt(token, SECRET_KEY)

input("\n>>> Presiona Enter para continuar...\n")

# ============================================================================
# PASO 5: ¿QUÉ PASA SI MODIFICAN EL TOKEN?
# ============================================================================

print("=" * 70)
print(" PASO 5: ¿QUÉ PASA SI ALGUIEN MODIFICA EL TOKEN?")
print("=" * 70)

# ── Ataque 1: Modificar el payload (cambiar rol) ────────────────────────
print("\n── ATAQUE 1: Cambiar el rol de 'admin' a 'superadmin' ─────────")
print()

# Un atacante decodifica el payload y lo modifica
payload_malicioso = payload.copy()
payload_malicioso['rol'] = 'superadmin'
payload_malicioso['nombre'] = 'Hacker Malvado'

payload_mal_json = json.dumps(payload_malicioso, separators=(',', ':'), ensure_ascii=False)
payload_mal_b64 = base64url_encode(payload_mal_json.encode('utf-8'))

# El atacante reemplaza el payload pero NO puede recalcular la firma
# porque no conoce la SECRET_KEY
token_modificado = f"{header_b64}.{payload_mal_b64}.{firma_b64}"

print(f"   Token original:   ...{token[50:80]}...")
print(f"   Token modificado: ...{token_modificado[50:80]}...")
print(f"   (El atacante cambió el payload pero dejó la firma original)")
print()

verificar_jwt(token_modificado, SECRET_KEY)

input("\n>>> Presiona Enter para continuar...\n")

# ── Ataque 2: Modificar un solo carácter ─────────────────────────────────
print("── ATAQUE 2: Cambiar UN SOLO carácter del payload ──────────────")
print()

# Cambiar solo 1 carácter en el payload codificado
token_partes = token.split('.')
payload_alterado = token_partes[1]
# Cambiar el último carácter
if payload_alterado[-1] == 'A':
    payload_alterado = payload_alterado[:-1] + 'B'
else:
    payload_alterado = payload_alterado[:-1] + 'A'

token_1_char = f"{token_partes[0]}.{payload_alterado}.{token_partes[2]}"

print(f"   Payload original:  ...{token_partes[1][-20:]}")
print(f"   Payload alterado:  ...{payload_alterado[-20:]}")
print(f"   (Solo 1 carácter diferente)")
print()

verificar_jwt(token_1_char, SECRET_KEY)

input("\n>>> Presiona Enter para continuar...\n")

# ── Ataque 3: Usar una clave secreta diferente ──────────────────────────
print("── ATAQUE 3: Firmar con una clave secreta diferente ────────────")
print()

# El atacante crea su propio token con SU clave
clave_atacante = "clave-del-atacante"
payload_atacante = {
    "sub": 1,
    "nombre": "Atacante",
    "rol": "admin",
    "iat": int(time.time()),
    "exp": int(time.time()) + 3600
}

h_b64 = base64url_encode(json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(',', ':')).encode())
p_b64 = base64url_encode(json.dumps(payload_atacante, separators=(',', ':'), ensure_ascii=False).encode())
f_bytes = hmac.new(clave_atacante.encode(), f"{h_b64}.{p_b64}".encode(), hashlib.sha256).digest()
f_b64 = base64url_encode(f_bytes)
token_atacante = f"{h_b64}.{p_b64}.{f_b64}"

print(f"   Clave del atacante:  {clave_atacante}")
print(f"   Clave del servidor:  {SECRET_KEY}")
print(f"   Token del atacante:  {token_atacante[:60]}...")
print()

verificar_jwt(token_atacante, SECRET_KEY)

input("\n>>> Presiona Enter para continuar...\n")

# ============================================================================
# PASO 6: TOKEN EXPIRADO
# ============================================================================

print("=" * 70)
print(" PASO 6: TOKEN EXPIRADO")
print("=" * 70)
print()

# Crear un token que ya expiró (expiración en el pasado)
payload_expirado = {
    "sub": 42,
    "nombre": "Ana García",
    "rol": "admin",
    "iat": int(time.time()) - 7200,     # Creado hace 2 horas
    "exp": int(time.time()) - 3600      # Expiró hace 1 hora
}

p_exp_json = json.dumps(payload_expirado, separators=(',', ':'), ensure_ascii=False)
p_exp_b64 = base64url_encode(p_exp_json.encode())
msg_exp = f"{header_b64}.{p_exp_b64}"
f_exp = base64url_encode(hmac.new(SECRET_KEY.encode(), msg_exp.encode(), hashlib.sha256).digest())
token_expirado = f"{header_b64}.{p_exp_b64}.{f_exp}"

print(f"   Token creado hace 2 horas, expiró hace 1 hora")
print()

verificar_jwt(token_expirado, SECRET_KEY)

input("\n>>> Presiona Enter para continuar...\n")

# ============================================================================
# PASO 7: USANDO LA LIBRERÍA PyJWT (forma profesional)
# ============================================================================

print("=" * 70)
print(" PASO 7: USANDO PyJWT (forma profesional)")
print("=" * 70)

try:
    import jwt  # pip install PyJWT

    print("\n   PyJWT está instalado. Veamos cómo se usa:\n")

    # ── Crear token ──────────────────────────────────────────────────
    clave = "mi-clave-secreta-para-jwt"

    payload_pro = {
        "sub": 42,
        "nombre": "Ana García",
        "email": "ana@email.com",
        "rol": "admin",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token_pro = jwt.encode(payload_pro, clave, algorithm="HS256")
    print(f"   Token creado con PyJWT:")
    print(f"   {token_pro[:70]}...")

    # ── Decodificar token ────────────────────────────────────────────
    datos = jwt.decode(token_pro, clave, algorithms=["HS256"])
    print(f"\n   Token decodificado:")
    for k, v in datos.items():
        print(f"     {k}: {v}")

    # ── Token expirado ───────────────────────────────────────────────
    print(f"\n   Probando token expirado...")
    payload_viejo = {
        "sub": 42,
        "exp": datetime.utcnow() - timedelta(hours=1)
    }
    token_viejo = jwt.encode(payload_viejo, clave, algorithm="HS256")
    try:
        jwt.decode(token_viejo, clave, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        print(f"   [OK] PyJWT lanza ExpiredSignatureError automáticamente")

    # ── Token con firma inválida ─────────────────────────────────────
    print(f"\n   Probando token con clave incorrecta...")
    try:
        jwt.decode(token_pro, "clave-incorrecta", algorithms=["HS256"])
    except jwt.InvalidSignatureError:
        print(f"   [OK] PyJWT lanza InvalidSignatureError automáticamente")

    print(f"""
   CÓDIGO COMPLETO PARA USAR EN TU APP:
   ─────────────────────────────────────

   import jwt
   from datetime import datetime, timedelta

   SECRET_KEY = "tu-clave-secreta"

   # CREAR TOKEN (al hacer login):
   def crear_token(usuario_id, nombre, rol):
       payload = {{
           "sub": usuario_id,
           "nombre": nombre,
           "rol": rol,
           "iat": datetime.utcnow(),
           "exp": datetime.utcnow() + timedelta(hours=24)
       }}
       return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

   # VERIFICAR TOKEN (en cada petición):
   def verificar_token(token):
       try:
           datos = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
           return datos  # Contiene sub, nombre, rol, etc.
       except jwt.ExpiredSignatureError:
           return None  # Token expirado
       except jwt.InvalidTokenError:
           return None  # Token inválido
""")

except ImportError:
    print("""
   PyJWT NO está instalado.

   Para instalarlo:
     pip install PyJWT

   Arriba viste cómo funciona JWT internamente (sin librerías).
   PyJWT hace todo eso automáticamente con 2 líneas de código:

     import jwt

     # Crear token
     token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

     # Verificar token
     datos = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
""")

input(">>> Presiona Enter para continuar...\n")

# ============================================================================
# PASO 8: FLUJO COMPLETO EN UNA API
# ============================================================================

print("=" * 70)
print(" PASO 8: FLUJO COMPLETO - JWT EN UNA API REST")
print("=" * 70)

print("""
Así funciona JWT en una aplicación real (API REST):

┌─────────────┐                           ┌─────────────┐
│   CLIENTE   │                           │  SERVIDOR   │
│ (App móvil, │                           │  (API Flask) │
│  Frontend)  │                           │             │
└──────┬──────┘                           └──────┬──────┘
       │                                         │
       │  1. POST /api/login                     │
       │     {"email": "ana@mail.com",           │
       │      "password": "secreto123"}          │
       │ ──────────────────────────────────────► │
       │                                         │
       │                         2. Buscar usuario en BD
       │                         3. Verificar password (hash)
       │                         4. Crear JWT con los datos
       │                                         │
       │  5. {"token": "eyJhbGci..."}           │
       │ ◄────────────────────────────────────── │
       │                                         │
       │  6. El cliente GUARDA el token          │
       │     (localStorage, SecureStorage, etc.)  │
       │                                         │
       │  7. GET /api/productos                  │
       │     Authorization: Bearer eyJhbGci...   │
       │ ──────────────────────────────────────► │
       │                                         │
       │                         8. Extraer token del header
       │                         9. Verificar firma (SECRET_KEY)
       │                        10. Verificar expiración
       │                        11. Extraer usuario del payload
       │                        12. Ejecutar la lógica
       │                                         │
       │  13. {"productos": [...]}               │
       │ ◄────────────────────────────────────── │
       │                                         │
       │                                         │
       │  === SI EL TOKEN EXPIRA ===             │
       │                                         │
       │  14. GET /api/productos                 │
       │      Authorization: Bearer eyJ(expirado)│
       │ ──────────────────────────────────────► │
       │                                         │
       │                        15. Token expirado
       │                                         │
       │  16. {"error": "Token expirado"}        │
       │      Status: 401 Unauthorized           │
       │ ◄────────────────────────────────────── │
       │                                         │
       │  17. El cliente redirige al login       │
       │                                         │


HEADER HTTP:
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJz...

   "Bearer" es el tipo de autenticación.
   Lo que sigue después del espacio es el token JWT.
""")

input(">>> Presiona Enter para ver el resumen final...\n")

# ============================================================================
# RESUMEN FINAL
# ============================================================================

print("=" * 70)
print(" RESUMEN: TODO SOBRE JWT")
print("=" * 70)

print("""
┌──────────────────────────────────────────────────────────────────────┐
│                        ESTRUCTURA JWT                                │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  HEADER.PAYLOAD.SIGNATURE                                            │
│                                                                      │
│  HEADER:    {"alg": "HS256", "typ": "JWT"}                          │
│             Algoritmo + tipo (siempre igual)                         │
│                                                                      │
│  PAYLOAD:   {"sub": 42, "nombre": "Ana", "exp": 1234567890}        │
│             Datos del usuario + expiración                           │
│             ¡NO poner contraseñas aquí! (es legible)                │
│                                                                      │
│  SIGNATURE: HMAC-SHA256(header + "." + payload, SECRET_KEY)         │
│             Garantiza que nadie modificó nada                        │
│             Solo se puede crear con la clave secreta                │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                     SEGURIDAD                                        │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Si modifican el PAYLOAD → la firma no coincide → RECHAZADO         │
│  Si modifican la FIRMA   → no coincide con el cálculo → RECHAZADO  │
│  Si el token EXPIRÓ      → timestamp > exp → RECHAZADO              │
│  Si usan OTRA CLAVE      → firma diferente → RECHAZADO              │
│                                                                      │
│  SOLO un token creado con la SECRET_KEY correcta                    │
│  y que NO haya expirado será aceptado.                              │
│                                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                  SESIONES vs JWT                                     │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  SESIONES (nuestra app web):                                        │
│  - Estado en el servidor (BD o memoria)                             │
│  - Cookie con session_id                                            │
│  - Ideal para: apps web con HTML/templates                          │
│  - Ventaja: fácil de invalidar (borrar sesión del servidor)         │
│                                                                      │
│  JWT (APIs REST):                                                    │
│  - Estado en el cliente (el token tiene todo)                       │
│  - Header Authorization: Bearer <token>                             │
│  - Ideal para: APIs, apps móviles, microservicios                   │
│  - Ventaja: no necesita estado en el servidor (escalable)           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

¿CUÁNDO USAR CADA UNO?

   App web tradicional (Flask + templates)  → SESIONES (lo que usamos)
   API REST (Flask + JSON)                  → JWT
   App móvil consumiendo API                → JWT
   Microservicios comunicándose             → JWT
   Single Page App (React, Vue)             → JWT
""")

print("=" * 70)
print(" FIN DE LA EXPLICACIÓN DE JWT")
print("=" * 70)
