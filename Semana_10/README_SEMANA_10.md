# ============================================================================
# SEMANA 10: Proyectos de Evaluación Final
# ============================================================================

## Objetivo

La Semana 10 es la **evaluación final del curso**. El estudiante debe elegir
**uno de los tres proyectos** disponibles, estudiarlo, comprenderlo y ser capaz
de explicar cada parte del código.

Cada proyecto es una **aplicación web completa** que integra todos los conceptos
aprendidos durante el curso:

| Semana | Concepto                        | Aplicado en los proyectos              |
|--------|---------------------------------|----------------------------------------|
| 1-3    | Variables, funciones, lógica    | Lógica de negocio en cada ruta         |
| 4-5    | Estructuras de datos, POO       | Modelos SQLAlchemy (clases)            |
| 6-7    | Módulos, archivos, SQL          | Queries, relaciones entre tablas       |
| 8      | CRUD con Flask                  | Operaciones completas en cada entidad  |
| 9      | Autenticación y seguridad       | Login, sesiones, roles, decoradores    |
| **10** | **Proyecto integrador**         | **Todo lo anterior en un sistema real**|

---

## Los 3 Proyectos

### 1. Mini Tienda E-Commerce (`01_ecommerce/`)

**Tema:** Tienda en línea con catálogo, carrito de compras y pedidos.

**Modelos:**
- `Usuario` - Autenticación con roles (admin/usuario)
- `Categoria` - Organización de productos
- `Producto` - Artículos con precio, stock e imagen
- `Carrito` / `ItemCarrito` - Carrito de compras por usuario
- `Pedido` / `ItemPedido` - Órdenes con estados de seguimiento

**Funcionalidades clave:**
- Catálogo de productos con filtro por categoría
- Carrito de compras (agregar, actualizar, eliminar)
- Proceso de checkout con dirección de envío
- Historial de pedidos con estados
- Panel de administración para productos y pedidos

**Ejecutar:** `python app.py` → http://localhost:5010

---

### 2. Sistema de Citas (`02_sistema_citas/`)

**Tema:** Plataforma de agendamiento de citas para clientes.

**Modelos:**
- `Usuario` - Autenticación con roles (admin/profesional/cliente)
- `Servicio` - Servicios ofrecidos con duración y precio
- `Profesional` - Profesionales que atienden las citas
- `HorarioDisponible` - Horarios de atención por profesional
- `Cita` - Citas agendadas con estado de seguimiento

**Funcionalidades clave:**
- Catálogo de servicios con precios y duración
- Selección de profesional, fecha y hora disponible
- Gestión de citas (agendar, ver, cancelar)
- Panel admin: gestionar servicios, profesionales, horarios y citas
- Dashboard con citas del día y próximas

**Ejecutar:** `python app.py` → http://localhost:5011

---

### 3. Publicidad en Aeropuertos (`03_publicidad_aeropuertos/`)

**Tema:** Plataforma B2B para contratar espacios publicitarios en aeropuertos.

**Modelos:**
- `Usuario` - Autenticación con roles (admin/cliente) + empresa
- `Aeropuerto` - Aeropuertos con código IATA y tráfico de pasajeros
- `EspacioPublicitario` - Espacios disponibles (pantallas, vallas, banners, etc.)
- `Campana` - Campañas publicitarias del cliente
- `Contrato` - Contratos de un espacio para una campaña

**Funcionalidades clave:**
- Directorio de aeropuertos con estadísticas de tráfico
- Catálogo de espacios publicitarios con filtros
- Creación de campañas publicitarias
- Contratación de espacios para campañas
- Panel admin: gestión completa de aeropuertos, espacios y contratos

**Ejecutar:** `python app.py` → http://localhost:5012

---

## Credenciales por Defecto

Todos los proyectos crean automáticamente un usuario administrador:

| Campo    | Valor              |
|----------|--------------------|
| Email    | admin@ejemplo.com  |
| Password | admin123           |

---

## Cómo Evaluar

### El estudiante debe ser capaz de:

1. **Explicar la estructura** del proyecto elegido
   - ¿Qué hace cada modelo y cómo se relacionan?
   - ¿Qué rutas existen y qué hace cada una?

2. **Explicar conceptos de autenticación**
   - ¿Cómo funciona el hashing de contraseñas?
   - ¿Qué hace el decorador `@login_required`?
   - ¿Cómo funcionan las sesiones de Flask?

3. **Explicar el CRUD**
   - ¿Qué es GET vs POST?
   - ¿Cómo se crea/lee/actualiza/elimina un registro?
   - ¿Cómo se manejan los errores?

