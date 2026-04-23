# ============================================================================
# SEMANA 12: API REST con FastAPI + SQLModel + Clean Architecture
# ============================================================================

## Objetivo

La Semana 12 cierra el curso aplicando **Clean Architecture** sobre una API REST
real construida con **FastAPI**, **SQLModel** (Pydantic + SQLAlchemy) y
**SQLite**. El alumno aprende a separar el codigo en capas independientes,
donde las reglas de negocio no dependen del framework ni de la base de datos,
sino al reves.

| Semana  | Concepto                          | Aplicado en el proyecto                 |
|---------|-----------------------------------|-----------------------------------------|
| 1-3     | Variables, funciones, logica      | Reglas de negocio en use cases          |
| 4-5     | POO y abstracciones               | Entidades, interfaces de repositorio    |
| 6-7     | Modulos, archivos, SQL            | sqlite3 + sentencias SQL a mano         |
| 8       | CRUD con Flask                    | Base del CRUD que se reescribe en FastAPI|
| 9       | Autenticacion y seguridad         | Base para extender con JWT (opcional)   |
| 10      | Proyecto integrador               | Mismo dominio, ahora desacoplado        |
| 11      | Ciencia de datos                  | Consume datos via API                   |
| **12**  | **API + Clean Architecture**      | **Biblioteca: Libro / Autor / Prestamo**|

---

## Proyecto: API Biblioteca

**Carpeta:** `api_biblioteca/`

**Ejecutar:**

```bash
pip install -r api_biblioteca/requirements.txt
cd api_biblioteca
uvicorn main:app --reload --port 8012
```

**Docs interactivas (Swagger UI):** http://localhost:8012/docs
**Docs alternativas (ReDoc):**       http://localhost:8012/redoc

---

## Entidades

| Entidad    | Estado           | Rol en la clase                         |
|------------|------------------|-----------------------------------------|
| `Libro`    | **IMPLEMENTADO** | Ejemplo completo para guiar el live coding |
| `Autor`    | TODO             | Los alumnos replican el patron de Libro  |
| `Prestamo` | TODO             | Extension con reglas de negocio (FK, validar disponibilidad) |

La idea es que `Libro` sirva como plantilla: los alumnos copian el patron y lo
adaptan para `Autor` y `Prestamo` durante la clase en vivo.

---

## Clean Architecture (capas)

```
+-------------------------------------------+
|  interfaces/  (FastAPI routers)           |  <- Frameworks & drivers
+-------------------------------------------+
|  application/ (use cases + schemas)        |  <- Casos de uso / orquestacion
+-------------------------------------------+
|  domain/      (entities + repo interfaces)|  <- Reglas de negocio puras
+-------------------------------------------+
|  infrastructure/ (SQLite + SQL a mano)    |  <- Detalles tecnicos
+-------------------------------------------+
```

**Regla de oro:** las flechas de dependencia apuntan hacia adentro. `domain/`
no importa nada de las otras capas.

### Estructura de carpetas

```
api_biblioteca/
├── main.py                   # Punto de entrada (FastAPI + wiring)
├── requirements.txt
├── sql/
│   ├── schema.sql            # CREATE TABLE de las 3 entidades
│   └── seed.sql              # Datos de ejemplo
├── domain/                   # Reglas de negocio PURAS (sin FastAPI, sin SQL)
│   ├── entities/             # Libro, Autor, Prestamo (dataclasses)
│   ├── repositories/         # Interfaces abstractas (ABC)
│   └── exceptions.py         # Excepciones de dominio
├── application/              # Casos de uso (orquestan dominio)
│   ├── schemas/              # Pydantic: entrada/salida HTTP
│   └── use_cases/            # Un archivo por caso de uso
│       ├── libro/            # COMPLETO
│       ├── autor/            # TODO
│       └── prestamo/         # TODO
├── infrastructure/           # Detalles tecnicos
│   ├── database/             # Conexion sqlite3 + init_db
│   └── repositories/         # Implementacion SQL de los repos
└── interfaces/               # Entrada/salida HTTP
    ├── dependencies.py       # Inyeccion de dependencias FastAPI
    └── routers/              # Un router por entidad
```

---

## Conceptos clave de la semana

