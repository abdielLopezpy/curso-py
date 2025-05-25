# 🚀 Programación Orientada a Objetos (POO)

## 📚 ¿Qué es la Programación Orientada a Objetos?

La Programación Orientada a Objetos (POO) es un paradigma de programación que organiza el código en torno a **objetos** en lugar de funciones y lógica. Permite crear código más organizado, reutilizable y fácil de mantener.

> 💡 **Metáfora:** Piensa en POO como una colección de "objetos" que interactúan entre sí, similar a cómo en el mundo real los buses, pasajeros y choferes interactúan en un sistema de transporte.

## 🔑 Conceptos Fundamentales de POO

### 1. Clases

Una **clase** es una plantilla o molde para crear objetos. Define las propiedades (atributos) y comportamientos (métodos) que tendrán todos los objetos creados a partir de ella.

```python
# Ejemplo: La clase Bus define la estructura para todos los buses
class Bus:
    # Atributos de clase
    _total_buses = 0
    
    # Constructor
    def __init__(self, ruta, capacidad, numero_bus):
        # Atributos de instancia
        self.__ruta = ruta
        self.__capacidad = capacidad
        self.__numero_bus = numero_bus
        self.__pasajeros_actuales = 0
        Bus._total_buses += 1
        
    # Métodos
    def subir_pasajeros(self, cantidad):
        # Código para subir pasajeros
        pass
```

> 📌 **Ejemplo real:** En nuestro simulador, `Bus` es una clase que define el comportamiento de todos los autobuses del sistema.

### 2. Objetos

Un **objeto** es una instancia de una clase. Si la clase es el molde, el objeto es el producto final creado con ese molde.

```python
# Crear objetos (instancias) de la clase Bus
bus1 = Bus("Ruta 1", 50, "B-123")
bus2 = Bus("Ruta 2", 40, "B-456")

# Cada objeto tiene su propio estado (atributos)
# pero comparte comportamiento (métodos)
```

> 📌 **Ejemplo real:** En el simulador, creamos varios buses como `bus1` y `bus2`, cada uno con sus propias características.

### 3. Atributos

Los **atributos** son las características o propiedades que tiene un objeto.

#### Tipos de atributos

- **Atributos de instancia**: Pertenecen a cada objeto individual.
- **Atributos de clase**: Compartidos por todos los objetos de la clase.

```python
class Bus:
    # Atributo de clase - compartido por todos los buses
    _total_buses = 0
    _capacidad_estandar = 50
    
    def __init__(self, ruta, capacidad, numero_bus):
        # Atributos de instancia - únicos para cada bus
        self.__ruta = ruta              # Privado
        self.__capacidad = capacidad    # Privado
        self.__numero_bus = numero_bus  # Privado
        self.__pasajeros_actuales = 0   # Privado
```

> 💡 **Nota:** Los atributos con doble guion bajo (`__`) son privados y solo se pueden acceder desde dentro de la clase.

### 4. Métodos

Los **métodos** son funciones definidas dentro de una clase que describen los comportamientos del objeto.

#### Tipos de métodos

- **Métodos de instancia**: Operan sobre un objeto específico.
- **Métodos de clase**: Operan sobre la clase en sí misma.
- **Métodos estáticos**: Funciones relacionadas con la clase pero que no acceden a los datos de la clase.

```python
class Bus:
    # Método de instancia
    def subir_pasajeros(self, cantidad):
        if self.__pasajeros_actuales + cantidad <= self.__capacidad:
            self.__pasajeros_actuales += cantidad
            Bus._total_pasajeros_transportados += cantidad
            return f"Subieron {cantidad} pasajeros al bus {self.__numero_bus}"
            
    # Método de clase
    @classmethod
    def contar_buses(cls):
        return f"Existen {cls._total_buses} buses en la flota."
        
    # Método de instancia para cambiar la ruta
    def cambiar_ruta(self, nueva_ruta):
        self.__ruta = nueva_ruta
        return f"El bus ahora va por la ruta {self.__ruta}."
```

> 📌 **Ejemplo real:** En el simulador, cada bus tiene métodos como `subir_pasajeros()`, `bajar_pasajeros()` y `cambiar_ruta()`.

### 5. Constructor

El **constructor** (`__init__`) es un método especial que se ejecuta automáticamente cuando se crea un nuevo objeto.

