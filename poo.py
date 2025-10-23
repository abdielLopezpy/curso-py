"""
=================================================================
PROGRAMACIÓN ORIENTADA A OBJETOS (POO) EN PYTHON - NIVEL BÁSICO
Guía simple y comentada para principiantes
=================================================================

¿QUÉ ES LA POO?
Es una forma de programar donde agrupamos datos y funciones relacionadas
en "objetos". Es como crear moldes (clases) para hacer cosas (objetos).

EJEMPLO DEL MUNDO REAL:
- Clase = Molde para hacer galletas (la receta)
- Objeto = Cada galleta que haces con ese molde
"""

# =================================================================
# 1. MI PRIMERA CLASE - CONCEPTO BÁSICO
# =================================================================

print("=" * 50)
print("1. CREANDO MI PRIMERA CLASE")
print("=" * 50)

# Una CLASE es como un molde o plantilla
# Define QUÉ información tendrá y QUÉ puede hacer
class Usuario:
    """
    Esto es una clase llamada Usuario.
    Una clase es como un molde para crear objetos.
    Representa a un usuario de una aplicación web.
    """
    
    # El método __init__ es el CONSTRUCTOR
    # Se ejecuta automáticamente cuando creas un nuevo usuario
    def __init__(self, nombre, email, edad):
        """
        __init__ = inicializar
        self = se refiere al objeto que estamos creando
        nombre y email = información que recibimos al crear el usuario
        """
        # self.nombre crea una variable que pertenece a este usuario
        self.nombre = nombre    # Guardamos el nombre del usuario
        self.email = email      # Guardamos el email del usuario
        self.edad = edad        # Guardamos la edad del usuario
        self.activo = True      # Por defecto el usuario está activo
    
    # Un MÉTODO es una función que pertenece a la clase
    # Define QUÉ puede hacer el objeto
    def activar(self):
        """
        Este es un método (función de la clase).
        Activa la cuenta del usuario.
        """
        # Usamos self.activo para cambiar el estado de este usuario específico
        self.activo = True
        return f"Usuario {self.nombre} ha sido activado"
    
    def desactivar(self):
        """
        Este método desactiva la cuenta del usuario.
        Útil cuando un usuario se da de baja o es suspendido.
        """
        self.activo = False  # Cambiamos el estado a False (inactivo)
        return f"Usuario {self.nombre} ha sido desactivado"
    
    def cambiar_email(self, nuevo_email):
        """
        Permite cambiar el email del usuario.
        nuevo_email = el nuevo correo que queremos asignar
        """
        email_anterior = self.email  # Guardamos el email viejo
        self.email = nuevo_email     # Asignamos el nuevo email
        return f"Email cambiado de {email_anterior} a {self.email}"

# CREAR OBJETOS (instancias) de la clase Usuario
# Cada objeto es un usuario diferente creado con el mismo molde
usuario1 = Usuario("María López", "maria@email.com", 20)      # Creamos usuario 1
usuario2 = Usuario("Juan Pérez", "juan@email.com", 25)        # Creamos usuario 2

# Acceder a los ATRIBUTOS (variables) del objeto
print(f"\nUsuario 1: {usuario1.nombre}")
print(f"Email: {usuario1.email}")
print(f"Edad: {usuario1.edad}")
print(f"¿Está activo? {usuario1.activo}")

print(f"\nUsuario 2: {usuario2.nombre}")
print(f"Email: {usuario2.email}")
print(f"Edad: {usuario2.edad}")
print(f"¿Está activo? {usuario2.activo}")

# Llamar a los MÉTODOS (funciones) del objeto
print(f"\n{usuario1.desactivar()}")       # Desactivamos a María
print(f"\n{usuario2.desactivar()}")
print(f"\n{usuario2.activar()}")         # Activamos a Juan


print(f"¿Está activo ahora? {usuario1.activo}")

print(f"\n{usuario2.cambiar_email('juanperez@gmail.com')}")  # Juan cambia su email


