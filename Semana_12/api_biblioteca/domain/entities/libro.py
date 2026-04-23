# ============================================================================
# ENTIDAD: Libro
# ============================================================================
# Modelo SQLModel que combina la tabla de BD y el modelo de dominio.
#
# Patron (tipico de SQLModel):
#   - LibroBase  -> campos comunes (sin id)
#   - Libro      -> tabla real (hereda de LibroBase + agrega id)
#
# Los schemas de entrada/salida (LibroCreate, LibroRead, LibroUpdate) viven
# en application/schemas/libro_schema.py y tambien reutilizan LibroBase.
# ============================================================================

from typing import Optional

from sqlmodel import SQLModel, Field


class LibroBase(SQLModel):
    titulo: str
    isbn: str = Field(unique=True, index=True)
    anio_publicacion: int
    disponible: bool = True
    autor_id: int = Field(foreign_key="autores.id")


class Libro(LibroBase, table=True):
    __tablename__ = "libros"

    id: Optional[int] = Field(default=None, primary_key=True)

    def marcar_como_prestado(self) -> None:
        self.disponible = False

    def marcar_como_devuelto(self) -> None:
        self.disponible = True
