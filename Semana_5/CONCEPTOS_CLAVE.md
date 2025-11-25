# Conceptos Clave de Python - Semana 5

Este documento explica los conceptos importantes de Python que usamos en esta semana del curso.

---

## 📚 Tabla de Contenidos

1. [¿Qué es @dataclass?](#qué-es-dataclass)
2. [Clases y Objetos](#clases-y-objetos)
3. [Herencia](#herencia)
4. [Clases Abstractas (ABC)](#clases-abstractas-abc)
5. [Type Hints y Typing](#type-hints-y-typing)
6. [Métodos de Clase (@classmethod)](#métodos-de-clase-classmethod)
7. [Genéricos (Generic)](#genéricos-generic)
8. [Enumeraciones (Enum)](#enumeraciones-enum)

---

## ¿Qué es @dataclass?

### Explicación Simple

`@dataclass` es un **decorador** de Python que te ayuda a crear clases de forma más fácil y limpia, especialmente cuando quieres almacenar datos.

### Sin @dataclass (la forma tradicional)

```python
class Producto:
    def __init__(self, id, nombre, precio):
        self.id = id
        self.nombre = nombre
        self.precio = precio

    def __repr__(self):
        return f"Producto(id={self.id}, nombre={self.nombre}, precio={self.precio})"

    def __eq__(self, other):
        if not isinstance(other, Producto):
            return False
        return self.id == other.id and self.nombre == other.nombre and self.precio == other.precio
```

### Con @dataclass (forma moderna y simple)

```python
from dataclasses import dataclass

@dataclass
class Producto:
    id: int
    nombre: str
    precio: float
```

### ¿Qué hace @dataclass automáticamente?

1. **Crea el `__init__`**: No necesitas escribir el constructor
2. **Crea el `__repr__`**: Genera una representación en texto automática
3. **Crea el `__eq__`**: Permite comparar objetos
4. **Más legible**: El código es más claro y fácil de entender

### Ejemplo Completo

```python
from dataclasses import dataclass

@dataclass
class Estudiante:
    id: int
    nombre: str
    edad: int
    promedio: float

# Crear un estudiante es muy fácil
estudiante1 = Estudiante(1, "Ana García", 20, 9.5)

# Imprimir muestra automáticamente todos los datos
print(estudiante1)
# Salida: Estudiante(id=1, nombre='Ana García', edad=20, promedio=9.5)

# Comparar estudiantes
estudiante2 = Estudiante(1, "Ana García", 20, 9.5)
print(estudiante1 == estudiante2)  # True
```

### ¿Cuándo usar @dataclass?

✅ **Úsalo cuando**:
- Necesitas almacenar datos relacionados juntos
- Quieres crear objetos rápidamente
- Necesitas representar entidades (Producto, Cliente, Venta, etc.)

❌ **No lo uses cuando**:
- La clase tiene mucha lógica compleja
- Necesitas controlar completamente el `__init__`

---

## Clases y Objetos

### ¿Qué es una Clase?

Una **clase** es como un molde o plantilla para crear objetos. Define qué datos y operaciones tiene un tipo de objeto.

### ¿Qué es un Objeto?

Un **objeto** es una instancia específica de una clase. Es un "ejemplar" creado a partir del molde.

### Analogía del Mundo Real

```
Clase = Receta de galletas
Objeto = Una galleta específica que hiciste con la receta
```

### Ejemplo

```python
from dataclasses import dataclass

# CLASE: El molde/plantilla
@dataclass
class Carro:
    marca: str
    modelo: str
    año: int
    color: str

# OBJETOS: Carros específicos creados con el molde
carro1 = Carro("Toyota", "Corolla", 2020, "Rojo")
carro2 = Carro("Honda", "Civic", 2021, "Azul")
carro3 = Carro("Mazda", "3", 2022, "Negro")

print(carro1)  # Carro(marca='Toyota', modelo='Corolla', año=2020, color='Rojo')
print(carro2)  # Carro(marca='Honda', modelo='Civic', año=2021, color='Azul')
```

### Métodos de una Clase

Los métodos son **funciones** que pertenecen a una clase y operan sobre sus datos.

```python
from dataclasses import dataclass

@dataclass
class Rectangulo:
    ancho: float
    alto: float

    # Método para calcular el área
    def area(self) -> float:
        return self.ancho * self.alto

    # Método para calcular el perímetro
    def perimetro(self) -> float:
        return 2 * (self.ancho + self.alto)

    # Método para verificar si es un cuadrado
    def es_cuadrado(self) -> bool:
        return self.ancho == self.alto

# Usar los métodos
rect = Rectangulo(10, 5)
print(f"Área: {rect.area()}")           # Área: 50
print(f"Perímetro: {rect.perimetro()}")  # Perímetro: 30
print(f"¿Es cuadrado? {rect.es_cuadrado()}")  # ¿Es cuadrado? False
```

---

## Herencia

### ¿Qué es la Herencia?

La **herencia** permite crear una clase nueva basada en una clase existente. La clase nueva (hija) obtiene todas las características de la clase padre y puede agregar más.

### Analogía del Mundo Real

```
Clase Padre: Animal
  └── Clase Hija: Perro (hereda de Animal, pero agrega características específicas)
```

### Ejemplo Básico

```python
from dataclasses import dataclass

# Clase PADRE (Base)
@dataclass
class Persona:
    nombre: str
    edad: int

    def saludar(self):
        print(f"Hola, soy {self.nombre}")

# Clase HIJA (hereda de Persona)
@dataclass
class Estudiante(Persona):
    carrera: str
    promedio: float

    def estudiar(self):
        print(f"{self.nombre} está estudiando {self.carrera}")

# El estudiante tiene TODO lo de Persona + sus propios atributos
est = Estudiante("Ana", 20, "Ingeniería", 9.5)
est.saludar()    # Método heredado de Persona
est.estudiar()   # Método propio de Estudiante
```

### ¿Por qué usar Herencia?

✅ **Ventajas**:
- **Reutilización de código**: No repites el código común
- **Organización**: Agrupa características comunes en la clase padre
- **Extensibilidad**: Fácil agregar nuevos tipos

### Ejemplo en el Framework

En nuestro framework, todas las entidades heredan de `Entidad`:

```python
from dataclasses import dataclass
from database_framework import Entidad

@dataclass
class Producto(Entidad):  # <-- Hereda de Entidad
    id: int
    nombre: str
    precio: float

    def obtener_id(self) -> int:
        return self.id
```

Esto significa que `Producto` automáticamente tiene:
- El método `a_diccionario()` de Entidad
- El método `__str__()` de Entidad
- La estructura que espera el framework

---

## Clases Abstractas (ABC)

### ¿Qué es una Clase Abstracta?

Una **clase abstracta** es una clase que:
1. **No se puede instanciar directamente** (no puedes crear objetos de ella)
2. **Define métodos que DEBEN implementarse** en las clases hijas
3. **Sirve como plantilla** para otras clases

### ¿Para qué sirven?

Las clases abstractas sirven para **forzar que todas las clases hijas implementen ciertos métodos**.

### Ejemplo

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

# Clase ABSTRACTA (no se puede instanciar)
class Vehiculo(ABC):
    @abstractmethod
    def arrancar(self):
        """Todas las clases hijas DEBEN implementar este método"""
        pass

    @abstractmethod
    def detener(self):
        """Todas las clases hijas DEBEN implementar este método"""
        pass

# Clase CONCRETA (sí se puede instanciar)
@dataclass
class Carro(Vehiculo):
    marca: str

    def arrancar(self):
        print(f"{self.marca} arrancó con el motor")

    def detener(self):
        print(f"{self.marca} se detuvo con los frenos")

# Clase CONCRETA
@dataclass
class Bicicleta(Vehiculo):
    tipo: str

    def arrancar(self):
        print("Bicicleta comenzó a pedalear")

    def detener(self):
        print("Bicicleta usó los frenos de mano")

# ❌ NO PUEDES HACER ESTO:
# vehiculo = Vehiculo()  # Error: no se puede instanciar clase abstracta

# ✅ SÍ PUEDES HACER ESTO:
carro = Carro("Toyota")
carro.arrancar()  # Toyota arrancó con el motor

bici = Bicicleta("Montaña")
bici.arrancar()   # Bicicleta comenzó a pedalear
```

### En el Framework

```python
class Entidad(ABC):
    @abstractmethod
    def obtener_id(self) -> Any:
        """Todas las entidades DEBEN tener este método"""
        pass
```

Esto obliga a que **todas** las clases que hereden de `Entidad` implementen `obtener_id()`.

---

## Type Hints y Typing

### ¿Qué son los Type Hints?

Los **Type Hints** son anotaciones que indican qué tipo de datos espera una variable, parámetro o retorno de función.

### ¿Para qué sirven?

1. **Documentación**: Es más claro qué tipo de datos esperar
2. **Autocompletado**: Los editores pueden ayudarte mejor
3. **Detección de errores**: Herramientas pueden detectar errores antes de ejecutar

### Sintaxis

```python
# Variables
nombre: str = "Ana"
edad: int = 25
precio: float = 99.99
activo: bool = True

# Funciones
def sumar(a: int, b: int) -> int:
    return a + b

def saludar(nombre: str) -> str:
    return f"Hola {nombre}"

# Listas
numeros: List[int] = [1, 2, 3, 4, 5]
nombres: List[str] = ["Ana", "Luis", "María"]

# Diccionarios
datos: Dict[str, Any] = {
    "nombre": "Ana",
    "edad": 25,
    "activo": True
}

# Opcional (puede ser None)
def buscar_usuario(id: int) -> Optional[str]:
    if id == 1:
        return "Ana"
    return None  # Puede retornar None
```

### Tipos Comunes

| Type Hint | Descripción | Ejemplo |
|-----------|-------------|---------|
| `int` | Número entero | `42` |
| `float` | Número decimal | `3.14` |
| `str` | Texto | `"Hola"` |
| `bool` | Verdadero/Falso | `True` |
| `List[int]` | Lista de enteros | `[1, 2, 3]` |
| `Dict[str, int]` | Diccionario str→int | `{"a": 1}` |
| `Optional[str]` | Puede ser str o None | `"Ana"` o `None` |
| `Any` | Cualquier tipo | Cualquier cosa |

---

## Métodos de Clase (@classmethod)

### ¿Qué es @classmethod?

Un **método de clase** es un método que:
1. **Pertenece a la clase**, no a un objeto específico
2. **Recibe `cls` como primer parámetro** (la clase misma)
3. **Puede crear instancias de la clase** de formas alternativas

### ¿Cuándo usar @classmethod?

Se usa para crear **métodos constructores alternativos**.

### Ejemplo

```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Producto:
    id: int
    nombre: str
    precio: float

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> 'Producto':
        """Constructor alternativo: crea un Producto desde un diccionario"""
        return cls(
            id=datos['id'],
            nombre=datos['nombre'],
            precio=datos['precio']
        )

    @classmethod
    def crear_gratis(cls, id: int, nombre: str) -> 'Producto':
        """Constructor alternativo: crea un producto gratis"""
        return cls(id, nombre, 0.0)

# Forma normal de crear
p1 = Producto(1, "Laptop", 1200.0)

# Usando classmethod desde diccionario
datos = {"id": 2, "nombre": "Mouse", "precio": 25.0}
p2 = Producto.desde_diccionario(datos)

# Usando classmethod gratis
p3 = Producto.crear_gratis(3, "Muestra")
print(p3)  # Producto(id=3, nombre='Muestra', precio=0.0)
```

### En el Framework

```python
@classmethod
def desde_diccionario(cls, datos: Dict[str, Any]) -> Entidad:
    """Crea una entidad desde un diccionario JSON"""
    return cls(**datos)
```

Esto permite convertir datos JSON (diccionarios) en objetos de Python.

---

## Genéricos (Generic)

### ¿Qué son los Genéricos?

Los **genéricos** permiten crear clases o funciones que funcionen con **cualquier tipo** de dato, pero manteniendo la seguridad de tipos.

### Analogía

Piensa en una **caja genérica**:
- Puede guardar cualquier cosa (números, textos, objetos)
- Pero una vez defines qué tipo guarda, solo acepta ese tipo

### Ejemplo Simple

```python
from typing import List, TypeVar, Generic

# Definir un tipo genérico
T = TypeVar('T')

class Caja(Generic[T]):
    def __init__(self):
        self.contenido: List[T] = []

    def agregar(self, item: T) -> None:
        self.contenido.append(item)

    def obtener_todos(self) -> List[T]:
        return self.contenido

# Caja de enteros
caja_numeros: Caja[int] = Caja()
caja_numeros.agregar(10)
caja_numeros.agregar(20)

# Caja de textos
caja_textos: Caja[str] = Caja()
caja_textos.agregar("Hola")
caja_textos.agregar("Mundo")
```

### En el Framework

```python
T = TypeVar('T', bound=Entidad)

class RepositorioJSON(Generic[T]):
    def __init__(self, nombre: str, tipo_entidad: Type[T], ...):
        self.tipo_entidad = tipo_entidad

    def consultar_todos(self) -> List[T]:
        # Retorna una lista del tipo especificado
        return [...]
```

Esto permite que:
```python
# Repositorio de Productos
repo_productos: RepositorioJSON[Producto] = RepositorioJSON(...)
productos: List[Producto] = repo_productos.consultar_todos()

# Repositorio de Clientes
repo_clientes: RepositorioJSON[Cliente] = RepositorioJSON(...)
clientes: List[Cliente] = repo_clientes.consultar_todos()
```

---

## Enumeraciones (Enum)

### ¿Qué es una Enumeración?

Una **enumeración** es un conjunto de **constantes con nombre** que representan valores relacionados.

### ¿Para qué sirven?

✅ **Ventajas**:
- Código más legible
- Evita errores de escritura
- Agrupas valores relacionados
- El editor te sugiere las opciones

### Ejemplo Simple

```python
from enum import Enum

class DiaSemana(Enum):
    LUNES = 1
    MARTES = 2
    MIERCOLES = 3
    JUEVES = 4
    VIERNES = 5
    SABADO = 6
    DOMINGO = 7

# Usar la enumeración
hoy = DiaSemana.LUNES
print(hoy)         # DiaSemana.LUNES
print(hoy.value)   # 1
print(hoy.name)    # 'LUNES'

# Comparar
if hoy == DiaSemana.LUNES:
    print("¡Es lunes!")

# Iterar sobre todos los días
for dia in DiaSemana:
    print(dia.name, dia.value)
```

### Otro Ejemplo: Estados

```python
from enum import Enum

class EstadoPedido(Enum):
    PENDIENTE = "pending"
    PROCESANDO = "processing"
    ENVIADO = "shipped"
    ENTREGADO = "delivered"
    CANCELADO = "cancelled"

pedido_estado = EstadoPedido.PROCESANDO

if pedido_estado == EstadoPedido.PROCESANDO:
    print("El pedido está siendo procesado...")
```

### En el Framework

```python
class TipoOperacion(Enum):
    CREAR = "CREATE"
    LEER = "READ"
    ACTUALIZAR = "UPDATE"
    ELIMINAR = "DELETE"
    CONSULTAR = "QUERY"

# Usar en la bitácora
self._registrar_operacion(TipoOperacion.CREAR, entidad_id, datos)
```

---

## 🎯 Resumen Rápido

| Concepto | ¿Qué es? | ¿Para qué sirve? |
|----------|----------|------------------|
| `@dataclass` | Decorador para crear clases simples | Facilita crear clases que almacenan datos |
| **Clase** | Molde/plantilla | Define la estructura de los objetos |
| **Objeto** | Instancia de una clase | Un ejemplar específico creado del molde |
| **Herencia** | Clase hija hereda de clase padre | Reutilizar código y crear jerarquías |
| **ABC** | Clase abstracta | Forzar implementación de métodos |
| **Type Hints** | Anotaciones de tipo | Documentar y validar tipos de datos |
| `@classmethod` | Método de la clase | Constructores alternativos |
| **Generic** | Tipos parametrizados | Crear código reutilizable con tipos |
| **Enum** | Conjunto de constantes | Agrupar valores relacionados |

---

## 📚 Recursos Adicionales

- [Documentación oficial de dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [Documentación oficial de ABC](https://docs.python.org/3/library/abc.html)
- [Documentación oficial de typing](https://docs.python.org/3/library/typing.html)
- [Documentación oficial de Enum](https://docs.python.org/3/library/enum.html)
- [Tutorial de Clases en Python](https://docs.python.org/3/tutorial/classes.html)

---

## ❓ Preguntas Frecuentes

### ¿Tengo que entender TODO esto para hacer el desafío?

**No necesariamente**. Para el desafío básico solo necesitas entender:
- ✅ @dataclass (crear clases simples)
- ✅ Herencia (heredar de Entidad)
- ✅ Type Hints básicos (int, str, float, List)

Los demás conceptos te ayudarán a entender **cómo funciona** el framework, pero no necesitas dominarlos para usarlo.

### ¿Por qué usar @dataclass en vez de clases normales?

Porque es **más simple y rápido**. Menos código, más claridad.

### ¿Qué es `self`?

`self` se refiere al **objeto actual**. Es como decir "yo mismo" dentro de la clase.

```python
@dataclass
class Persona:
    nombre: str

    def saludar(self):
        print(f"Hola, soy {self.nombre}")  # self.nombre = mi propio nombre

ana = Persona("Ana")
ana.saludar()  # self = ana, entonces imprime "Hola, soy Ana"
```

### ¿Qué es `cls`?

`cls` se refiere a la **clase misma** (no a un objeto específico). Se usa en `@classmethod`.

```python
class Producto:
    @classmethod
    def crear_nuevo(cls):
        return cls(...)  # cls = Producto
```

---

**¡Revisa este documento siempre que tengas dudas sobre los conceptos!**
