# ============================================================================
# INYECCION DE DEPENDENCIAS (FastAPI)
# ============================================================================
# Cada endpoint recibe el repositorio listo para usar. Esto permite:
#  - Intercambiar la implementacion concreta sin tocar los routers.
#  - Testear con un repositorio en memoria inyectando un Depends() distinto.
# ============================================================================

from fastapi import Depends
from sqlmodel import Session

from domain.repositories.libro_repository import LibroRepository
from infrastructure.database.connection import get_session
from infrastructure.repositories.libro_sqlmodel_repository import LibroSQLModelRepository


def get_libro_repository(session: Session = Depends(get_session)) -> LibroRepository:
    return LibroSQLModelRepository(session)


# TODO: agregar get_autor_repository y get_prestamo_repository
#       siguiendo este mismo patron cuando se completen las entidades.
