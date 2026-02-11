# ============================================================================
# SEMANA 9 - PARTE 1: Introducción a la Autenticación
# ============================================================================
#
# La AUTENTICACIÓN es el proceso de verificar la identidad de un usuario.
# Es decir: "¿Eres realmente quien dices ser?"
#
# No confundir con AUTORIZACIÓN, que es: "¿Tienes permiso para hacer esto?"
#
# AUTENTICACIÓN → ¿Quién eres?
# AUTORIZACIÓN  → ¿Qué puedes hacer?
#
# ============================================================================

# ============================================================================
# 1. ¿POR QUÉ ES IMPORTANTE?
# ============================================================================
#
# Sin autenticación, cualquier persona podría:
# - Ver datos privados de otros usuarios
# - Modificar o eliminar información
# - Hacerse pasar por otra persona
# - Acceder a funciones de administrador
#
# ============================================================================

# ============================================================================
# 2. MÉTODOS COMUNES DE AUTENTICACIÓN
# ============================================================================
#
# ┌──────────────────────────────────────────────────────────────────────┐
# │ MÉTODO              │ DESCRIPCIÓN                                    │
# ├──────────────────────────────────────────────────────────────────────┤
# │ Usuario + Contraseña│ El más básico y común                         │
# │ OAuth (Google, etc.)│ "Iniciar sesión con Google"                   │
# │ Tokens (JWT)        │ Token enviado en cada petición (APIs)         │
# │ Sesiones (Cookies)  │ Cookie que identifica al usuario ← USAMOS    │
# │ API Keys            │ Clave única para acceso programático          │
# │ Biométrico          │ Huella digital, reconocimiento facial         │
# │ 2FA                 │ Verificación en dos pasos                     │
# └──────────────────────────────────────────────────────────────────────┘
#
# En este curso usamos SESIONES CON COOKIES, que es lo más común
# en aplicaciones web tradicionales (no APIs).
# ============================================================================

# ============================================================================
# 3. FLUJO DE AUTENTICACIÓN CON SESIONES
# ============================================================================
#
# ┌─────────────┐                         ┌─────────────┐
# │  NAVEGADOR  │                         │  SERVIDOR   │
# └──────┬──────┘                         └──────┬──────┘
#        │                                       │
#        │  1. POST /login                       │
#        │     email: "user@mail.com"             │
#        │     password: "secreto123"             │
#        │ ───────────────────────────────────►   │
#        │                                       │
#        │                          2. Buscar usuario en BD
#        │                          3. Verificar password hash
#        │                          4. Crear sesión
#        │                                       │
#        │  5. Set-Cookie: session=abc123        │
#        │  ◄───────────────────────────────────  │
#        │                                       │
#        │  6. GET /productos                    │
#        │     Cookie: session=abc123            │
#        │ ───────────────────────────────────►   │
#        │                                       │
#        │                          7. Verificar sesión
#        │                          8. Obtener usuario
#        │                                       │
#        │  9. HTML con datos                    │
#        │  ◄───────────────────────────────────  │
#        │                                       │
#
# ============================================================================

# ============================================================================
# 4. ¿QUÉ PASA CON LAS CONTRASEÑAS?
# ============================================================================
#
# REGLA DE ORO: NUNCA guardar contraseñas en texto plano.
#
# ❌ INCORRECTO (texto plano):
#    password = "mi_contraseña"
#    → Si alguien accede a la BD, ve TODAS las contraseñas
#
# ✅ CORRECTO (hash):
#    password_hash = "pbkdf2:sha256:260000$abc..."
#    → Incluso si acceden a la BD, no pueden saber la contraseña
#
# ¿Qué es un HASH?
# Es una función matemática que convierte texto en una cadena irreversible:
#
#    "hola123"   → "pbkdf2:sha256:260000$Xt2..."
#    "hola124"   → "pbkdf2:sha256:260000$Jk9..."  ← Totalmente diferente
#
# Propiedades del hash:
# 1. Es IRREVERSIBLE: no se puede obtener "hola123" desde el hash
# 2. Es DETERMINÍSTICO: el mismo input siempre da el mismo output
# 3. EFECTO AVALANCHA: un cambio pequeño cambia todo el hash
# 4. Incluye SAL (salt): valor aleatorio que hace cada hash único
#
# ============================================================================

