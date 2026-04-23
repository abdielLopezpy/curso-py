# ============================================================================
# IMPLEMENTACION: AutorSQLModelRepository
# ============================================================================
# Completar siguiendo el patron de libro_sqlmodel_repository.py.
# ============================================================================

from typing import List, Optional

from sqlmodel import Session, select

from domain.entities.autor import Autor
from domain.repositories.autor_repository import AutorRepository


class AutorSQLModelRepository(AutorRepository):

    def __init__(self, session: Session) -> None:
        self.session = session

    def listar(self) -> List[Autor]:
        # TODO: implementar con select() y session.exec().
        return []
