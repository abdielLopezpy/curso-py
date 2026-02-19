# ============================================================================
# EXAMEN FINAL - SEMANA 10: Proyecto Integrador Flask
# ============================================================================

**Nombre del estudiante:** _______________________________________________

**Fecha:** _______________________________________________

**Proyecto elegido:** [ ] E-Commerce  [ ] Sistema de Citas  [ ] Publicidad Aeropuertos

---

## Instrucciones

- Elija **uno** de los tres proyectos disponibles.
- Estudie el código del proyecto y responda las preguntas a continuación.
- Escriba su respuesta en el espacio indicado debajo de cada pregunta.
- Sea claro y específico. Cuando la pregunta diga "señala en el código", incluya el nombre del archivo y la línea aproximada.

---

## PARTE A: Python Básico (20 pts)

### Pregunta 1 (5 pts)
¿Qué es una variable? Muéstrame un ejemplo del código del proyecto que elegiste.

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 2 (5 pts)
¿Qué diferencia hay entre un `string`, un `int` y un `float`? Señala uno de cada tipo en el código del proyecto.

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 3 (5 pts)
¿Qué hace `.strip()` cuando se aplica a un string? ¿Por qué se usa en los formularios del proyecto?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 4 (5 pts)
¿Qué hace `f'Bienvenido, {usuario.nombre}!'`? ¿Cómo se llama esa técnica en Python?

**Tu respuesta:**
```
(escribe aquí)


```

---

## PARTE B: Funciones y POO (20 pts)

### Pregunta 5 (5 pts)
¿Qué es una clase en Python? Elige un modelo del proyecto y explica sus partes (atributos, métodos, propiedades).

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 6 (5 pts)
¿Qué es `self` dentro de una clase? ¿Por qué es necesario?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 7 (5 pts)
¿Qué es una `@property`? Busca un ejemplo en el proyecto y explica qué hace y por qué se usa.

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 8 (5 pts)
¿Qué es un decorador (`@algo`)? Explica con tus palabras qué hace `@app.route('/login')`.

**Tu respuesta:**
```
(escribe aquí)


```

---

## PARTE C: Base de Datos y SQL (20 pts)

### Pregunta 9 (4 pts)
¿Qué hace `create_engine(DATABASE_URL)`? ¿Qué información contiene esa URL de conexión?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 10 (4 pts)
¿Qué es una clave foránea (Foreign Key)? Señala una en el código del proyecto y explica qué tablas conecta.

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 11 (4 pts)
¿Qué hace `db.add(producto)`? ¿Y `db.commit()`? ¿Por qué son pasos separados?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 12 (4 pts)
¿Qué pasa si ocurre un error después de `db.add()` pero antes de `db.commit()`? ¿Para qué sirve `db.rollback()`?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 13 (4 pts)
¿Qué es `relationship()` en SQLAlchemy? ¿En qué se diferencia de `ForeignKey`?

**Tu respuesta:**
```
(escribe aquí)


```

---

## PARTE D: Flask y Rutas (20 pts)

### Pregunta 14 (4 pts)
¿Qué diferencia hay entre `methods=['GET']` y `methods=['GET', 'POST']` en una ruta de Flask?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 15 (4 pts)
¿Qué hace `request.form.get('nombre', '')`? ¿Por qué se usa `.get()` en vez de acceder con `request.form['nombre']`?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 16 (4 pts)
¿Qué hace `redirect(url_for('login'))`? ¿Por qué usar `url_for()` en vez de escribir `/login` directamente?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 17 (4 pts)
¿Qué es `flash()` y para qué se usa? ¿En qué parte del template se muestran los mensajes?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 18 (4 pts)
¿Qué hace `render_template('index.html', productos=productos)`? ¿Cómo accede el template a la variable `productos`?

**Tu respuesta:**
```
(escribe aquí)


```

---

## PARTE E: Autenticación y Seguridad (20 pts)

### Pregunta 19 (5 pts)
¿Por qué no se guardan las contraseñas en texto plano? ¿Qué hacen `generate_password_hash()` y `check_password_hash()`?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 20 (5 pts)
¿Qué es una sesión en Flask (`session`)? ¿Qué información se guarda en ella al hacer login en el proyecto?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 21 (5 pts)
Explica paso a paso cómo funciona el decorador `@login_required`. ¿Qué pasa si un usuario no logueado intenta acceder a una ruta protegida?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 22 (5 pts)
¿Qué diferencia hay entre `@login_required` y `@admin_required`? ¿Por qué se necesitan dos decoradores distintos?

**Tu respuesta:**
```
(escribe aquí)


```

---

## PARTE F: Templates y Frontend (10 pts)

