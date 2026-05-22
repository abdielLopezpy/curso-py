# ============================================================================
# USE CASE: Crear pelicula
# ============================================================================
# Flujo:
#   1. Recibe un MovieCreate (schema validado por Pydantic).
#   2. Convierte el schema a la entidad de dominio Movie.
#   3. Pide al repositorio que persista la entidad.
#   4. Devuelve la entidad ya con id + created_at.
#
# Aqui ponemos validaciones de negocio que excedan a un type check Pydantic.
# Ejemplo: "no permitir titulos vacios" (ya validado en schema).
# ============================================================================

from application.entities.movie import Movie
from application.repositories.movie_repository import MovieRepository
from application.schemas.movie_schema import MovieCreate


class CrearMovie:

    def __init__(self, repo: MovieRepository) -> None:
        self.repo = repo

    def execute(self, data: MovieCreate) -> Movie:
        movie = Movie(
            id=None,
            title=data.title,
            url=data.url,
            age_rating=data.age_rating,
        )
        return self.repo.crear(movie)
