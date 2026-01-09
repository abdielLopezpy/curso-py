# Conceptos Clave de SQL y Bases de Datos

Este documento explica los conceptos fundamentales que necesitas entender para trabajar con SQL y SQLite.

---

## 📊 1. Bases de Datos Relacionales

### ¿Qué son?
Las bases de datos relacionales organizan la información en **tablas** que pueden estar **relacionadas** entre sí. Es como tener varias hojas de Excel conectadas.

### Ejemplo Real: Sistema de una Tienda
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    CLIENTES     │     │     VENTAS      │     │    PRODUCTOS    │
├─────────────────┤     ├─────────────────┤     ├─────────────────┤
│ id              │◄────│ cliente_id      │     │ id              │
│ nombre          │     │ producto_id     │────►│ nombre          │
│ email           │     │ cantidad        │     │ precio          │
│ telefono        │     │ fecha           │     │ stock           │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## 🔑 2. Claves Primarias (Primary Key)

### ¿Qué es?
Un identificador **único** para cada registro. No puede repetirse ni ser nulo.

### Características
- ✅ Única por cada fila
- ✅ No puede ser NULL
- ✅ Generalmente es un número entero
- ✅ Se auto-incrementa automáticamente

### Ejemplo en SQLite
```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Clave primaria
    nombre TEXT NOT NULL,
    email TEXT
);
```

### ¿Por qué es importante?
- Identifica cada registro de forma única
- Permite buscar registros específicos rápidamente
- Es necesaria para relacionar tablas

---

## 🔗 3. Claves Foráneas (Foreign Key)

### ¿Qué es?
Una columna que **referencia** la clave primaria de otra tabla. Crea una relación entre tablas.

### Ejemplo Visual
```
TABLA: productos                    TABLA: categorias
┌────┬──────────┬─────────────┐    ┌────┬────────────┐
│ id │ nombre   │ categoria_id│    │ id │ nombre     │
├────┼──────────┼─────────────┤    ├────┼────────────┤
│ 1  │ iPhone   │     1       │───►│ 1  │ Electrónica│
│ 2  │ Laptop   │     1       │───►│    │            │
│ 3  │ Camiseta │     2       │───►│ 2  │ Ropa       │
└────┴──────────┴─────────────┘    └────┴────────────┘
                │                         ▲
                └─────────────────────────┘
                    Clave Foránea
```

### Ejemplo en SQLite
```sql
-- Primero creamos la tabla padre
CREATE TABLE categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);

-- Luego la tabla hija con la clave foránea
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);
```

---

## 📝 4. Tipos de Datos en SQLite

SQLite es flexible con los tipos de datos. Los principales son:

| Tipo | Descripción | Ejemplo Python |
|------|-------------|----------------|
| `INTEGER` | Números enteros | `int` |
| `REAL` | Números decimales | `float` |
| `TEXT` | Cadenas de texto | `str` |
| `BLOB` | Datos binarios | `bytes` |
| `NULL` | Valor nulo | `None` |

### Ejemplo
```sql
CREATE TABLE productos (
    id INTEGER PRIMARY KEY,      -- Entero
    nombre TEXT NOT NULL,        -- Texto
    precio REAL,                 -- Decimal
    descripcion TEXT,            -- Texto (puede ser NULL)
    imagen BLOB                  -- Binario
);
```

---

## ⚠️ 5. Restricciones (Constraints)

Las restricciones definen reglas para los datos:

| Restricción | Significado | Ejemplo |
|-------------|-------------|---------|
| `PRIMARY KEY` | Identificador único | `id INTEGER PRIMARY KEY` |
| `NOT NULL` | No puede estar vacío | `nombre TEXT NOT NULL` |
| `UNIQUE` | No puede repetirse | `email TEXT UNIQUE` |
| `DEFAULT` | Valor por defecto | `activo INTEGER DEFAULT 1` |
| `CHECK` | Validación personalizada | `edad INTEGER CHECK(edad >= 0)` |
| `FOREIGN KEY` | Referencia otra tabla | `FOREIGN KEY (x) REFERENCES tabla(y)` |

### Ejemplo Completo
```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    edad INTEGER CHECK(edad >= 0 AND edad <= 150),
    activo INTEGER DEFAULT 1,
    pais_id INTEGER,
    FOREIGN KEY (pais_id) REFERENCES paises(id)
);
```

---

## 🔄 6. Tipos de Relaciones

### Uno a Uno (1:1)
Un registro en tabla A se relaciona con exactamente un registro en tabla B.

```
USUARIO ──────────── PERFIL
  1     tiene solo     1
```

**Ejemplo:** Un usuario tiene un solo perfil.

### Uno a Muchos (1:N)
Un registro en tabla A se relaciona con muchos registros en tabla B.

```
CATEGORIA ──────────── PRODUCTOS
    1      tiene muchos    N
```

**Ejemplo:** Una categoría tiene muchos productos.

