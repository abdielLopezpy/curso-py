# Semana 5: Objetos JSON y Persistencia de Datos

Bienvenido a la Semana 5 del curso. Esta semana está dedicada a aprender cómo trabajar con archivos JSON y crear sistemas completos de gestión de datos que persistan información en disco.

---

## 🎯 Objetivos de Aprendizaje

Al finalizar esta semana serás capaz de:

✅ Entender qué es JSON y por qué es importante
✅ Serializar y deserializar datos entre Python y JSON
✅ Crear y gestionar archivos JSON en disco
✅ Diseñar entidades usando `@dataclass`
✅ Implementar operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
✅ Relacionar múltiples entidades en un sistema
✅ Construir un sistema completo de gestión con persistencia en JSON

---

## 📁 Estructura del Proyecto

```
Semana_5/
├── README_SEMANA_5.md              👈 Este archivo
├── CONCEPTOS_CLAVE.md              👈 Explicación de @dataclass, herencia, type hints, etc.
│
├── framework/                      📦 FRAMEWORK (infraestructura lista para usar)
│   └── database_framework.py       👈 Sistema completo de gestión de datos JSON
│
├── ejemplo/                        📖 EJEMPLO COMPLETO
│   └── ejemplo_tienda.py           👈 Sistema de tienda con productos, clientes y ventas
│
├── desafio/                        🎯 TU DESAFÍO
│   ├── DESAFIO_README.md           👈 Instrucciones paso a paso del desafío
│   └── DESAFIO.py                  👈 Aquí trabajarás tu desafío
│
├── datos/                          💾 Archivos JSON generados
│   ├── tienda_ejemplo/             👈 Datos del ejemplo
│   └── [tu_sistema]/               👈 Tus datos se guardarán aquí
│
└── [Archivos de semanas anteriores para compatibilidad]
    ├── json_basics.py
    ├── json_db_simulator.py
    └── ...
```

---

## 📚 1. ¿Qué es JSON?

**JSON** (JavaScript Object Notation) es un formato de texto ligero para intercambiar datos. Es el formato estándar de facto en la web y en aplicaciones modernas.

### Características de JSON

- ✅ **Legible**: Fácil de leer para humanos y máquinas
- ✅ **Universal**: Compatible con todos los lenguajes de programación
- ✅ **Ligero**: No tiene sobrecarga innecesaria
- ✅ **Estructurado**: Soporta objetos anidados y listas

### Ejemplo de JSON

```json
{
  "id": 1,
  "nombre": "Ana García",
  "edad": 25,
  "activo": true,
  "hobbies": ["leer", "programar", "viajar"],
  "direccion": {
    "ciudad": "Bogotá",
    "pais": "Colombia"
  }
}
```

### Tipos de Datos en JSON

| Tipo JSON | Tipo Python | Ejemplo |
|-----------|-------------|---------|
| `string` | `str` | `"Hola"` |
| `number` | `int` / `float` | `42`, `3.14` |
| `boolean` | `bool` | `true`, `false` |
| `null` | `None` | `null` |
| `array` | `list` | `[1, 2, 3]` |
| `object` | `dict` | `{"nombre": "Ana"}` |

---

## 🔄 2. JSON en Python

Python incluye el módulo `json` en su biblioteca estándar para trabajar con JSON.

### Serialización (Python → JSON)

```python
import json

# Diccionario de Python
datos = {
    "nombre": "Ana",
    "edad": 25,
    "activo": True
}

# Convertir a texto JSON
json_string = json.dumps(datos, indent=2, ensure_ascii=False)
print(json_string)
```

### Deserialización (JSON → Python)

```python
import json

# Texto JSON
json_string = '{"nombre": "Ana", "edad": 25, "activo": true}'

# Convertir a diccionario Python
datos = json.loads(json_string)
print(datos["nombre"])  # Ana
```

### Guardar en Archivo

```python
import json
from pathlib import Path

datos = {"nombre": "Ana", "edad": 25}

# Guardar
with open("datos.json", "w", encoding="utf-8") as archivo:
    json.dump(datos, archivo, indent=2, ensure_ascii=False)
```

### Leer desde Archivo

```python
import json

# Leer
with open("datos.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

print(datos)
```

---

