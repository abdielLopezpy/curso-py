# ============================================================================
# ENTIDAD: Prestamo
# ============================================================================
# Completar siguiendo el patron de domain/entities/libro.py.
#
# Campos esperados (ver sql/schema.sql tabla prestamos):
#   - libro_id:         int = Field(foreign_key="libros.id")
#   - nombre_usuario:   str
#   - fecha_prestamo:   datetime
#   - fecha_devolucion: Optional[datetime] = None
#   - id:               Optional[int] = Field(default=None, primary_key=True)
#
# Reglas de negocio sugeridas:
#   - Solo se puede prestar un libro que este disponible.
#   - Al crear un prestamo, libro.disponible = False.
#   - Al devolver, fecha_devolucion = now() y libro.disponible = True.
# ============================================================================

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class PrestamoBase(SQLModel):
    # TODO: declarar los campos comunes.
    pass


class Prestamo(PrestamoBase, table=True):
    __tablename__ = "prestamos"

    id: Optional[int] = Field(default=None, primary_key=True)
