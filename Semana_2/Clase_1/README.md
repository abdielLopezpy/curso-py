# Clase 1: Funciones en Python

## ¿Qué son las funciones?

Las funciones son bloques de código organizados que realizan una tarea específica. Son como "mini-programas" dentro de tu programa principal que puedes llamar cuando los necesites.

## Ventajas de usar funciones

- **Reutilización de código**: Escribes el código una vez y lo usas muchas veces.
- **Organización**: Tu código queda mejor organizado y es más fácil de entender.
- **Mantenimiento**: Si necesitas hacer cambios, sólo modificas la función, no todo el código.
- **Simplificación**: Divides problemas grandes en tareas más pequeñas y manejables.

## Sintaxis de una función en Python

```python
def nombre_de_la_funcion(parametro1, parametro2):
    # Código que realiza la tarea
    # ...
    return resultado  # opcional
```

Donde:
- `def` es la palabra clave para definir una función
- `nombre_de_la_funcion` es el nombre que le das a tu función
- `parametro1, parametro2` son datos que la función necesita para trabajar (opcionales)
- `return` devuelve un resultado después de ejecutar la función (opcional)

## Ejemplos prácticos

### Función simple sin parámetros

```python
def saludar():
    print("¡Hola! Bienvenido al curso de Python")

# Llamar a la función
saludar()
```

### Función con parámetros

```python
def saludar_persona(nombre):
    print(f"¡Hola {nombre}! Bienvenido al curso de Python")

# Llamar a la función pasando un argumento
saludar_persona("Juan")
saludar_persona("María")
```

### Función que devuelve un valor

```python
def sumar(a, b):
    resultado = a + b
    return resultado

# Usar el valor devuelto
total = sumar(5, 3)
print(f"La suma es: {total}")
```

### Función con parámetros por defecto

```python
def saludar_con_idioma(nombre, idioma="español"):
    if idioma == "español":
        print(f"¡Hola {nombre}!")
    elif idioma == "inglés":
        print(f"Hello {nombre}!")

# Usar la función con el valor por defecto
saludar_con_idioma("Carlos")  # Saluda en español

# Cambiar el valor por defecto
saludar_con_idioma("Carlos", "inglés")  # Saluda en inglés
```

## Ejercicios prácticos

Revisa el archivo `ejercicios_funciones.py` para practicar con funciones en Python.

## Quiz

Completa el archivo `quiz_funciones.py` para poner a prueba tu conocimiento sobre funciones.
