# ============================================================================
# ENTIDAD: Autor
# ============================================================================
# Completar siguiendo el patron de domain/entities/libro.py.
#
# Campos esperados (ver sql/schema.sql tabla autores):
#   - nombre:       str
#   - nacionalidad: str
#   - biografia:    Optional[str] = None
#   - id:           Optional[int] = Field(default=None, primary_key=True)
# ============================================================================

from typing import Optional

from sqlmodel import SQLModel, Field


class AutorBase(SQLModel):
    # TODO: declarar los campos comunes.
    pass


class Autor(AutorBase, table=True):
    __tablename__ = "autores"

    id: Optional[int] = Field(default=None, primary_key=True)
