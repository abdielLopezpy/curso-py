# ============================================================================
# SCHEMAS: Prestamo
# ============================================================================
# Completar siguiendo el patron de application/schemas/libro_schema.py.
#
#   PrestamoCreate -> body del POST (ej: solo libro_id y nombre_usuario)
#   PrestamoRead   -> respuesta del GET
#   PrestamoUpdate -> body del PUT (ej: registrar fecha_devolucion)
# ============================================================================

from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel

from domain.entities.prestamo import PrestamoBase


class PrestamoCreate(SQLModel):
    # TODO: al crear un prestamo NO se pide fecha_prestamo (se pone now()).
    libro_id: int
    nombre_usuario: str


class PrestamoRead(PrestamoBase):
    id: int


class PrestamoUpdate(SQLModel):
    # TODO: campos opcionales para marcar devolucion.
    fecha_devolucion: Optional[datetime] = None
