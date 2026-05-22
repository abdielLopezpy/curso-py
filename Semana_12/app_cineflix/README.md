# Cineflix - Semana 12

API REST tipo Netflix construida con **FastAPI** + **SQLite** + **Clean
Architecture**. La entidad `Movie` esta completamente implementada como
plantilla; el resto (`User`, `UserGroup`, `Plan`, `Subscription`, `Catalog`)
queda como TODO para el live coding.

## Estado por entidad

| Entidad        | Estado           | Notas                                       |
|----------------|------------------|---------------------------------------------|
| `Movie`        | **IMPLEMENTADA** | CRUD completo, sirve de plantilla           |
| `User`         | TODO             | Replicar patron de Movie + hash de password |
| `UserGroup`    | TODO             | Validar `max_members` del plan al sumar     |
| `Plan`         | TODO             | Recordar bool <-> int en SQLite             |
| `Subscription` | TODO             | Regla: `expires_at = now + plan.duration_days` |
| `Catalog`      | TODO             | Maneja M:N con `catalog_movies`             |

## Capas (Clean Architecture)

```
app_cineflix/
+-- main.py                       # FastAPI + lifespan (init_db al arrancar)
+-- requirements.txt
+-- sql/
|   +-- schema.sql                # CREATE TABLE
|   +-- seed.sql                  # Datos de ejemplo
+-- application/                  # Reglas de negocio (PURO, sin frameworks)
|   +-- entities/                 # Dataclasses puras (Movie, User, ...)
|   +-- exceptions.py             # DomainError, EntidadNoEncontrada, ...
|   +-- schemas/                  # Pydantic DTOs (entrada/salida HTTP)
|   +-- repositories/             # INTERFACES abstractas (ABC)
|   +-- use_cases/                # Una clase por accion de negocio
|       +-- movie/                # COMPLETO (plantilla)
|       +-- {user,user_group,plan,subscription,catalog}/   # TODO
+-- infrastructure/               # Detalles tecnicos
|   +-- database/                 # Conexion sqlite3 + init_db
|   +-- models/                   # Row models (UserModel.to_entity, ...)
|   +-- repositories/             # Implementacion SQL de los repos
+-- interfaces/                   # Mundo exterior (frameworks)
    +-- dependencies.py           # Inyeccion de dependencias FastAPI
    +-- routers/                  # Un router por entidad
```

**Regla de oro:** las flechas de dependencia apuntan hacia adentro.
`application/` NO importa nada de `infrastructure/` ni de `interfaces/`.

## Flujo de una request (ejemplo `GET /api/movies/3`)

```
HTTP GET /api/movies/3
        |
        v
interfaces/routers/movie_router.py        # extrae movie_id de la URL
        |
        v  ObtenerMovie(repo).execute(3)
application/use_cases/movie/obtener_movie.py   # logica pura
        |
        v  repo.obtener_por_id(3)
application/repositories/movie_repository.py    # interfaz abstracta
        |
        v  (resuelto via Depends)
infrastructure/repositories/movie_sqlite_repository.py   # SQL real
        |
        v  SELECT * FROM movies WHERE id = 3
SQLite (cineflix.db)
        |
        v  fila
infrastructure/models/movie_model.py.from_row(row).to_entity()
        |
        v  Movie (entidad pura)
        |
        v  serializada como MovieRead (Pydantic)
HTTP 200 { "id": 3, "title": "...", ... }
```

## Como correr

```bash
cd Semana_12/app_cineflix
pip install -r requirements.txt
uvicorn main:app --reload --port 8012
```

Abrir en el navegador:
- Swagger UI: http://localhost:8012/docs
- ReDoc:      http://localhost:8012/redoc

Al arrancar, el lifespan crea `cineflix.db` y carga el seed automaticamente.

## Endpoints actuales

### Movies (implementados)

| Metodo | Ruta                | Codigo OK | Codigos error |
|--------|---------------------|-----------|---------------|
| GET    | `/api/movies`       | 200       | -             |
| GET    | `/api/movies/{id}`  | 200       | 404           |
| POST   | `/api/movies`       | 201       | 422           |
| PUT    | `/api/movies/{id}`  | 200       | 404           |
| DELETE | `/api/movies/{id}`  | 204       | 404           |

### Resto (a implementar en vivo)

`/api/users`, `/api/groups`, `/api/plans`, `/api/subscriptions`, `/api/catalogs`.
Cada router stub ya existe con su `APIRouter` listo; faltan los endpoints.

## Guion sugerido para el live coding

1. **Arranque:** levantar el servidor y mostrar `/docs` con `Movie` funcionando.
2. **Tour vertical:** seguir un `GET /api/movies` de afuera hacia adentro
   (router -> use case -> interfaz repo -> repo SQLite -> entidad).
3. **Replicar `Plan`:** copiar la estructura de `Movie` y adaptarla. Es la
   mas parecida (sin FKs complicadas, solo bool <-> int).
4. **Replicar `User`:** introducir hashing de password en el use case
   `crear_user` (no en el schema ni en el repo).
5. **Replicar `Subscription`:** primer caso con **regla de negocio fuerte**
   (calcular `expires_at`, validar que el plan este activo).
6. **Replicar `Catalog`:** introducir M:N con `catalog_movies` y endpoints
   especificos para `agregar_movie` / `quitar_movie`.

## Esquema (mejoras frente al whiteboard original)

1. Tabla `USER_TYPE` eliminada -> `users.role` ('admin' | 'standard' | 'kid').
   `is_adult` se deriva en la entidad desde `birthday`.
2. Circularidad `user_groups <-> subscriptions` eliminada: solo
   `subscriptions.group_id`.
3. `PLAN_TYPE` fusionado dentro de `plans` (`kind` + `max_members`).
4. `USER_CATALOG.catalog_id` (auto-referencia) eliminada: ahora `catalogs` +
   tabla M:N `catalog_movies`.