### Pregunta 23 (5 pts)
¿Qué hace `{% extends "base.html" %}` al inicio de un template? ¿Qué es la herencia de templates y por qué es útil?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 24 (5 pts)
¿Qué es un macro en Jinja2? Busca uno en `macros.html` del proyecto, cópialo aquí y explica cómo funciona.

**Tu respuesta:**
```
(escribe aquí)


```

---

## PARTE G: Preguntas del Proyecto Elegido (10 pts)

> Responde SOLO las preguntas de tu proyecto. Si elegiste E-Commerce responde G.1, si elegiste Citas responde G.2, si elegiste Publicidad responde G.3.

### G.1 Si elegiste E-Commerce:

**Pregunta 25a (5 pts):** Explica el flujo completo del carrito de compras: desde que el usuario agrega un producto hasta que se crea el pedido en el checkout. ¿Qué pasa con el stock?

**Tu respuesta:**
```
(escribe aquí)


```

**Pregunta 26a (5 pts):** ¿Qué estados puede tener un pedido? ¿Cómo se cambian? ¿Quién puede cambiarlos?

**Tu respuesta:**
```
(escribe aquí)


```

---

### G.2 Si elegiste Sistema de Citas:

**Pregunta 25b (5 pts):** ¿Cómo funciona el sistema de horarios disponibles? Explica la relación entre Profesional, HorarioDisponible y Cita.

**Tu respuesta:**
```
(escribe aquí)


```

**Pregunta 26b (5 pts):** ¿Qué roles existen en el sistema? Explica qué puede hacer cada rol (admin, profesional, cliente).

**Tu respuesta:**
```
(escribe aquí)


```

---

### G.3 Si elegiste Publicidad en Aeropuertos:

**Pregunta 25c (5 pts):** ¿Cómo se relacionan Aeropuerto, EspacioPublicitario, Campana y Contrato? Dibuja o describe la cadena de relaciones.

**Tu respuesta:**
```
(escribe aquí)


```

**Pregunta 26c (5 pts):** ¿Qué es un código IATA? ¿Qué tipos de espacios publicitarios existen y dónde se definen en el código?

**Tu respuesta:**
```
(escribe aquí)


```

---

## PARTE H: Análisis y Pensamiento Crítico (10 pts - BONO)

### Pregunta 27 (5 pts)
¿Qué pasaría si dos usuarios intentan comprar el último producto al mismo tiempo? ¿Cómo se podría resolver ese problema?

**Tu respuesta:**
```
(escribe aquí)


```

---

### Pregunta 28 (5 pts)
Si tuvieras que agregar una funcionalidad de **búsqueda** al proyecto, ¿qué cambios harías? Describe las rutas, queries y templates que necesitarías.

**Tu respuesta:**
```
(escribe aquí)


```

---

## PARTE I: Ejercicio Práctico (20 pts)

> El evaluador elegirá UNO de los siguientes ejercicios para que el estudiante lo realice en vivo.

| #   | Ejercicio                                                                         |
|-----|-----------------------------------------------------------------------------------|
| 1   | Agrega un campo `telefono` al modelo `Usuario` y muéstralo en el registro         |
| 2   | Crea una ruta `/acerca` que muestre una página estática "Acerca de nosotros"      |
| 3   | Agrega una nueva columna a una tabla existente en un template                     |
| 4   | Agrega una validación: que el email contenga `@` antes de crear la cuenta         |
| 5   | Cambia el color principal del tema CSS modificando la variable en `:root`          |
| 6   | Agrega un nuevo registro (producto/servicio/aeropuerto) desde el panel de admin   |
| 7   | Crea un nuevo modelo simple con al menos 3 campos y su ruta de listado            |
| 8   | Agrega un contador nuevo en el dashboard de admin                                 |

**Ejercicio asignado:** #____

**Resultado:** [ ] Completado  [ ] Parcialmente completado  [ ] No completado

**Observaciones del evaluador:**
```
(espacio para el evaluador)


```

---

## Resumen de Calificación

| Sección                              | Puntos Posibles | Puntos Obtenidos |
|--------------------------------------|:---------------:|:----------------:|
| A. Python Básico                     |       20        |                  |
| B. Funciones y POO                   |       20        |                  |
| C. Base de Datos y SQL               |       20        |                  |
| D. Flask y Rutas                     |       20        |                  |
| E. Autenticación y Seguridad         |       20        |                  |
| F. Templates y Frontend              |       10        |                  |
| G. Preguntas del Proyecto            |       10        |                  |
| H. Análisis Crítico (BONO)          |       10        |                  |
| I. Ejercicio Práctico                |       20        |                  |
| **TOTAL**                            |  **140 (+ 10)** |                  |

**Nota final (sobre 100):** _____ / 100

**Firma del evaluador:** _______________________________________________