### Muchos a Muchos (N:M)
Muchos registros en tabla A se relacionan con muchos registros en tabla B.
Requiere una **tabla intermedia**.

```
ESTUDIANTES ──── INSCRIPCIONES ──── CURSOS
     N              (tabla              M
                   intermedia)
```

**Ejemplo:** Un estudiante puede estar en muchos cursos, y un curso tiene muchos estudiantes.

---

## 🔍 7. Operadores de Comparación

| Operador | Significado | Ejemplo |
|----------|-------------|---------|
| `=` | Igual a | `WHERE edad = 25` |
| `<>` o `!=` | Diferente de | `WHERE status <> 'inactivo'` |
| `>` | Mayor que | `WHERE precio > 100` |
| `<` | Menor que | `WHERE stock < 10` |
| `>=` | Mayor o igual | `WHERE edad >= 18` |
| `<=` | Menor o igual | `WHERE cantidad <= 5` |
| `BETWEEN` | Entre dos valores | `WHERE edad BETWEEN 18 AND 30` |
| `LIKE` | Patrón de texto | `WHERE nombre LIKE 'A%'` |
| `IN` | En una lista | `WHERE id IN (1, 2, 3)` |
| `IS NULL` | Es nulo | `WHERE email IS NULL` |

---

## 🔗 8. JOINs (Unir Tablas)

Los JOINs permiten combinar datos de múltiples tablas.

### INNER JOIN
Devuelve solo registros que coinciden en ambas tablas.

```sql
SELECT productos.nombre, categorias.nombre
FROM productos
INNER JOIN categorias ON productos.categoria_id = categorias.id;
```

### LEFT JOIN
Devuelve todos los registros de la tabla izquierda + coincidencias de la derecha.

```sql
SELECT clientes.nombre, ventas.total
FROM clientes
LEFT JOIN ventas ON clientes.id = ventas.cliente_id;
```

### Diagrama Visual
```
INNER JOIN:        LEFT JOIN:         RIGHT JOIN:
    ┌───┐              ┌───┐              ┌───┐
  ┌─┤ A ├─┐          ┌─┤ A │            ┌─┤   ├─┐
  │ └─┬─┘ │          │ └─┬─┘            │ └─┬─┘ │
  │ ┌─┴─┐ │          │ ┌─┴─┐            │ ┌─┴─┐ │
  └─┤███├─┘          └─┤██ │            │ ██├─┘
    └─┬─┘              └─┬─┘            └─┬─┘
  ┌─┤ B ├─┐          ┌─┤   │          ┌─┤ B ├─┐
  │ └───┘ │          │ └───┘          │ └───┘ │
  └───────┘          └───────         └───────┘
Solo coincidencias   Todo A +         Todo B +
                     coincidencias    coincidencias
```

---

## 📊 9. Funciones de Agregación

| Función | Descripción | Ejemplo |
|---------|-------------|---------|
| `COUNT()` | Cuenta registros | `SELECT COUNT(*) FROM usuarios` |
| `SUM()` | Suma valores | `SELECT SUM(precio) FROM productos` |
| `AVG()` | Promedio | `SELECT AVG(edad) FROM usuarios` |
| `MAX()` | Valor máximo | `SELECT MAX(precio) FROM productos` |
| `MIN()` | Valor mínimo | `SELECT MIN(precio) FROM productos` |

### Con GROUP BY
```sql
-- Contar productos por categoría
SELECT categoria_id, COUNT(*) as total
FROM productos
GROUP BY categoria_id;
```

---

## 🔒 10. Transacciones

Una transacción agrupa múltiples operaciones como una sola unidad. Si algo falla, todo se revierte.

### Propiedades ACID
- **A**tomicity (Atomicidad): Todo o nada
- **C**onsistency (Consistencia): Datos siempre válidos
- **I**solation (Aislamiento): Operaciones independientes
- **D**urability (Durabilidad): Cambios permanentes

### Ejemplo en Python
```python
try:
    cursor.execute("INSERT INTO cuentas ...")
    cursor.execute("UPDATE saldos ...")
    conexion.commit()  # Confirmar si todo fue bien
except:
    conexion.rollback()  # Revertir si hubo error
```

---

## 🎯 Resumen de Comandos SQL

```sql
-- CREAR
CREATE TABLE nombre_tabla (...);

-- INSERTAR
INSERT INTO tabla (col1, col2) VALUES (val1, val2);

-- CONSULTAR
SELECT columnas FROM tabla WHERE condicion;

-- ACTUALIZAR
UPDATE tabla SET columna = valor WHERE condicion;

-- ELIMINAR
DELETE FROM tabla WHERE condicion;

-- ELIMINAR TABLA
DROP TABLE nombre_tabla;

-- MODIFICAR TABLA
ALTER TABLE tabla ADD COLUMN nueva_columna TIPO;
```

---

¡Con estos conceptos estás listo para empezar a programar con SQL y SQLite! 🚀