# =================================================================
# 2. CLASE CON MÁS FUNCIONALIDAD - EJEMPLO PRÁCTICO
# =================================================================

print("\n" + "=" * 50)
print("2. CLASE CON MÁS FUNCIONALIDAD")
print("=" * 50)

class Estudiante:
    """
    Clase que representa a un estudiante.
    Guarda su información y puede calcular su promedio.
    """
    
    def __init__(self, nombre, edad):
        """
        Constructor: crea un nuevo estudiante.
        Inicializa sus datos básicos y una lista vacía de notas.
        """
        self.nombre = nombre           # Nombre del estudiante
        self.edad = edad               # Edad del estudiante
        self.notas = []                # Lista vacía para guardar notas
    
    def agregar_nota(self, nota):
        """
        Método para agregar una nota a la lista de notas.
        nota = número que representa la calificación
        """
        # Validamos que la nota esté entre 0 y 100
        if 0 <= nota <= 100:
            self.notas.append(nota)    # append agrega al final de la lista
            return f"Nota {nota} agregada a {self.nombre}"
        else:
            return "La nota debe estar entre 0 y 100"
    
    def calcular_promedio(self):
        """
        Calcula el promedio de todas las notas.
        Retorna 0 si no hay notas.
        """
        # Si la lista de notas está vacía, retorna 0
        if len(self.notas) == 0:
            return 0
        
        # sum() suma todos los números de la lista
        # len() cuenta cuántos elementos hay en la lista
        promedio = sum(self.notas) / len(self.notas)
        return promedio
    
    def mostrar_info(self):
        """
        Muestra toda la información del estudiante.
        """
        info = f"\n--- Información del Estudiante ---"
        info += f"\nNombre: {self.nombre}"
        info += f"\nEdad: {self.edad}"
        info += f"\nNotas: {self.notas}"
        info += f"\nPromedio: {self.calcular_promedio():.2f}"
        return info

# Crear un estudiante
estudiante1 = Estudiante("Ana García", 20)

# Agregar varias notas
print(estudiante1.agregar_nota(85))
print(estudiante1.agregar_nota(90))
print(estudiante1.agregar_nota(78))

# Mostrar información completa
print(estudiante1.mostrar_info())


# =================================================================
# 3. HERENCIA - REUTILIZAR CÓDIGO
# =================================================================

print("\n" + "=" * 50)
print("3. HERENCIA - CREAR CLASES A PARTIR DE OTRAS")
print("=" * 50)

# Clase PADRE (también llamada clase base o superclase)
class Persona:
    """
    Clase padre con información básica de una persona.
    Otras clases pueden HEREDAR de esta.
    """
    
    def __init__(self, nombre, edad):
        """
        Constructor de la clase Persona.
        """
        self.nombre = nombre
        self.edad = edad
    
    def saludar(self):
        """
        Método que todas las personas pueden usar.
        """
        return f"Hola, soy {self.nombre}"
    
    def mostrar_edad(self):
        """
        Método para mostrar la edad.
        """
        return f"Tengo {self.edad} años"

# Clase HIJA (también llamada clase derivada o subclase)
# La palabra "Persona" entre paréntesis significa que hereda de Persona
class Profesor(Persona):
    """
    Clase hija que HEREDA de Persona.
    Tiene todo lo de Persona + información adicional.
    """
    
    def __init__(self, nombre, edad, materia):
        """
        Constructor de la clase Profesor.
        """
        # super() llama al constructor de la clase PADRE (Persona)
        # Esto inicializa nombre y edad usando el código de Persona
        super().__init__(nombre, edad)
        
        # Agregamos un atributo adicional solo para profesores
        self.materia = materia
    
    def enseñar(self):
        """
        Método EXCLUSIVO de la clase Profesor.
        La clase Persona NO tiene este método.
        """
        return f"Estoy enseñando {self.materia}"

# Crear un objeto Profesor
profesor1 = Profesor("Carlos López", 35, "Matemáticas")

