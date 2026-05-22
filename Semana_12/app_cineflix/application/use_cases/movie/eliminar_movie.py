# ============================================================================
# USE CASE: Eliminar pelicula
# ============================================================================
# Si el repo devuelve False, significa que la pelicula no existia: traducimos
# eso a EntidadNoEncontrada para que el router responda 404.
# ============================================================================

from application.exceptions import EntidadNoEncontrada
from application.repositories.movie_repository import MovieRepository


class EliminarMovie:

    def __init__(self, repo: MovieRepository) -> None:
        self.repo = repo

    def execute(self, movie_id: int) -> None:
        eliminado = self.repo.eliminar(movie_id)
        if not eliminado:
            raise EntidadNoEncontrada(f"No existe la pelicula con id={movie_id}")
