# ============================================================================
# USE CASE: Crear libro
# ============================================================================

from domain.entities.libro import Libro
from domain.exceptions import EntidadDuplicada
from domain.repositories.libro_repository import LibroRepository
from application.schemas.libro_schema import LibroCreate


class CrearLibro:

    def __init__(self, repo: LibroRepository) -> None:
        self.repo = repo

    def execute(self, data: LibroCreate) -> Libro:
        # Convertimos el schema (Pydantic) a entidad de dominio.
        libro = Libro(**data.model_dump())
        try:
            return self.repo.crear(libro)
        except EntidadDuplicada:
            # Propagamos para que el router la traduzca a 409.
            raise