# El profesor puede usar métodos de Persona (heredados)
print(profesor1.saludar())           # Método heredado de Persona
print(profesor1.mostrar_edad())      # Método heredado de Persona

# Y también sus propios métodos
print(profesor1.enseñar())           # Método propio de Profesor
print(f"Materia: {profesor1.materia}")  # Atributo propio de Profesor


# =================================================================
# 4. EJEMPLO PRÁCTICO COMPLETO - SISTEMA SIMPLE
# =================================================================

print("\n" + "=" * 50)
print("4. EJEMPLO COMPLETO - SISTEMA DE PRODUCTOS")
print("=" * 50)

class Producto:
    """
    Clase que representa un producto en una tienda.
    Guarda información del producto y puede calcular descuentos.
    """
    
    def __init__(self, nombre, precio, cantidad):
        """
        Constructor: crea un nuevo producto.
        """
        self.nombre = nombre         # Nombre del producto
        self.precio = precio         # Precio unitario
        self.cantidad = cantidad     # Cantidad en stock
    
    def aplicar_descuento(self, porcentaje):
        """
        Aplica un descuento al precio del producto.
        porcentaje = número del 0 al 100
        Ejemplo: 20 significa 20% de descuento
        """
        # Calculamos el descuento
        descuento = self.precio * (porcentaje / 100)
        
        # Restamos el descuento al precio
        self.precio = self.precio - descuento
        
        return f"Descuento aplicado. Nuevo precio: ${self.precio:.2f}"
    
    def vender(self, cantidad_vendida):
        """
        Vende una cantidad de productos.
        Reduce el stock disponible.
        """
        # Verificamos si hay suficiente stock
        if cantidad_vendida > self.cantidad:
            return f"No hay suficiente stock. Solo tenemos {self.cantidad}"
        
        # Restamos la cantidad vendida del stock
        self.cantidad -= cantidad_vendida
        
        # Calculamos el total de la venta
        total = cantidad_vendida * self.precio
        
        return f"Venta exitosa. Total: ${total:.2f}. Stock restante: {self.cantidad}"
    
    def mostrar_info(self):
        """
        Muestra toda la información del producto.
        """
        print(f"\n--- Producto ---")
        print(f"Nombre: {self.nombre}")
        print(f"Precio: ${self.precio:.2f}")
        print(f"Stock: {self.cantidad} unidades")

# Crear productos
producto1 = Producto("Laptop", 800, 10)
producto2 = Producto("Mouse", 25, 50)

# Mostrar información inicial
producto1.mostrar_info()

# Aplicar descuento del 10%
print(producto1.aplicar_descuento(10))

# Vender algunas unidades
print(producto1.vender(3))

# Mostrar información actualizada
producto1.mostrar_info()


# =================================================================
# 5. LISTA DE OBJETOS - TRABAJANDO CON MÚLTIPLES OBJETOS
# =================================================================

print("\n" + "=" * 50)
print("5. TRABAJANDO CON MÚLTIPLES OBJETOS")
print("=" * 50)

class Tarea:
    """
    Clase simple para representar una tarea.
    """
    
    def __init__(self, descripcion):
        """
        Constructor: crea una nueva tarea.
        """
        self.descripcion = descripcion    # Descripción de la tarea
        self.completada = False           # Por defecto no está completada
    
    def completar(self):
        """
        Marca la tarea como completada.
        """
        self.completada = True
        return f"Tarea '{self.descripcion}' completada ✓"
    
    def __str__(self):
        """
        Método especial __str__
        Define cómo se ve el objeto cuando lo imprimimos.
        """
        # Operador ternario: valor_si_true if condición else valor_si_false
        estado = "✓ Completada" if self.completada else "○ Pendiente"
        return f"{estado}: {self.descripcion}"

# Crear una LISTA de objetos Tarea
lista_tareas = [
    Tarea("Estudiar Python"),
    Tarea("Hacer ejercicio"),
    Tarea("Leer documentación"),
]