4. **Explicar las relaciones entre tablas**
   - ¿Qué es una clave foránea (FK)?
   - ¿Cómo funciona la relación one-to-many?
   - ¿Qué es CASCADE en las relaciones?

5. **Hacer una modificación en vivo**
   - Agregar un campo nuevo a un modelo
   - Crear una nueva ruta simple
   - Modificar un template existente

---

## Banco de Preguntas para Evaluación

A continuación se presentan preguntas organizadas por tema. El evaluador puede
seleccionar entre 10 y 20 preguntas según el nivel deseado.

### A. Python Básico (Semanas 1-3)

1. ¿Qué es una variable? Muéstrame un ejemplo en el código del proyecto.
2. ¿Qué diferencia hay entre un `string`, un `int` y un `float`? Señala uno de cada tipo en el código.
3. ¿Qué hace la instrucción `if not nombre:`? ¿Cuándo se ejecuta?
4. ¿Para qué sirve un `for` loop? Encuentra un ejemplo en el proyecto y explícalo.
5. ¿Qué hace `.strip()` cuando se aplica a un string? ¿Por qué se usa en los formularios?
6. ¿Qué diferencia hay entre `=` y `==`?
7. ¿Qué hace `return` en una función? ¿Qué pasa si una función no tiene `return`?
8. ¿Qué hace `f'Bienvenido, {usuario.nombre}!'`? ¿Cómo se llama esa técnica?
9. ¿Qué es un diccionario en Python? Señala uno en el código y explica su uso.
10. ¿Qué hace el método `.get()` en un diccionario? ¿Por qué es mejor que usar `[]`?

### B. Funciones y Programación Orientada a Objetos (Semanas 4-5)

11. ¿Qué es una clase en Python? Señala una clase del proyecto y explica sus partes.
12. ¿Qué es `self` dentro de una clase? ¿Por qué es necesario?
13. ¿Qué es un método? ¿En qué se diferencia de una función normal?
14. ¿Qué es una `@property`? Busca un ejemplo en el proyecto y explica qué hace.
15. ¿Para qué sirve `__tablename__` en los modelos?
16. ¿Qué hace `def set_password(self, password):`? ¿Por qué no se guarda la contraseña directamente?
17. ¿Qué es un decorador (`@algo`)? Explica qué hace `@app.route('/login')`.
18. ¿Qué es la herencia en Python? ¿Cuál es la clase "padre" de todos los modelos del proyecto?
19. ¿Qué significa `Column(Integer, primary_key=True)`? ¿Qué pasa con el valor de `id`?
20. ¿Qué es un constructor `__init__`? ¿Cómo lo maneja SQLAlchemy automáticamente?

### C. SQL y Base de Datos (Semanas 6-7)

21. ¿Qué es una base de datos relacional? ¿Qué base de datos usa este proyecto?
22. ¿Qué hace `create_engine(DATABASE_URL)`? ¿Qué información contiene la URL?
23. ¿Qué hace `Base.metadata.create_all(engine)`?
24. ¿Qué es una clave primaria (Primary Key)? ¿Para qué sirve?
25. ¿Qué es una clave foránea (Foreign Key)? Señala una en el código y explica la relación.
26. ¿Qué hace `db.query(Producto).filter(Producto.activo == True).all()`? Tradúcelo a SQL.
27. ¿Qué diferencia hay entre `.all()`, `.first()` y `.get(id)`?
28. ¿Qué hace `db.add(producto)`? ¿Y `db.commit()`? ¿Por qué son pasos separados?
29. ¿Qué pasa si llamas `db.commit()` y hay un error? ¿Para qué sirve `db.rollback()`?
30. ¿Qué hace `db.flush()` y cuándo se usa? ¿En qué se diferencia de `commit()`?
31. ¿Qué es `relationship()` en SQLAlchemy? ¿En qué se diferencia de `ForeignKey`?
32. ¿Qué significa `cascade="all, delete-orphan"` en una relación?
33. ¿Qué hace `scoped_session`? ¿Por qué es importante en una aplicación web?
34. ¿Qué es una sesión de base de datos? ¿En qué se diferencia de una sesión de Flask?

### D. Flask y Rutas (Semana 8)