```python
def __init__(self, ruta, capacidad, numero_bus):
    # Inicializa atributos
    self.__ruta = ruta
    self.__capacidad = capacidad
    self.__numero_bus = numero_bus
    self.__pasajeros_actuales = 0
    
    # Incrementa contador de clase
    Bus._total_buses += 1
```

> 💡 **Nota:** El constructor es como el "formulario de registro" que debe completarse para crear un nuevo objeto.

## 🏛️ Pilares de la Programación Orientada a Objetos

### 1. Encapsulamiento

El **encapsulamiento** consiste en ocultar los detalles internos de un objeto y exponer solo lo necesario. Se implementa usando atributos y métodos privados.

En Python:

- Atributos/métodos con `__` (doble guion bajo) son privados.
- Atributos/métodos con `_` (un guion bajo) son protegidos.

```python
class Bus:
    def __init__(self, ruta, capacidad):
        # Atributos privados
        self.__ruta = ruta
        self.__capacidad = capacidad
        
    # Métodos para acceder (getters)
    def get_ruta(self):
        return self.__ruta
        
    # Métodos para modificar (setters)
    def set_ruta(self, nueva_ruta):
        if isinstance(nueva_ruta, str) and nueva_ruta:
            self.__ruta = nueva_ruta
            return True
        return False
```

> 🔒 **Beneficio:** El encapsulamiento previene que el código externo manipule incorrectamente los atributos internos del objeto.

### 2. Herencia

La **herencia** permite crear nuevas clases que heredan atributos y métodos de clases existentes.

```python
# Clase base (padre)
class Persona:
    def __init__(self, nombre):
        self.nombre = nombre
        
    def presentarse(self):
        return f"¡Hola, soy {self.nombre}!"

# Clase derivada (hijo)
class Chofer(Persona):
    def __init__(self, nombre, bus):
        # Llama al constructor de la clase padre
        super().__init__(nombre)
        self.bus = bus
        
    # Añade nuevos métodos
    def conducir(self):
        return f"{self.nombre} está conduciendo el bus {self.bus._Bus__numero_bus}"
```

> 👨‍👦 **Ejemplo real:** En nuestro simulador, tanto `Chofer` como `Pasajero` heredan de `Persona`, compartiendo propiedades básicas pero añadiendo comportamiento específico.

### 3. Polimorfismo

El **polimorfismo** permite que objetos de diferentes clases respondan de manera diferente al mismo método.

```python
# Diferentes clases con el mismo método pero comportamiento diferente
class Chofer(Persona):
    def presentarse(self):
        return f"¡Hola, soy el chofer {self.nombre}!"
        
class Pasajero(Persona):
    def presentarse(self):
        return f"¡Hola, soy el pasajero {self.nombre}!"
        
# Uso polimórfico - mismo método, diferentes comportamientos
def saludar(persona):
    return persona.presentarse()

# Funcionará tanto para choferes como para pasajeros
chofer = Chofer("Juan", bus1)
pasajero = Pasajero("María", "Ruta 1")

print(saludar(chofer))   # "¡Hola, soy el chofer Juan!"
print(saludar(pasajero)) # "¡Hola, soy el pasajero María!"
```

> 🔄 **Concepto clave:** El polimorfismo permite tratar objetos de diferentes clases de manera uniforme siempre que implementen los mismos métodos.

### 4. Abstracción

La **abstracción** consiste en mostrar solo la información esencial y ocultar los detalles complejos.

```python
# La clase Bus ofrece métodos como subir_pasajeros() y bajar_pasajeros()
# Los usuarios no necesitan saber cómo se implementan estos métodos internamente

# Ejemplo de abstracción
bus = Bus("Ruta 1", 50, "B-123")
resultado = bus.subir_pasajeros(5)  # No necesitamos saber cómo funciona internamente

# El sistema solo muestra lo necesario:
print(bus.mostrar_info())  # "Bus: B-123, Ruta: Ruta 1, Pasajeros: 5/50"
```

> 🎭 **Analogía:** Como conductor, usas el volante, frenos y acelerador sin necesitar entender exactamente cómo funciona el motor del coche internamente.

## 💪 Ventajas de la POO

1. **Reutilización del código**: Las clases pueden usarse múltiples veces.
2. **Modularidad**: El código se organiza en bloques lógicos.
3. **Flexibilidad**: Facilita los cambios y extensiones del programa.
4. **Mantenibilidad**: Código más limpio y fácil de mantener.
5. **Organización**: Los problemas se dividen en entidades más pequeñas y manejables.
6. **Modelo del mundo real**: Representa de forma más natural objetos y relaciones del mundo real.
7. **Seguridad**: El encapsulamiento protege los datos y previene modificaciones no deseadas.

