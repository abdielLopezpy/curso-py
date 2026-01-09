# Semana 6: Introducción a SQL y SQLite con Python

Bienvenido a la Semana 6 del curso. Esta semana aprenderás a trabajar con bases de datos SQL usando SQLite, la base de datos incluida en Python.

---

## 🎯 Objetivos de Aprendizaje

Al finalizar esta semana serás capaz de:

✅ Entender qué es SQL y para qué sirve  
✅ Conocer los conceptos básicos de bases de datos relacionales  
✅ Crear y gestionar bases de datos SQLite con Python  
✅ Ejecutar consultas CRUD (Crear, Leer, Actualizar, Eliminar)  
✅ Diseñar tablas con claves primarias y foráneas  
✅ Relacionar tablas usando JOINs  
✅ Construir un sistema completo con persistencia en SQLite  

---

## 📁 Estructura del Proyecto

```
Semana_6/
├── README_SEMANA_6.md              👈 Este archivo
├── CONCEPTOS_SQL.md                👈 Explicación de conceptos SQL
│
├── 01_intro_sqlite.py              📖 Paso 1: Introducción a SQLite
├── 02_crear_tablas.py              📖 Paso 2: Crear tablas
├── 03_insertar_datos.py            📖 Paso 3: Insertar datos (INSERT)
├── 04_consultar_datos.py           📖 Paso 4: Consultar datos (SELECT)
├── 05_actualizar_eliminar.py       📖 Paso 5: Actualizar y eliminar (UPDATE/DELETE)
├── 06_relaciones_joins.py          📖 Paso 6: Relaciones y JOINs
├── 07_sistema_completo.py          📖 Paso 7: Sistema completo integrado
│
├── quiz_semana_6.py                🎮 Quiz interactivo
├── ejercicios_sqlite.py            ✏️ Ejercicios prácticos
│
└── datos/                          💾 Bases de datos SQLite generadas
    └── [archivos .db se crean aquí]
```

---

## 📚 ¿Qué es SQL?

**SQL** (Structured Query Language) es el lenguaje estándar para comunicarse con bases de datos relacionales. Es como "hablar" con la base de datos para pedirle que guarde, busque, modifique o elimine información.

### ¿Por qué SQL es importante?

| Característica | Beneficio |
|---------------|-----------|
| **Universal** | Funciona en MySQL, PostgreSQL, SQLite, SQL Server, etc. |
| **Potente** | Puede manejar millones de registros eficientemente |
| **Estructurado** | Los datos están organizados en tablas con relaciones |
| **Seguro** | Soporta transacciones y control de acceso |
| **Persistente** | Los datos se guardan en disco permanentemente |

---

## 🗄️ ¿Qué es SQLite?

**SQLite** es una base de datos ligera que:

- ✅ **Viene incluida en Python** - No necesitas instalar nada extra
- ✅ **Guarda todo en un archivo** - Un solo archivo `.db` contiene toda la base de datos
- ✅ **Es perfecta para aprender** - Misma sintaxis SQL que bases de datos grandes
- ✅ **Es usada en producción** - Navegadores, apps móviles, sistemas embebidos

```python
import sqlite3  # ¡Ya viene con Python!
```

---

## 🔤 Conceptos Básicos de Bases de Datos

### 1. Base de Datos
Un contenedor que almacena información organizada. En SQLite, es un archivo `.db`.

### 2. Tabla
Una estructura que organiza datos en filas y columnas, como una hoja de Excel.

```
┌─────────────────────────────────────────┐
│              TABLA: usuarios            │
├────┬──────────────┬───────┬─────────────┤
│ id │    nombre    │ edad  │   email     │
├────┼──────────────┼───────┼─────────────┤
│ 1  │ Ana García   │  25   │ ana@mail.com│
│ 2  │ Luis Pérez   │  30   │ luis@mail.com│
│ 3  │ María López  │  22   │ maria@mail.com│
└────┴──────────────┴───────┴─────────────┘
```

### 3. Columna (Campo)
Define el tipo de dato que se almacena: nombre, edad, email, etc.