35. ¿Qué es Flask? ¿Para qué se usa?
36. ¿Qué hace `@app.route('/productos/<int:id>')`? ¿Qué significa `<int:id>`?
37. ¿Qué diferencia hay entre `methods=['GET']` y `methods=['GET', 'POST']`?
38. ¿Qué hace `request.method == 'POST'`? ¿Cuándo se ejecuta ese bloque?
39. ¿Qué hace `request.form.get('nombre', '')`? ¿Por qué se usa `.get()` en vez de `[]`?
40. ¿Qué hace `redirect(url_for('login'))`? ¿Por qué usar `url_for` en vez de escribir la URL directa?
41. ¿Qué hace `render_template('index.html', productos=productos)`?
42. ¿Qué es `flash()` y para qué se usa? ¿Dónde se muestran los mensajes flash?
43. ¿Qué hace `return redirect(request.referrer or url_for('catalogo'))`?
44. ¿Para qué sirve `app.secret_key`? ¿Qué pasa si no se configura?
45. ¿Qué hace `@app.errorhandler(404)`? ¿Cuándo se ejecuta?
46. ¿Qué hace `@app.teardown_appcontext`?

### E. Autenticación y Seguridad (Semana 9)

47. ¿Qué es el hashing de contraseñas? ¿Por qué no se guardan en texto plano?
48. ¿Qué hace `generate_password_hash()` y `check_password_hash()`?
49. ¿Qué es una sesión en Flask (`session`)? ¿Dónde se almacena?
50. ¿Qué se guarda en `session['usuario_id']` al hacer login?
51. ¿Qué hace `session.clear()` al cerrar sesión?
52. ¿Qué hace el decorador `@login_required`? Explica paso a paso cómo funciona.
53. ¿Qué hace `@admin_required`? ¿En qué se diferencia de `@login_required`?
54. ¿Qué hace `@wraps(f)` dentro del decorador? ¿Qué pasa si no lo usas?
55. ¿Qué es `@app.context_processor`? ¿Para qué se usa en este proyecto?
56. ¿Cómo se verifica que un usuario no pueda ver los pedidos de otro usuario?
57. ¿Qué riesgo hay si no se validan los datos del formulario antes de guardarlos?

### F. Templates Jinja2 y Frontend

58. ¿Qué es Jinja2? ¿Cómo se relaciona con Flask?
59. ¿Qué hace `{% extends "base.html" %}`? ¿Qué es la herencia de templates?
60. ¿Qué diferencia hay entre `{{ variable }}` y `{% instruccion %}`?
61. ¿Qué hace `{% block content %}...{% endblock %}`?
62. ¿Qué es un macro en Jinja2? Busca uno en `macros.html` y explica cómo se usa.
63. ¿Qué hace `{% from "macros.html" import campo_texto %}`?
64. ¿Qué hace `{% for producto in productos %}`? ¿Cómo se cierra el bloque?
65. ¿Qué hace `{% if espacio and espacio.tipo == t %}`?
66. ¿Qué hace el filtro `{{ t|replace('_', ' ')|capitalize }}`?
67. ¿Qué hace `{{ url_for('static', filename='css/styles.css') }}`?
68. ¿Cómo se muestran los mensajes flash en el template `base.html`?

### G. Preguntas Específicas por Proyecto

#### G.1 E-Commerce (01_ecommerce)

69. ¿Cómo funciona el carrito de compras? Explica el flujo desde agregar un producto hasta el checkout.
70. ¿Qué pasa con el stock de un producto cuando se completa un pedido?
71. ¿Qué estados puede tener un pedido? ¿Cómo se cambian desde el panel de admin?
72. ¿Qué es la relación entre Carrito y Usuario? ¿Por qué es one-to-one (`uselist=False`)?
73. ¿Cómo se calcula el total del carrito? Explica la `@property total`.
74. ¿Qué validaciones se hacen antes de crear un pedido en el checkout?
75. ¿Qué pasa si el usuario intenta agregar más unidades de las que hay en stock?

#### G.2 Sistema de Citas (02_sistema_citas)

76. ¿Cómo se define un horario disponible para un profesional?
77. ¿Qué información necesita el usuario para agendar una cita?
78. ¿Qué estados puede tener una cita? ¿Quién puede cambiar el estado?
79. ¿Cómo se muestra la disponibilidad horaria de un profesional?
80. ¿Qué roles existen en este sistema? ¿Qué puede hacer cada uno?
81. ¿Cómo se relacionan Servicio, Profesional y Cita?
82. ¿Qué validación se necesita para que dos citas no se solapen en el mismo horario?

#### G.3 Publicidad en Aeropuertos (03_publicidad_aeropuertos)

83. ¿Qué es un código IATA? ¿Para qué se usa en el sistema?
84. ¿Qué tipos de espacios publicitarios existen? ¿Dónde se definen?
85. ¿Cómo se relacionan Aeropuerto, EspacioPublicitario, Campana y Contrato?
86. ¿Qué es una campaña publicitaria en el contexto de este sistema?
87. ¿Cómo se contrata un espacio para una campaña?
88. ¿Qué significa que un espacio esté "disponible" vs "ocupado"?
89. ¿Cómo se calcula el costo total de un contrato?