## 🏗️ 3. Framework de Gestión de Datos JSON

Hemos creado un **framework completo** que te permite construir sistemas de gestión con persistencia en JSON sin preocuparte por los detalles técnicos.

### ¿Qué incluye el Framework?

📦 **[framework/database_framework.py](framework/database_framework.py)**

#### Componentes Principales

| Componente | Descripción | Uso |
|------------|-------------|-----|
| `Entidad` | Clase base para tus entidades | Hereda de esta para crear tus modelos |
| `RepositorioJSON` | Maneja operaciones CRUD | Crea uno por cada entidad |
| `SistemaGestion` | Base para tu sistema | Hereda para crear tu sistema completo |
| `TipoOperacion` | Enum para tipos de operaciones | Para la bitácora |
| Funciones de validación | `validar_no_vacio`, `validar_positivo`, etc. | Para validar datos |

#### Operaciones CRUD Disponibles

El `RepositorioJSON` proporciona:

- ✅ **Create** (Crear): `insertar(entidad)`
- ✅ **Read** (Leer): `consultar_por_id(id)`, `consultar_todos()`, `consultar_por_campo(campo, valor)`
- ✅ **Update** (Actualizar): `actualizar(entidad)`
- ✅ **Delete** (Eliminar): `eliminar(id)`

#### Características Adicionales

- 🔍 **Búsquedas**: Por ID, por campo específico, o todas
- 📊 **Estadísticas**: Contadores, reportes, resúmenes
- 📜 **Bitácora**: Registro automático de todas las operaciones
- ✅ **Validaciones**: Sistema de validación de datos
- 💾 **Persistencia automática**: Los datos se guardan automáticamente en JSON

---

## 📖 4. Ejemplo Completo: Sistema de Tienda

Estudia el ejemplo completo en [ejemplo/ejemplo_tienda.py](ejemplo/ejemplo_tienda.py).

### Qué hace el Ejemplo

El sistema de tienda maneja:
1. **Productos** - Catálogo de productos con inventario
2. **Clientes** - Base de datos de clientes
3. **Ventas** - Registro de transacciones que relaciona productos y clientes

### Cómo Ejecutarlo

```bash
# Desde la raíz del curso
python3 Semana_5/ejemplo/ejemplo_tienda.py
```

### Qué Observar

