# ============================================================================
# USE CASE: Eliminar libro
# ============================================================================

from domain.exceptions import EntidadNoEncontrada
from domain.repositories.libro_repository import LibroRepository


class EliminarLibro:

    def __init__(self, repo: LibroRepository) -> None:
        self.repo = repo

    def execute(self, libro_id: int) -> None:
        eliminado = self.repo.eliminar(libro_id)
        if not eliminado:
            raise EntidadNoEncontrada(f"No existe el libro con id={libro_id}")