### H. Preguntas de Análisis y Pensamiento Crítico

90. ¿Qué pasaría si se cae la conexión a la base de datos a mitad de un `commit()`? ¿Cómo protege el código contra esto?
91. Si quisieras agregar un sistema de búsqueda de productos, ¿qué cambios harías?
92. ¿Cómo agregarías paginación si el catálogo tuviera 10,000 productos?
93. ¿Qué cambiarías para permitir que un producto pertenezca a múltiples categorías (relación many-to-many)?
94. ¿Qué mejoras de seguridad agregarías antes de poner este sistema en producción?
95. ¿Por qué cada proyecto usa un prefijo diferente para las tablas (`ec_`, `citas_`, `pub_`)?
96. ¿Qué ventaja tiene usar `url_for()` en vez de escribir las URLs directamente en los templates?
97. ¿Por qué los tres proyectos comparten la misma estructura de archivos? ¿Qué ventaja tiene esto?
98. ¿Qué pasa si dos usuarios intentan comprar el último producto al mismo tiempo? ¿Cómo se podría resolver?
99. ¿Cómo agregarías una funcionalidad de recuperación de contraseña olvidada?
100. ¿Qué diferencia hay entre autenticación (quién eres) y autorización (qué puedes hacer)? Da ejemplos del proyecto.

### I. Preguntas Prácticas (Modificación en Vivo)

El evaluador puede pedir al estudiante que realice una de estas modificaciones:

101. Agrega un campo `telefono` al modelo `Usuario` y muéstralo en el perfil.
102. Crea una ruta `/acerca` que muestre una página "Acerca de nosotros".
103. Modifica el template de la lista para mostrar una columna adicional.
104. Agrega una validación: que el email contenga `@` antes de crear la cuenta.
105. Cambia el color principal del tema CSS modificando la variable en `:root`.
106. Agrega un nuevo servicio/producto/aeropuerto desde el panel de admin y verifica que aparezca en la lista.
107. Modifica un macro en `macros.html` para que incluya un atributo `placeholder`.
108. Agrega un filtro a una de las listas (ej: filtrar pedidos por estado, citas por fecha).
109. Crea un nuevo modelo simple (ej: `Resena`, `Nota`, `Etiqueta`) con al menos 3 campos.
110. Agrega un contador en el dashboard de admin que muestre una estadística nueva.

---

## Requisitos Previos

```bash
pip install flask sqlalchemy psycopg2-binary werkzeug
```

---

## Estructura de Archivos (cada proyecto)

```
XX_nombre_proyecto/
├── app.py                  ← Aplicación principal (todo el backend)
├── static/
│   └── css/
│       └── styles.css      ← Estilos modernos con CSS variables
└── templates/
    ├── base.html           ← Layout base (navbar, footer, flash messages)
    ├── index.html          ← Página principal / Dashboard
    ├── error.html          ← Página de error
    ├── macros.html         ← Componentes reutilizables (formularios, badges)
    ├── auth/               ← Templates de autenticación
    │   ├── login.html
    │   └── registro.html
    └── [entidades]/        ← Templates por cada entidad del dominio
        ├── lista.html
        ├── formulario.html
        └── detalle.html
```

---

## Conceptos Integrados por Proyecto

| Concepto                  | E-Commerce | Citas | Publicidad |
|---------------------------|:----------:|:-----:|:----------:|
| Modelos SQLAlchemy        |     ✓      |   ✓   |     ✓      |
| Relaciones FK             |     ✓      |   ✓   |     ✓      |
| Hashing de contraseñas    |     ✓      |   ✓   |     ✓      |
| Sesiones Flask            |     ✓      |   ✓   |     ✓      |
| Decoradores (login/admin) |     ✓      |   ✓   |     ✓      |
| CRUD completo             |     ✓      |   ✓   |     ✓      |
| Flash messages            |     ✓      |   ✓   |     ✓      |
| Templates Jinja2          |     ✓      |   ✓   |     ✓      |
| Macros reutilizables      |     ✓      |   ✓   |     ✓      |
| CSS moderno               |     ✓      |   ✓   |     ✓      |
| Diseño responsivo         |     ✓      |   ✓   |     ✓      |
| Datos de ejemplo          |     ✓      |   ✓   |     ✓      |
| Manejo de errores         |     ✓      |   ✓   |     ✓      |
| Context processors        |     ✓      |   ✓   |     ✓      |
