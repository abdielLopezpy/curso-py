# ============================================================================
# SCHEMAS: Autor
# ============================================================================
# Completar siguiendo el patron de application/schemas/libro_schema.py.
#
#   AutorCreate -> body del POST
#   AutorRead   -> respuesta del GET (incluye id)
#   AutorUpdate -> body del PUT (todos opcionales)
# ============================================================================

from typing import Optional

from sqlmodel import SQLModel

from domain.entities.autor import AutorBase


class AutorCreate(AutorBase):
    pass


class AutorRead(AutorBase):
    id: int


class AutorUpdate(SQLModel):
    # TODO: todos los campos opcionales.
    nombre: Optional[str] = None
