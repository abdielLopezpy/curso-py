# ============================================================================
# INTERFAZ de repositorio: MovieRepository
# ============================================================================
# Contrato abstracto: dice QUE puede hacer un repositorio de peliculas,
# pero no COMO. La implementacion concreta (SQLite, Postgres, memoria, etc.)
# vive en `infrastructure/repositories/movie_sqlite_repository.py`.
#
# Beneficios:
#   - Los use cases dependen SOLO de esta interfaz (inversion de dependencia).
#   - Podemos testear use cases con un repo falso en memoria.
#   - Si manana cambiamos el backend, solo tocamos la implementacion concreta.
# ============================================================================

from abc import ABC, abstractmethod
from typing import List, Optional

from application.entities.movie import Movie


class MovieRepository(ABC):

    @abstractmethod
    def listar(self) -> List[Movie]:
        """Devuelve todas las peliculas ordenadas por id."""

    @abstractmethod
    def obtener_por_id(self, movie_id: int) -> Optional[Movie]:
        """Devuelve la pelicula con ese id, o None si no existe."""

    @abstractmethod
    def crear(self, movie: Movie) -> Movie:
        """Persiste la pelicula y devuelve la entidad con id + created_at."""

    @abstractmethod
    def actualizar(self, movie: Movie) -> Optional[Movie]:
        """Actualiza una pelicula existente. Devuelve None si no existe."""

    @abstractmethod
    def eliminar(self, movie_id: int) -> bool:
        """Elimina la pelicula. Devuelve True si elimino, False si no existia."""
