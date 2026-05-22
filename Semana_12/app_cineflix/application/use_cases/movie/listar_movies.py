# ============================================================================
# USE CASE: Listar peliculas
# ============================================================================
# Un use case = una accion de negocio aislada.
# Reglas:
#   - Es una clase con un solo metodo `execute()`.
#   - Depende de la INTERFAZ del repositorio (MovieRepository), no de la
#     implementacion concreta. Inyectamos el repo por el constructor.
#   - NO sabe nada de HTTP, FastAPI ni SQL.
# ============================================================================

from typing import List

from application.entities.movie import Movie
from application.repositories.movie_repository import MovieRepository


class ListarMovies:

    def __init__(self, repo: MovieRepository) -> None:
        self.repo = repo

    def execute(self) -> List[Movie]:
        return self.repo.listar()
