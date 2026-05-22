# ============================================================================
# USE CASE: Actualizar pelicula
# ============================================================================
# Estrategia de actualizacion parcial:
#   - data.model_dump(exclude_unset=True) devuelve SOLO los campos que el
#     cliente envio explicitamente en el body.
#   - Aplicamos esos campos sobre la entidad cargada de BD.
#   - Persistimos la entidad completa.
# ============================================================================

from application.entities.movie import Movie
from application.exceptions import EntidadNoEncontrada
from application.repositories.movie_repository import MovieRepository
from application.schemas.movie_schema import MovieUpdate


class ActualizarMovie:

    def __init__(self, repo: MovieRepository) -> None:
        self.repo = repo

    def execute(self, movie_id: int, data: MovieUpdate) -> Movie:
        movie = self.repo.obtener_por_id(movie_id)
        if movie is None:
            raise EntidadNoEncontrada(f"No existe la pelicula con id={movie_id}")

        cambios = data.model_dump(exclude_unset=True)
        for campo, valor in cambios.items():
            setattr(movie, campo, valor)

        actualizado = self.repo.actualizar(movie)
        if actualizado is None:
            raise EntidadNoEncontrada(f"No existe la pelicula con id={movie_id}")
        return actualizado