print("=" * 60)
print("DEMOSTRACIÓN: Autenticación con Python")
print("=" * 60)

# Importamos las funciones de hashing de werkzeug
# (viene incluido con Flask, no necesitas instalar nada extra)
from werkzeug.security import generate_password_hash, check_password_hash

# ── Ejemplo 1: Hashear una contraseña ────────────────────────────────────
print("\n1. HASHEAR CONTRASEÑAS")
print("-" * 40)

password = "mi_password_seguro"
hash_resultado = generate_password_hash(password)

print(f"   Contraseña original: {password}")
print(f"   Hash generado:       {hash_resultado}")
print(f"   Longitud del hash:   {len(hash_resultado)} caracteres")

# ── Ejemplo 2: Cada hash es diferente (por la sal) ──────────────────────
print("\n2. CADA HASH ES ÚNICO (por la sal)")
print("-" * 40)

hash1 = generate_password_hash("hola123")
hash2 = generate_password_hash("hola123")

print(f"   Hash 1: {hash1[:50]}...")
print(f"   Hash 2: {hash2[:50]}...")
print(f"   ¿Son iguales? {hash1 == hash2}")  # False!
print(f"   (Ambos son válidos para 'hola123', pero son diferentes)")

# ── Ejemplo 3: Verificar una contraseña ──────────────────────────────────
print("\n3. VERIFICAR CONTRASEÑAS")
print("-" * 40)

password_correcta = "hola123"
password_incorrecta = "hola124"

# Simulamos guardar el hash en la base de datos
hash_guardado = generate_password_hash(password_correcta)

# Verificamos
resultado1 = check_password_hash(hash_guardado, password_correcta)
resultado2 = check_password_hash(hash_guardado, password_incorrecta)

print(f"   Hash guardado: {hash_guardado[:50]}...")
print(f"   ¿'hola123' es correcta? {resultado1}")   # True
print(f"   ¿'hola124' es correcta? {resultado2}")   # False

# ── Ejemplo 4: Simulación de registro y login ───────────────────────────
print("\n4. SIMULACIÓN: REGISTRO Y LOGIN")
print("-" * 40)

# Simulamos una "base de datos" con un diccionario
base_de_datos = {}

def registrar_usuario(email, password):
    """Registra un usuario con su contraseña hasheada."""
    if email in base_de_datos:
        print(f"   [ERROR] El email {email} ya está registrado")
        return False

    hash_password = generate_password_hash(password)
    base_de_datos[email] = {
        'email': email,
        'password_hash': hash_password
    }
    print(f"   [OK] Usuario {email} registrado")
    return True

def login(email, password):
    """Intenta iniciar sesión."""
    usuario = base_de_datos.get(email)

    if not usuario:
        print(f"   [ERROR] Email o contraseña incorrectos")
        return False

    if check_password_hash(usuario['password_hash'], password):
        print(f"   [OK] ¡Bienvenido, {email}!")
        return True
    else:
        print(f"   [ERROR] Email o contraseña incorrectos")
        return False

# Registrar usuarios
registrar_usuario("ana@mail.com", "ana_segura123")
registrar_usuario("pedro@mail.com", "pedro_pass456")

# Intentar login
print()
login("ana@mail.com", "ana_segura123")        # OK
login("ana@mail.com", "contraseña_mala")       # ERROR
login("noexiste@mail.com", "algo")             # ERROR

# ── Ejemplo 5: Buenas prácticas ─────────────────────────────────────────
print("\n5. BUENAS PRÁCTICAS DE SEGURIDAD")
print("-" * 40)
print("""
   1. NUNCA guardar contraseñas en texto plano
   2. Usar algoritmos probados (bcrypt, scrypt, pbkdf2)
   3. Usar mensajes genéricos de error:
      ✅ "Email o contraseña incorrectos"
      ❌ "El email no existe" (da info al atacante)
   4. Mínimo 6-8 caracteres en contraseñas
   5. Limitar intentos de login (rate limiting)
   6. Usar HTTPS en producción
   7. Renovar el secret_key en producción
""")

print("=" * 60)
print("FIN DE LA DEMOSTRACIÓN")
print("=" * 60)