print("\n--- Lista de Tareas ---")
# Recorrer la lista e imprimir cada tarea
for tarea in lista_tareas:
    print(tarea)  # Llama automáticamente al método __str__

# Completar la primera tarea
print(f"\n{lista_tareas[0].completar()}")

print("\n--- Lista Actualizada ---")
# Mostrar la lista actualizada
for tarea in lista_tareas:
    print(tarea)


# =================================================================
# 6. PRINCIPIOS DE POO - EXPLICADOS CON CASOS DE USO
# =================================================================

print("\n" + "=" * 50)
print("6. PRINCIPIOS FUNDAMENTALES DE POO")
print("=" * 50)

print("\n--- PRINCIPIO 1: ENCAPSULAMIENTO ---")
print("Ocultar datos internos y solo exponer lo necesario")

class CuentaBancaria:
    """
    ENCAPSULAMIENTO: Proteger datos sensibles.
    
    CASO DE USO REAL: Sistema bancario
    - No queremos que alguien cambie el saldo directamente
    - Solo permitimos cambios a través de métodos controlados
    - Así evitamos fraudes o errores
    """
    
    def __init__(self, titular, saldo_inicial):
        """
        Constructor de la cuenta bancaria.
        """
        self.titular = titular                    # Público: cualquiera puede ver el titular
        self.__saldo = saldo_inicial              # Privado: __ hace que sea inaccesible desde fuera
        self.__historial = []                     # Privado: guardamos el historial de transacciones
    
    def depositar(self, cantidad):
        """
        Método PÚBLICO para depositar dinero.
        Solo se puede modificar el saldo a través de este método.
        """
        if cantidad > 0:
            self.__saldo += cantidad              # Modificamos el saldo privado
            self.__historial.append(f"+${cantidad}")  # Registramos en el historial
            return f"Depósito exitoso: ${cantidad}. Saldo: ${self.__saldo}"
        return "La cantidad debe ser positiva"
    
    def retirar(self, cantidad):
        """
        Método PÚBLICO para retirar dinero.
        Incluye validación de negocio (no puede retirar más de lo que tiene).
        """
        if cantidad > self.__saldo:
            return "❌ Fondos insuficientes"
        if cantidad > 0:
            self.__saldo -= cantidad
            self.__historial.append(f"-${cantidad}")
            return f"Retiro exitoso: ${cantidad}. Saldo: ${self.__saldo}"
        return "La cantidad debe ser positiva"
    
    def consultar_saldo(self):
        """
        Método PÚBLICO para ver el saldo de forma segura.
        """
        return f"Saldo actual: ${self.__saldo}"
    
    def ver_historial(self):
        """
        Método PÚBLICO para ver el historial.
        """
        return f"Historial: {', '.join(self.__historial)}"

# Probar el encapsulamiento
cuenta = CuentaBancaria("Pedro Gómez", 1000)
print(f"\n{cuenta.titular} - {cuenta.consultar_saldo()}")
print(cuenta.depositar(500))
print(cuenta.retirar(200))
print(cuenta.ver_historial())

# Intentar acceder al saldo privado directamente (NO funciona)
# print(cuenta.__saldo)  # Esto daría ERROR ❌


print("\n--- PRINCIPIO 2: ABSTRACCIÓN ---")
print("Mostrar solo lo esencial, ocultar la complejidad")