## 🚌 Ejemplo Práctico: Sistema de Simulación de Transporte

El archivo `simulador_transporte.py` de este proyecto es un excelente ejemplo de programación orientada a objetos:

- Usa **clases** (`Bus`, `Persona`, `Chofer`, `Pasajero`) para modelar entidades del mundo real.
- Implementa **encapsulamiento** con atributos privados (`__ruta`, `__capacidad`).
- Muestra **herencia** con las clases `Chofer` y `Pasajero` que extienden `Persona`.
- Contiene **métodos de instancia** (`subir_pasajeros()`) y **métodos de clase** (`contar_buses()`).
- Utiliza **polimorfismo** al tener diferentes implementaciones del método `presentarse()`.

### Diagrama de Clases del Simulador

```
┌───────────┐         ┌───────────┐
│   Bus     │         │  Persona  │
├───────────┤         ├───────────┤
│ _total_buses        │ nombre    │
│ _cap_estandar       ├───────────┤
├───────────┤         │presentarse()
│ __ruta    │         └─────┬─────┘
│ __capacidad         ┌─────┴─────┐
│ __numero_bus        │           │
│ __pasajeros         │           │
├───────────┤    ┌────┴───┐  ┌────┴────┐
│subir_pasajeros()│ Chofer │  │ Pasajero │
│bajar_pasajeros()├────────┤  ├─────────┤
│cambiar_ruta()   │ bus    │  │ruta_pref│
│mostrar_info()   ├────────┤  ├─────────┤
└───────────┘     │conducir│  │subir_bus│
                  └────────┘  └─────────┘
```

## 📝 Casos de Uso Prácticos

### ¿Cuándo usar POO?

- **Sistemas complejos** con múltiples entidades relacionadas.
- **Software que simula** objetos del mundo real (como nuestro sistema de transporte).
- **Interfaces gráficas** donde cada elemento es un objeto (botones, ventanas, etc.).
- **Juegos** donde personajes, enemigos, objetos interactúan entre sí.
- **Aplicaciones empresariales** con usuarios, productos, transacciones, etc.

### Ejemplo de uso real en el simulador:

```python
# Creamos buses
bus1 = Bus("Ruta 1", 50, "B-123")
bus2 = Bus("Ruta 2", 40, "B-456")

# Creamos personal
chofer1 = Chofer("José", bus1)
chofer2 = Chofer("Sofía", bus2)

# Creamos pasajeros
pasajero1 = Pasajero("Carlos", "Ruta 1")
pasajero2 = Pasajero("María", "Ruta 2")

# Interacción entre objetos
print(chofer1.manejar_y_subir_pasajeros(5))  # José hace subir 5 pasajeros
print(pasajero1.subir_a_bus(bus1))           # Carlos sube al bus1
print(Bus.contar_buses())                    # Muestra el total de buses
print(bus1.mostrar_info())                   # Muestra la información del bus1
```

## 🏋️ Ejercicios de Práctica

1. Crea una nueva clase `Estacion` que represente una parada de bus.
2. Modifica la clase `Bus` para que tenga un método `llegar_a_estacion()`.
3. Implementa un sistema de tarifas usando encapsulamiento.
4. Crea una subclase de `Bus` llamada `BusElectrico` que herede todo el comportamiento de `Bus` pero tenga métodos adicionales como `cargar_bateria()`.
5. Implementa un método estático en la clase `Bus` que calcule el tiempo estimado entre dos rutas.

## 📚 Recursos Adicionales

- [Documentación oficial de Python sobre POO](https://docs.python.org/es/3/tutorial/classes.html)
- [Real Python: Object-Oriented Programming in Python](https://realpython.com/python3-object-oriented-programming/)
- [Programación orientada a objetos en Wikipedia](https://es.wikipedia.org/wiki/Programaci%C3%B3n_orientada_a_objetos)

### Libros recomendados:
- "Python Object-Oriented Programming" por Steven F. Lott
- "Learning Python" por Mark Lutz
- "Head First Object-Oriented Analysis and Design" por Brett McLaughlin

---

Desarrollado para el curso de Python por Alejandro - Mayo 2025