| Concepto                  | Que es                                              |
|---------------------------|-----------------------------------------------------|
| **Clean Architecture**    | Separar reglas de negocio de detalles tecnicos      |
| **Entity (dominio)**      | Objeto de negocio puro (dataclass, sin anotaciones de framework) |
| **Repository pattern**    | Interfaz para acceder a datos sin saber el backend  |
| **Use case**              | Una accion de negocio: "CrearLibro", "ListarLibros" |
| **DTO / Schema**          | Objeto de transferencia (Pydantic) para la API      |
| **Dependency Injection**  | FastAPI inyecta el repositorio en cada endpoint     |
| **FastAPI**               | Framework ASGI con validacion Pydantic + OpenAPI    |
| **Pydantic**              | Validacion y serializacion declarativa              |
| **SQLModel**              | ORM moderno: combina Pydantic + SQLAlchemy          |
| **Session / select()**    | API declarativa de SQLModel para queries            |
| **uvicorn**               | Servidor ASGI para correr FastAPI                   |
| **OpenAPI / Swagger**     | Documentacion automatica en `/docs`                 |

---

## Endpoints del API

### Libros (implementados)

| Metodo | Ruta                | Descripcion                 |
|--------|---------------------|-----------------------------|
| GET    | `/api/libros`       | Listar todos los libros     |
| GET    | `/api/libros/{id}`  | Obtener un libro por id     |
| POST   | `/api/libros`       | Crear un libro              |
| PUT    | `/api/libros/{id}`  | Actualizar un libro         |
| DELETE | `/api/libros/{id}`  | Eliminar un libro           |

### Autores (a implementar en vivo)

| Metodo | Ruta                | Descripcion                 |
|--------|---------------------|-----------------------------|
| GET    | `/api/autores`      | Listar todos los autores    |
| GET    | `/api/autores/{id}` | Obtener un autor por id     |
| POST   | `/api/autores`      | Crear un autor              |
| PUT    | `/api/autores/{id}` | Actualizar un autor         |
| DELETE | `/api/autores/{id}` | Eliminar un autor           |

### Prestamos (a implementar en vivo)

| Metodo | Ruta                  | Descripcion                     |
|--------|-----------------------|---------------------------------|
| GET    | `/api/prestamos`      | Listar todos los prestamos      |
| GET    | `/api/prestamos/{id}` | Obtener un prestamo             |
| POST   | `/api/prestamos`      | Registrar un prestamo de libro  |
| PUT    | `/api/prestamos/{id}/devolver` | Marcar como devuelto   |
| DELETE | `/api/prestamos/{id}` | Eliminar un prestamo            |

---

## Guion del live coding

1. **Arranque:** `uvicorn main:app --reload --port 8012`, abrir `/docs` y mostrar
   los endpoints de Libros funcionando.
2. **Tour por capas:** recorrer el flujo completo de un `GET /api/libros` de
   afuera hacia adentro (router -> use case -> repository interface ->
   SQLite repo -> entidad).
3. **Replicar `Autor`:** en vivo, copiar la estructura de `Libro` y adaptarla.
   Empezar por la entidad, luego el schema, repo, use cases y router.
4. **Replicar `Prestamo`:** agregar la regla de negocio de "el libro debe estar
   disponible" y la actualizacion en cascada (al prestar, `libro.disponible=False`).
5. **Probar con Swagger UI:** crear autor, crear libro apuntando al autor,
   registrar prestamo, devolverlo.

---

## Preguntas de repaso

1. ¿Por que `domain/` no importa nada de `fastapi` ni de `sqlite3`?
2. ¿Que pasa si manana cambiamos SQLite por PostgreSQL? ¿Que capas cambian?
3. ¿Para que sirve la interfaz `LibroRepository` si ya existe `LibroSQLiteRepository`?
4. ¿Cual es la diferencia entre un **entity** y un **schema** Pydantic?
5. ¿Que hace `Depends()` en FastAPI y por que es clave para Clean Architecture?
6. ¿Por que los use cases son clases con un solo metodo y no funciones sueltas?
7. ¿Como prevenimos inyeccion SQL al pasar parametros?
8. ¿Donde iria la validacion "el ISBN debe tener 13 digitos": en el schema,
   en la entidad o en el use case?
9. ¿Que ventajas da la documentacion automatica de FastAPI?
10. ¿Como testeariamos un use case sin levantar FastAPI ni SQLite?

---

## Notas del instructor

- Clean Architecture puede sonar sobre-ingeniado para un CRUD pequeno, pero el
  objetivo pedagogico es que los alumnos vean **por que** separar capas paga
  intereses cuando el proyecto crece.
- El live coding debe enfatizar el **orden de creacion** de afuera hacia adentro
  o de adentro hacia afuera, pero **siempre siguiendo el mismo orden** para
  Autor y Prestamo. Eso cimienta el patron.
- Si queda tiempo, mostrar como testear un use case con un repositorio falso
  en memoria (mock) sin tocar SQLite.