class ServicioEmail:
    """
    ABSTRACCIÓN: Simplificar operaciones complejas.
    
    CASO DE USO REAL: Sistema de notificaciones
    - El usuario solo llama a enviar()
    - No necesita saber cómo funciona el servidor SMTP
    - La complejidad está oculta dentro de la clase
    """
    
    def __init__(self, servidor, puerto):
        """
        Constructor con configuración del servidor de email.
        """
        self.servidor = servidor
        self.puerto = puerto
    
    def __conectar_servidor(self):
        """
        Método PRIVADO (por convención con __).
        El usuario NO necesita llamar esto directamente.
        """
        return f"[Conectando a {self.servidor}:{self.puerto}...]"
    
    def __autenticar(self):
        """
        Método PRIVADO para autenticación.
        Complejidad oculta.
        """
        return "[Autenticando usuario...]"
    
    def __preparar_mensaje(self, destinatario, asunto, cuerpo):
        """
        Método PRIVADO para formatear el mensaje.
        """
        return f"Para: {destinatario}\nAsunto: {asunto}\n\n{cuerpo}"
    
    def enviar(self, destinatario, asunto, cuerpo):
        """
        Método PÚBLICO simple.
        Oculta toda la complejidad de enviar un email.
        El usuario solo necesita llamar este método.
        """
        # Aquí se llaman todos los métodos privados automáticamente
        print(self.__conectar_servidor())
        print(self.__autenticar())
        mensaje = self.__preparar_mensaje(destinatario, asunto, cuerpo)
        print(f"[Enviando mensaje...]\n{mensaje}")
        return "✓ Email enviado exitosamente"

# Usar el servicio (muy simple desde afuera)
email_service = ServicioEmail("smtp.gmail.com", 587)
resultado = email_service.enviar(
    "cliente@example.com",
    "Bienvenida",
    "Gracias por registrarte en nuestra plataforma"
)
print(resultado)


print("\n--- PRINCIPIO 3: HERENCIA ---")
print("Reutilizar código creando clases especializadas")

class EmpleadoBase:
    """
    HERENCIA: Clase base con funcionalidad común.
    
    CASO DE USO REAL: Sistema de recursos humanos
    - Todos los empleados tienen nombre y salario base
    - Cada tipo de empleado calcula su salario diferente
    - Evitamos repetir código
    """
    
    def __init__(self, nombre, salario_base):
        """
        Constructor de la clase base.
        """
        self.nombre = nombre
        self.salario_base = salario_base
    
    def calcular_salario(self):
        """
        Método base que puede ser SOBRESCRITO por las clases hijas.
        """
        return self.salario_base
    
    def presentarse(self):
        """
        Método común a todos los empleados.
        """
        return f"Soy {self.nombre}, empleado de la empresa"

class Programador(EmpleadoBase):
    """
    Clase HIJA que HEREDA de EmpleadoBase.
    Los programadores tienen un bono por proyecto.
    """
    
    def __init__(self, nombre, salario_base, proyectos_completados):
        """
        Constructor que extiende el de la clase padre.
        """
        # super() llama al constructor del padre
        super().__init__(nombre, salario_base)
        self.proyectos_completados = proyectos_completados
    
    def calcular_salario(self):
        """
        SOBRESCRIBIMOS el método del padre.
        Programadores ganan $200 extra por proyecto.
        """
        bono = self.proyectos_completados * 200
        return self.salario_base + bono
    
    def programar(self):
        """
        Método EXCLUSIVO de Programador.
        """
        return f"{self.nombre} está escribiendo código..."

class Gerente(EmpleadoBase):
    """
    Otra clase HIJA con cálculo diferente.
    Los gerentes tienen un bono porcentual.
    """
    
    def __init__(self, nombre, salario_base, bono_porcentaje):
        """
        Constructor del gerente.
        """
        super().__init__(nombre, salario_base)
        self.bono_porcentaje = bono_porcentaje
    
    def calcular_salario(self):
        """
        SOBRESCRIBIMOS el método.
        Gerentes ganan un porcentaje extra sobre su salario base.
        """
        bono = self.salario_base * (self.bono_porcentaje / 100)
        return self.salario_base + bono
    
    def gestionar_equipo(self):
        """
        Método EXCLUSIVO de Gerente.
        """
        return f"{self.nombre} está coordinando el equipo..."

# Crear empleados de diferentes tipos
programador = Programador("Ana Martínez", 3000, 5)
gerente = Gerente("Carlos Ruiz", 5000, 20)

# Ambos pueden usar métodos heredados
print(f"\n{programador.presentarse()}")
print(f"Salario total: ${programador.calcular_salario()}")
print(programador.programar())

