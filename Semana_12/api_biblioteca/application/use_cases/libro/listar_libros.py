# ============================================================================
# USE CASE: Listar libros
# ============================================================================
# Un use case = una accion de negocio. Una clase con un solo metodo execute().
# No sabe NADA de HTTP; solo orquesta dominio + repositorio.
# ============================================================================

from typing import List

from domain.entities.libro import Libro
from domain.repositories.libro_repository import LibroRepository


class ListarLibros:

    def __init__(self, repo: LibroRepository) -> None:
        self.repo = repo

    def execute(self) -> List[Libro]:
        return self.repo.listar()
