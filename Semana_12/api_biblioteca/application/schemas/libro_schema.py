# ============================================================================
# SCHEMAS (Pydantic / SQLModel): Libro
# ============================================================================
# Modelos de entrada y salida para el API. NO tienen table=True: son puros
# modelos de validacion/serializacion para FastAPI.
#
#   LibroCreate -> body del POST
#   LibroRead   -> respuesta del GET (incluye id)
#   LibroUpdate -> body del PUT (todos los campos opcionales)
# ============================================================================

from typing import Optional

from sqlmodel import SQLModel

from domain.entities.libro import LibroBase


class LibroCreate(LibroBase):
    """Lo que el cliente envia al crear un libro."""


class LibroRead(LibroBase):
    """Lo que el API devuelve al cliente."""
    id: int


class LibroUpdate(SQLModel):
    """Todos los campos son opcionales para permitir actualizaciones parciales."""
    titulo: Optional[str] = None
    isbn: Optional[str] = None
    anio_publicacion: Optional[int] = None
    disponible: Optional[bool] = None
    autor_id: Optional[int] = None
