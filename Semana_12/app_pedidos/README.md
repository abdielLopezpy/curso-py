# App Pedidos - Semana 12

Esqueleto con arquitectura limpia para una app de suscripciones / catalogo de
peliculas. Base de datos: **SQLite** (modulo `sqlite3` de la libreria estandar).

## Capas

```
app_pedidos/
+-- main.py                    # Punto de entrada (inicializa BD)
+-- requirements.txt
+-- sql/
|   +-- schema.sql             # CREATE TABLE (esquema mejorado del whiteboard)
|   +-- seed.sql               # Datos de ejemplo
+-- application/               # Reglas de negocio
|   +-- entities/              # Entidades puras (dataclasses, sin SQL)
|   +-- use_cases/             # TODO: a desarrollar en clase
+-- infrastructure/            # Detalles tecnicos
    +-- database/              # Conexion sqlite3 + init_db
    +-- models/                # Modelos de fila (UserModel, PlanModel, ...)
    +-- repositories/          # TODO: a desarrollar en clase
```

**Regla:** `application/` no importa nada de `infrastructure/`. La conversion
modelo <-> entidad vive en los `*_model.py` (capa infra).

## Esquema (mejoras frente al whiteboard)

1. Tabla `USER_TYPE` eliminada -> `users.role` ('admin' | 'standard' | 'kid').
   `is_adult` se deriva en la entidad desde `birthday`.
2. Circularidad `user_groups <-> subscriptions` eliminada: solo
   `subscriptions.group_id`.
3. `PLAN_TYPE` fusionado dentro de `plans` (`kind` + `max_members`).
4. `USER_CATALOG.catalog_id` (auto-referencia) eliminada: ahora `catalogs` +
   tabla M:N `catalog_movies`.

## Como correr

```bash
cd Semana_12/app_pedidos
python main.py
```

Esto crea `pedidos.db` y carga los datos del seed.
