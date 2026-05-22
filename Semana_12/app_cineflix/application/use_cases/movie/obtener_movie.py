# ============================================================================
# USE CASE: Obtener pelicula por id
# ============================================================================
# Si la pelicula no existe, levanta EntidadNoEncontrada. El router decide
# como traducir esa excepcion (en este caso a HTTP 404).
# ============================================================================

from application.entities.movie import Movie
from application.exceptions import EntidadNoEncontrada
from application.repositories.movie_repository import MovieRepository


class ObtenerMovie:

    def __init__(self, repo: MovieRepository) -> None:
        self.repo = repo

    def execute(self, movie_id: int) -> Movie:
        movie = self.repo.obtener_por_id(movie_id)
        if movie is None:
            raise EntidadNoEncontrada(f"No existe la pelicula con id={movie_id}")
        return movie
