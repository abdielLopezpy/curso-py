# ============================================================================
# INYECCION DE DEPENDENCIAS (FastAPI)
# ============================================================================
# Cada endpoint declara las dependencias que necesita via `Depends(...)`.
# FastAPI las resuelve y se las pasa como argumentos.
#
# Por que importa para Clean Architecture:
#   - El router NO instancia el repositorio a mano: lo recibe ya construido.
#   - Podemos intercambiar la implementacion concreta sin tocar el router
#     (ej: en tests, sustituir get_movie_repository por uno en memoria).
#
# Convencion: una funcion `get_<entidad>_repository` por entidad.
# ============================================================================

import sqlite3
from typing import Iterator

from fastapi import Depends

from application.repositories.movie_repository import MovieRepository
from infrastructure.database.connection import get_connection
from infrastructure.repositories.movie_sqlite_repository import MovieSQLiteRepository


def get_db() -> Iterator[sqlite3.Connection]:
    """Cede una conexion sqlite3 por request y la cierra al terminar."""
    with get_connection() as con:
        yield con


def get_movie_repository(
    con: sqlite3.Connection = Depends(get_db),
) -> MovieRepository:
    return MovieSQLiteRepository(con)


# ----------------------------------------------------------------------------
# TODO (live coding): agregar las funciones para las otras entidades:
#   - get_user_repository
#   - get_user_group_repository
#   - get_plan_repository
#   - get_subscription_repository
#   - get_catalog_repository
# Cada una sigue exactamente el mismo patron que get_movie_repository.
# ----------------------------------------------------------------------------
