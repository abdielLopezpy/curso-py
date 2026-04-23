# ============================================================================
# IMPLEMENTACION: PrestamoSQLModelRepository
# ============================================================================
# Completar siguiendo el patron de libro_sqlmodel_repository.py.
# ============================================================================

from typing import List, Optional

from sqlmodel import Session, select

from domain.entities.prestamo import Prestamo
from domain.repositories.prestamo_repository import PrestamoRepository


class PrestamoSQLModelRepository(PrestamoRepository):

    def __init__(self, session: Session) -> None:
        self.session = session

    def listar(self) -> List[Prestamo]:
        # TODO: implementar.
        return []