### 4. Fila (Registro)
Una entrada individual en la tabla. Cada usuario es una fila.

### 5. Clave Primaria (Primary Key)
Un identificador único para cada fila. Generalmente es el `id`.

### 6. Clave Foránea (Foreign Key)
Una columna que conecta una tabla con otra.

---

## 🛠️ Operaciones CRUD

CRUD son las 4 operaciones básicas que puedes hacer con datos:

| Operación | SQL | Descripción |
|-----------|-----|-------------|
| **C**reate | `INSERT` | Crear nuevos registros |
| **R**ead | `SELECT` | Leer/consultar registros |
| **U**pdate | `UPDATE` | Modificar registros existentes |
| **D**elete | `DELETE` | Eliminar registros |

---

## 📝 Sintaxis SQL Básica

### Crear una tabla
```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER,
    email TEXT UNIQUE
);
```

### Insertar datos
```sql
INSERT INTO usuarios (nombre, edad, email) 
VALUES ('Ana García', 25, 'ana@mail.com');
```

### Consultar datos
```sql
-- Todos los registros
SELECT * FROM usuarios;

-- Con filtro
SELECT nombre, edad FROM usuarios WHERE edad >= 18;

-- Ordenado
SELECT * FROM usuarios ORDER BY nombre ASC;
```

### Actualizar datos
```sql
UPDATE usuarios SET edad = 26 WHERE id = 1;
```

### Eliminar datos
```sql
DELETE FROM usuarios WHERE id = 1;
```

---

## 🔗 Conexión Python + SQLite

```python
import sqlite3

# 1. Conectar a la base de datos (se crea si no existe)
conexion = sqlite3.connect('mi_base_datos.db')

# 2. Crear un cursor para ejecutar comandos
cursor = conexion.cursor()

# 3. Ejecutar una consulta SQL
cursor.execute("SELECT * FROM usuarios")

# 4. Obtener resultados
resultados = cursor.fetchall()

# 5. Confirmar cambios (para INSERT, UPDATE, DELETE)
conexion.commit()

# 6. Cerrar conexión
conexion.close()
```

---

## 🚀 Orden de Estudio Recomendado

Sigue estos archivos en orden:

1. **`01_intro_sqlite.py`** - Tu primera conexión a SQLite
2. **`02_crear_tablas.py`** - Crear estructura de tablas
3. **`03_insertar_datos.py`** - Agregar registros
4. **`04_consultar_datos.py`** - Buscar y filtrar datos
5. **`05_actualizar_eliminar.py`** - Modificar y borrar
6. **`06_relaciones_joins.py`** - Conectar tablas
7. **`07_sistema_completo.py`** - Proyecto integrado

Después:
- **`ejercicios_sqlite.py`** - Practica lo aprendido
- **`quiz_semana_6.py`** - Evalúa tu conocimiento

---

## 💡 Tips para Principiantes

### 1. Siempre cierra la conexión
```python
conexion.close()
```
O mejor, usa `with`:
```python
with sqlite3.connect('datos.db') as conexion:
    cursor = conexion.cursor()
    # ... tus operaciones aquí
# Se cierra automáticamente
```

### 2. Usa parámetros para evitar inyección SQL
```python
# ❌ MAL - Vulnerable
cursor.execute(f"SELECT * FROM usuarios WHERE id = {id_usuario}")

# ✅ BIEN - Seguro
cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id_usuario,))
```

### 3. Confirma los cambios con commit()
```python
cursor.execute("INSERT INTO usuarios ...")
conexion.commit()  # ¡Sin esto, no se guarda!
```

### 4. Maneja errores con try/except
```python
try:
    cursor.execute("...")
    conexion.commit()
except sqlite3.Error as error:
    print(f"Error: {error}")
```

---

## 🎮 ¡Comienza Ahora!

Abre el archivo `01_intro_sqlite.py` y ejecuta:

```bash
cd Semana_6
python 01_intro_sqlite.py
```

¡Buena suerte! 🚀