print(f"\n{gerente.presentarse()}")
print(f"Salario total: ${gerente.calcular_salario()}")
print(gerente.gestionar_equipo())


print("\n--- PRINCIPIO 4: POLIMORFISMO ---")
print("Mismo método, diferente comportamiento según el objeto")

def procesar_pago_empleado(empleado):
    """
    POLIMORFISMO: Esta función acepta CUALQUIER tipo de empleado.
    
    CASO DE USO REAL: Sistema de nómina
    - No importa si es Programador o Gerente
    - Cada uno calcula su salario de forma diferente
    - Pero podemos tratarlos igual desde afuera
    """
    print(f"\nProcesando pago para: {empleado.nombre}")
    salario = empleado.calcular_salario()
    print(f"Monto a pagar: ${salario}")
    print(f"Transferencia realizada ✓")

# La MISMA función funciona con diferentes tipos de empleados
print("\n--- Sistema de Nómina ---")
empleados = [
    Programador("Luis Torres", 2800, 3),
    Gerente("María Sánchez", 4500, 15),
    Programador("Sofia López", 3200, 7)
]

# Procesamos el pago de TODOS usando la misma función
for emp in empleados:
    procesar_pago_empleado(emp)  # ¡Polimorfismo en acción!


# =================================================================
# 7. EJERCICIO PRÁCTICO - ¡AHORA TÚ!
# =================================================================

print("\n" + "=" * 50)
print("7. EJERCICIO PRÁCTICO")
print("=" * 50)

ejercicio = """
EJERCICIO: Crea un sistema de biblioteca

REQUISITOS:
1. Clase Libro con:
   - Atributos: titulo, autor, disponible (True/False)
   - Métodos: prestar(), devolver(), info()

2. Clase Usuario con:
   - Atributos: nombre, libros_prestados (lista)
   - Métodos: pedir_libro(libro), devolver_libro(libro)

3. Implementar:
   - Un usuario solo puede pedir un libro si está disponible
   - Al pedir un libro, se marca como no disponible
   - Al devolver, vuelve a estar disponible
   - Mostrar cuántos libros tiene cada usuario

PISTA: Usa self.disponible para controlar si un libro está disponible
PISTA: Usa self.libros_prestados.append() para agregar libros a la lista

¡INTENTA HACERLO TÚ MISMO ANTES DE VER LA SOLUCIÓN!
"""

print(ejercicio)

print("\n--- SOLUCIÓN DEL EJERCICIO ---")

class Libro:
    """
    Clase que representa un libro en la biblioteca.
    """
    
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor
        self.disponible = True  # Al inicio está disponible
    
    def prestar(self):
        """Marca el libro como prestado."""
        if self.disponible:
            self.disponible = False
            return f"✓ Libro '{self.titulo}' prestado"
        return f"❌ El libro '{self.titulo}' no está disponible"
    
    def devolver(self):
        """Marca el libro como devuelto."""
        self.disponible = True
        return f"✓ Libro '{self.titulo}' devuelto"
    
    def info(self):
        """Muestra información del libro."""
        estado = "Disponible" if self.disponible else "Prestado"
        return f"'{self.titulo}' por {self.autor} - {estado}"

class UsuarioBiblioteca:
    """
    Clase que representa un usuario de la biblioteca.
    """
    
    def __init__(self, nombre):
        self.nombre = nombre
        self.libros_prestados = []  # Lista vacía al inicio
    
    def pedir_libro(self, libro):
        """Intenta pedir un libro prestado."""
        if libro.disponible:
            resultado = libro.prestar()  # Llama al método prestar del libro
            self.libros_prestados.append(libro)  # Agrega a la lista
            print(f"{self.nombre}: {resultado}")
        else:
            print(f"{self.nombre}: ❌ El libro no está disponible")
    
    def devolver_libro(self, libro):
        """Devuelve un libro a la biblioteca."""
        if libro in self.libros_prestados:
            resultado = libro.devolver()  # Llama al método devolver del libro
            self.libros_prestados.remove(libro)  # Quita de la lista
            print(f"{self.nombre}: {resultado}")
        else:
            print(f"{self.nombre}: No tienes este libro")
    
    def mis_libros(self):
        """Muestra los libros que tiene el usuario."""
        if len(self.libros_prestados) == 0:
            return f"{self.nombre} no tiene libros prestados"
        
        lista = f"\n{self.nombre} tiene {len(self.libros_prestados)} libro(s):"
        for libro in self.libros_prestados:
            lista += f"\n  - {libro.titulo}"
        return lista

