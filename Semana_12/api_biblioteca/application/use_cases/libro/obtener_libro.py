# ============================================================================
# USE CASE: Obtener libro por id
# ============================================================================

from domain.entities.libro import Libro
from domain.exceptions import EntidadNoEncontrada
from domain.repositories.libro_repository import LibroRepository


class ObtenerLibro:

    def __init__(self, repo: LibroRepository) -> None:
        self.repo = repo

    def execute(self, libro_id: int) -> Libro:
        libro = self.repo.obtener_por_id(libro_id)
        if libro is None:
            raise EntidadNoEncontrada(f"No existe el libro con id={libro_id}")
        return libro