Después de ejecutar, revisa:
1. **Consola**: Salida formateada mostrando operaciones
2. **Carpeta datos/tienda_ejemplo/**: Archivos JSON generados
   - `productos.json` - Catálogo de productos
   - `productos_bitacora.json` - Historial de operaciones sobre productos
   - `clientes.json` - Base de clientes
   - `clientes_bitacora.json` - Historial de operaciones sobre clientes
   - `ventas.json` - Registro de ventas
   - `ventas_bitacora.json` - Historial de ventas

### Estructura del Ejemplo

```python
# 1. Definir Entidades
@dataclass
class Producto(Entidad):
    id: int
    nombre: str
    precio: float
    stock: int
    # ... métodos ...

# 2. Crear Sistema
class SistemaTienda(SistemaGestion):
    def __init__(self):
        super().__init__("tienda_ejemplo")
        self.productos = RepositorioJSON("productos", Producto, self.directorio_datos)
        self.clientes = RepositorioJSON("clientes", Cliente, self.directorio_datos)
        self.ventas = RepositorioJSON("ventas", Venta, self.directorio_datos)

    # 3. Implementar operaciones
    def registrar_venta(self, producto_id, cliente_id, cantidad):
        # Lógica que relaciona productos, clientes y ventas
        pass
```

---

## 🎯 5. DESAFÍO: Crea tu Propio Sistema

Es hora de poner en práctica lo aprendido. Tu desafío es crear un sistema completo con 3 entidades relacionadas.

### Instrucciones Completas

📋 **Lee**: [desafio/DESAFIO_README.md](desafio/DESAFIO_README.md)

Contiene:
- ✅ Instrucciones paso a paso
- ✅ Ejemplos de código
- ✅ Checklist de verificación
- ✅ Criterios de evaluación
- ✅ Solución de problemas

### Archivo de Trabajo

✏️ **Trabaja en**: [desafio/DESAFIO.py](desafio/DESAFIO.py)

Ya tiene:
- ✅ Estructura base lista
- ✅ Comentarios TODO indicando qué hacer
- ✅ Ejemplos comentados
- ✅ Checklist final

### Ideas de Sistemas

Elige uno o inventa el tuyo:

| Sistema | Entidades |
|---------|-----------|
| 🏥 Hospital | Doctores, Pacientes, Citas |
| 📚 Biblioteca | Libros, Usuarios, Préstamos |
| 🎓 Escuela | Estudiantes, Profesores, Cursos |
| 🍕 Restaurante | Platillos, Ingredientes, Pedidos |
| 🏨 Hotel | Habitaciones, Huéspedes, Reservaciones |
| 🚗 Renta de Autos | Vehículos, Clientes, Rentas |
| 💪 Gimnasio | Miembros, Entrenadores, Clases |
| 🎬 Cine | Películas, Salas, Funciones |

### Requisitos del Desafío

Tu sistema debe:

1. ✅ Definir 3 entidades usando `@dataclass`
2. ✅ Cada entidad con al menos 4 campos
3. ✅ Implementar validaciones en cada entidad
4. ✅ Crear repositorios para las 3 entidades
5. ✅ Implementar operaciones CRUD básicas
6. ✅ Crear al menos UN método que relacione las entidades
7. ✅ Agregar datos de ejemplo (mínimo 3 de cada tipo)
8. ✅ Demostrar que los datos se guardan en JSON
9. ✅ Código bien documentado y organizado

### Cómo Ejecutar tu Desafío

```bash
# Desde la raíz del curso
python3 Semana_5/desafio/DESAFIO.py
```

---

## 📚 6. Conceptos Clave

Si tienes dudas sobre los conceptos de Python que usamos esta semana, consulta:

📖 **[CONCEPTOS_CLAVE.md](CONCEPTOS_CLAVE.md)**

Explica en detalle:

- ✅ **@dataclass** - Qué es y por qué usarlo
- ✅ **Clases y Objetos** - Conceptos fundamentales
- ✅ **Herencia** - Reutilización de código
- ✅ **Clases Abstractas (ABC)** - Plantillas obligatorias
- ✅ **Type Hints** - Anotaciones de tipo
- ✅ **@classmethod** - Métodos de clase
- ✅ **Genéricos (Generic)** - Tipos parametrizados
- ✅ **Enumeraciones (Enum)** - Constantes con nombre

Cada concepto incluye:
- 📝 Explicación simple
- 💡 Ejemplos prácticos
- ✅ Cuándo usarlo
- ⚠️ Cuándo NO usarlo

---

## 🚀 7. Ruta de Aprendizaje Sugerida

Sigue este orden para aprovechar al máximo la semana:

### Día 1-2: Fundamentos
1. ✅ Lee la sección "¿Qué es JSON?" de este README
2. ✅ Lee la sección "JSON en Python"
3. ✅ Ejecuta y estudia `json_basics.py`
4. ✅ Lee la sección de `@dataclass` en [CONCEPTOS_CLAVE.md](CONCEPTOS_CLAVE.md)

### Día 3-4: Estudiar el Framework y Ejemplo
1. ✅ Lee la documentación en [framework/database_framework.py](framework/database_framework.py)
2. ✅ Ejecuta [ejemplo/ejemplo_tienda.py](ejemplo/ejemplo_tienda.py)
3. ✅ Revisa los archivos JSON generados en `datos/tienda_ejemplo/`
4. ✅ Estudia el código del ejemplo línea por línea
5. ✅ Lee otros conceptos en [CONCEPTOS_CLAVE.md](CONCEPTOS_CLAVE.md) según necesites

### Día 5-7: Completar el Desafío
1. ✅ Lee [desafio/DESAFIO_README.md](desafio/DESAFIO_README.md) completo
2. ✅ Decide qué sistema vas a crear
3. ✅ Define tus 3 entidades en [desafio/DESAFIO.py](desafio/DESAFIO.py)
4. ✅ Implementa tu sistema paso a paso
5. ✅ Prueba que todo funcione
6. ✅ Verifica el checklist final
7. ✅ Revisa los archivos JSON generados

---

## 🔍 8. Comparación con Bases de Datos Reales

Lo que aprendes esta semana es **muy similar** a cómo funcionan las bases de datos reales:

| Concepto de la Semana | Equivalente Real |
|-----------------------|------------------|
| Archivo JSON | Tabla en base de datos |
| Entidad (@dataclass) | Modelo/Schema |
| RepositorioJSON | ORM (Object-Relational Mapping) |
| CRUD operations | SQL queries |
| Bitácora | Transaction logs |
| campos `*_id` | Foreign keys |
| `consultar_por_campo()` | WHERE clause |

### Tecnologías Profesionales Similares

Lo que construyes esta semana se parece a:

- 🗄️ **SQLAlchemy** (Python ORM)
- 🗄️ **Django ORM** (Framework web)
- 🗄️ **MongoDB** (Base de datos NoSQL con documentos JSON)
- 🗄️ **Firebase Firestore** (Base de datos en la nube)
- 🗄️ **TinyDB** (Base de datos JSON para Python)

---

## 📊 9. Usos de JSON en el Mundo Real

### APIs REST
```python
# Respuesta típica de una API
{
  "status": "success",
  "data": {
    "user_id": 12345,
    "name": "Ana García",
    "email": "ana@example.com"
  }
}
```

### Archivos de Configuración
```json
{
  "app_name": "Mi Aplicación",
  "version": "1.0.0",
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "mi_db"
  },
  "features": {
    "debug_mode": false,
    "max_users": 1000
  }
}
```

### Bases de Datos NoSQL
```javascript
// MongoDB documento
{
  "_id": ObjectId("507f1f77bcf86cd799439011"),
  "producto": "Laptop",
  "precio": 1200.00,
  "especificaciones": {
    "ram": "16GB",
    "procesador": "Intel i7"
  },
  "tags": ["electrónica", "computadoras"]
}
```

### Data Science
```python
# pandas puede leer/escribir JSON
import pandas as pd

df = pd.read_json("datos.json")
df.to_json("salida.json", orient="records", indent=2)
```

---

## 💡 10. Tips y Mejores Prácticas

### Al Trabajar con JSON

✅ **Siempre usa `encoding="utf-8"`** para caracteres especiales
```python
with open("datos.json", "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, indent=2)
```

✅ **Usa `ensure_ascii=False`** para mantener acentos y ñ
```python
json.dumps(datos, ensure_ascii=False)  # ✅ "niño"
json.dumps(datos)  # ❌ "ni\u00f1o"
```

✅ **Usa `indent=2`** para archivos legibles
```python
json.dumps(datos, indent=2)  # ✅ Bien formateado
```

✅ **Valida datos antes de guardar**
```python
if entidad.validar():
    repositorio.insertar(entidad)
```

### Al Diseñar Entidades

✅ **Usa nombres descriptivos**
```python
# ✅ Bien
@dataclass
class Cliente:
    id: int
    nombre_completo: str
    fecha_registro: str

# ❌ Mal
@dataclass
class C:
    i: int
    n: str
    d: str
```

✅ **Documenta tus clases**
```python
@dataclass
class Producto:
    """Representa un producto en el catálogo.

    Attributes:
        id: Identificador único
        nombre: Nombre del producto
        precio: Precio en la moneda local
    """
```

✅ **Valida siempre**
```python
def validar(self) -> bool:
    if not validar_no_vacio(self.nombre, "nombre"):
        return False
    if not validar_positivo(self.precio, "precio"):
        return False
    return True
```

### Al Implementar Operaciones

✅ **Verifica que las entidades existan antes de relacionarlas**
```python
def crear_orden(self, producto_id, cliente_id):
    producto = self.buscar_producto(producto_id)
    if producto is None:
        print("❌ Producto no encontrado")
        return False
    # ... continuar
```

✅ **Actualiza todas las entidades relacionadas**
```python
def vender_producto(self, producto_id, cantidad):
    # Crear venta
    venta = Venta(...)
    self.ventas.insertar(venta)

    # Actualizar stock
    producto.stock -= cantidad
    self.productos.actualizar(producto)  # ⬅️ No olvides esto
```

✅ **Proporciona feedback al usuario**
```python
print(f"✅ Operación exitosa")
print(f"❌ Error: {mensaje}")
print(f"💰 Total: ${monto}")
```

---

## 🆘 11. Solución de Problemas

### Error: "FileNotFoundError"

**Causa**: El archivo o carpeta no existe

**Solución**:
```python
from pathlib import Path

ruta = Path("datos/archivo.json")
ruta.parent.mkdir(parents=True, exist_ok=True)  # Crea carpetas si no existen
```

### Error: "JSONDecodeError"

**Causa**: El archivo JSON está mal formado

**Solución**:
1. Abre el archivo JSON en un editor
2. Verifica que tenga sintaxis válida
3. Usa un validador JSON online: https://jsonlint.com/

### Error: "ModuleNotFoundError: No module named 'database_framework'"

**Causa**: Python no encuentra el módulo

**Solución**: Ejecuta desde la raíz del curso:
```bash
# ✅ Correcto
python3 Semana_5/ejemplo/ejemplo_tienda.py

# ❌ Incorrecto
cd Semana_5/ejemplo
python3 ejemplo_tienda.py
```

### Los datos no se guardan

**Verifica**:
1. ✅ ¿Llamas a `.insertar()` o `.actualizar()`?
2. ✅ ¿Los datos pasan las validaciones?
3. ✅ ¿Tienes permisos de escritura?
4. ✅ ¿La carpeta existe?

---

## 📚 12. Recursos Adicionales

### Documentación Oficial

- [Módulo json de Python](https://docs.python.org/3/library/json.html)
- [dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [typing](https://docs.python.org/3/library/typing.html)

### Tutoriales y Guías

- [JSON.org](https://www.json.org/json-es.html) - Especificación oficial
- [Real Python: Working with JSON](https://realpython.com/python-json/)
- [Real Python: Data Classes](https://realpython.com/python-data-classes/)

### Herramientas Útiles

- [JSONLint](https://jsonlint.com/) - Validador de JSON
- [JSON Formatter](https://jsonformatter.org/) - Formatea JSON
- [QuickType](https://quicktype.io/) - Genera clases desde JSON

---

## 🎓 13. Próximos Pasos

Después de completar esta semana, estarás listo para:

1. **Semanas siguientes**: Aplicar estos conceptos en proyectos más grandes
2. **Bases de datos reales**: SQLite, PostgreSQL, MongoDB
3. **APIs**: Crear servicios web que consuman y produzcan JSON
4. **ORMs**: Django ORM, SQLAlchemy, Peewee
5. **Frameworks web**: FastAPI, Flask, Django

---

## ✅ Checklist de la Semana

Marca lo que has completado:

### Teoría
- [ ] Entiendes qué es JSON y para qué sirve
- [ ] Sabes serializar y deserializar JSON en Python
- [ ] Comprendes qué es `@dataclass`
- [ ] Entiendes el concepto de herencia
- [ ] Conoces las operaciones CRUD

### Práctica
- [ ] Ejecutaste y estudiaste `json_basics.py`
- [ ] Ejecutaste y estudiaste `ejemplo_tienda.py`
- [ ] Revisaste los archivos JSON generados
- [ ] Completaste el desafío con tus 3 entidades
- [ ] Tu sistema guarda datos en JSON correctamente
- [ ] Implementaste validaciones
- [ ] Creaste operaciones que relacionan entidades

### Documentación
- [ ] Leíste [CONCEPTOS_CLAVE.md](CONCEPTOS_CLAVE.md)
- [ ] Leíste [desafio/DESAFIO_README.md](desafio/DESAFIO_README.md)
- [ ] Documentaste tu código con docstrings
- [ ] Tus nombres de variables son descriptivos

---

## 📞 Soporte

Si tienes dudas o problemas:

1. 📖 Consulta [CONCEPTOS_CLAVE.md](CONCEPTOS_CLAVE.md)
2. 👀 Revisa el [ejemplo completo](ejemplo/ejemplo_tienda.py)
3. 📋 Lee las [instrucciones del desafío](desafio/DESAFIO_README.md)
4. 🔍 Busca en la documentación oficial de Python
5. 💬 Pregunta a tu instructor

---

**¡Éxito en tu aprendizaje! 🚀**

> "JSON es el puente entre tu código Python y el mundo exterior; dominarlo significa hablar el idioma universal del intercambio de datos."

---

**Última actualización**: 2025