# Probar el sistema de biblioteca
print("\n--- Sistema de Biblioteca en Acción ---")

# Crear libros
libro1 = Libro("Python para Todos", "Juan Pérez")
libro2 = Libro("Django Avanzado", "María García")
libro3 = Libro("PostgreSQL Práctico", "Luis Rodríguez")

# Crear usuarios
usuario1 = UsuarioBiblioteca("Roberto")
usuario2 = UsuarioBiblioteca("Carmen")

# Simular préstamos
print("\n--- Préstamos ---")
usuario1.pedir_libro(libro1)  # Roberto pide libro 1
usuario1.pedir_libro(libro2)  # Roberto pide libro 2
usuario2.pedir_libro(libro1)  # Carmen intenta pedir libro 1 (ya prestado)
usuario2.pedir_libro(libro3)  # Carmen pide libro 3

# Ver libros de cada usuario
print(usuario1.mis_libros())
print(usuario2.mis_libros())

# Simular devoluciones
print("\n--- Devoluciones ---")
usuario1.devolver_libro(libro1)  # Roberto devuelve libro 1
usuario2.pedir_libro(libro1)     # Ahora Carmen SÍ puede pedirlo

# Estado final
print("\n--- Estado Final de los Libros ---")
print(libro1.info())
print(libro2.info())
print(libro3.info())

print(usuario1.mis_libros())
print(usuario2.mis_libros())


# =================================================================
# RESUMEN FINAL
# =================================================================

print("\n" + "=" * 50)
print("RESUMEN - CONCEPTOS CLAVE")
print("=" * 50)

resumen = """
CONCEPTOS APRENDIDOS:

1. CLASE: Molde o plantilla para crear objetos
   - Se define con: class NombreClase:

2. OBJETO: Instancia creada a partir de una clase
   - Se crea con: objeto = NombreClase()

3. __init__: Constructor que inicializa el objeto
   - Se ejecuta automáticamente al crear un objeto

4. self: Referencia al objeto actual
   - Permite acceder a los atributos y métodos del objeto

5. ATRIBUTOS: Variables que pertenecen al objeto
   - Ejemplo: self.nombre, self.edad

6. MÉTODOS: Funciones que pertenecen a la clase
   - Ejemplo: def saludar(self):

7. HERENCIA: Crear clases a partir de otras
   - Sintaxis: class Hija(Padre):
   - Permite reutilizar código

LOS 4 PRINCIPIOS DE POO:

1. ENCAPSULAMIENTO: Proteger datos sensibles
   Caso: CuentaBancaria con saldo privado

2. ABSTRACCIÓN: Ocultar complejidad
   Caso: ServicioEmail que simplifica el envío

3. HERENCIA: Reutilizar código
   Caso: EmpleadoBase → Programador, Gerente

4. POLIMORFISMO: Mismo método, diferente comportamiento
   Caso: calcular_salario() diferente para cada empleado

¿CUÁNDO USAR POO?
✓ Cuando tienes entidades con datos y comportamientos (Usuario, Producto)
✓ Cuando necesitas organizar código complejo
✓ Cuando trabajas con frameworks como Django
✓ Cuando quieres reutilizar código (herencia)

VENTAJAS:
• Código más organizado
• Fácil de mantener y modificar
• Reutilización de código
• Refleja el mundo real
"""

print(resumen)

print("\n" + "=" * 50)
print("FIN DEL PROGRAMA")
print("¡Practica creando tus propias clases!")
print("=" * 50)