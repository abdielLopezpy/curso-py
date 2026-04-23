# ============================================================================
# USE CASE: Actualizar libro
# ============================================================================

from domain.entities.libro import Libro
from domain.exceptions import EntidadNoEncontrada
from domain.repositories.libro_repository import LibroRepository
from application.schemas.libro_schema import LibroUpdate


class ActualizarLibro:

    def __init__(self, repo: LibroRepository) -> None:
        self.repo = repo

    def execute(self, libro_id: int, data: LibroUpdate) -> Libro:
        libro = self.repo.obtener_por_id(libro_id)
        if libro is None:
            raise EntidadNoEncontrada(f"No existe el libro con id={libro_id}")

        # Aplicamos solo los campos que vinieron (exclude_unset=True).
        cambios = data.model_dump(exclude_unset=True)
        for campo, valor in cambios.items():
            setattr(libro, campo, valor)

        actualizado = self.repo.actualizar(libro)
        if actualizado is None:
            raise EntidadNoEncontrada(f"No existe el libro con id={libro_id}")
        return actualizado
