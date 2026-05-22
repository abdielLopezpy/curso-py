# ============================================================================
# IMPLEMENTACION CONCRETA: MovieSQLiteRepository
# ============================================================================
# Traduce las operaciones del dominio a queries SQL sobre SQLite.
# Solo esta clase sabe que la BD es SQLite. Si manana cambiamos a Postgres,
# este es el unico archivo que habria que reemplazar.
#
# Flujo (de afuera hacia adentro):
#   router -> use case -> MovieRepository (interfaz) -> MovieSQLiteRepository
#                                                       (esta clase)
#
# Patron del row -> entity:
#   1. Ejecutamos SQL.
#   2. Construimos un MovieModel.from_row(row).
#   3. Convertimos con .to_entity() a la entidad pura Movie.
# ============================================================================

import sqlite3
from typing import List, Optional

from application.entities.movie import Movie
from application.repositories.movie_repository import MovieRepository
from infrastructure.models.movie_model import MovieModel


class MovieSQLiteRepository(MovieRepository):

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    # -- Lectura -----------------------------------------------------------

    def listar(self) -> List[Movie]:
        cur = self.connection.execute(
            "SELECT id, title, url, age_rating, created_at "
            "FROM movies ORDER BY id"
        )
        return [MovieModel.from_row(row).to_entity() for row in cur.fetchall()]

    def obtener_por_id(self, movie_id: int) -> Optional[Movie]:
        cur = self.connection.execute(
            "SELECT id, title, url, age_rating, created_at "
            "FROM movies WHERE id = ?",
            (movie_id,),
        )
        row = cur.fetchone()
        return MovieModel.from_row(row).to_entity() if row else None

    # -- Escritura ---------------------------------------------------------

    def crear(self, movie: Movie) -> Movie:
        cur = self.connection.execute(
            "INSERT INTO movies (title, url, age_rating) VALUES (?, ?, ?)",
            (movie.title, movie.url, movie.age_rating),
        )
        self.connection.commit()
        new_id = cur.lastrowid
        # Releemos para devolver tambien created_at (lo pone CURRENT_TIMESTAMP).
        creada = self.obtener_por_id(new_id)
        assert creada is not None  # acabamos de crearla
        return creada

    def actualizar(self, movie: Movie) -> Optional[Movie]:
        if movie.id is None:
            return None
        cur = self.connection.execute(
            "UPDATE movies SET title = ?, url = ?, age_rating = ? WHERE id = ?",
            (movie.title, movie.url, movie.age_rating, movie.id),
        )
        self.connection.commit()
        if cur.rowcount == 0:
            return None
        return self.obtener_por_id(movie.id)

    def eliminar(self, movie_id: int) -> bool:
        cur = self.connection.execute(
            "DELETE FROM movies WHERE id = ?",
            (movie_id,),
        )
        self.connection.commit()
        return cur.rowcount > 0
