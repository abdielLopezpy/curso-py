# ============================================================================
# INTERFAZ de repositorio: AutorRepository
# ============================================================================
# Completar siguiendo el patron de domain/repositories/libro_repository.py.
#
# Metodos esperados:
#   listar()                 -> List[Autor]
#   obtener_por_id(autor_id) -> Optional[Autor]
#   crear(autor)             -> Autor
#   actualizar(autor)        -> Optional[Autor]
#   eliminar(autor_id)       -> bool
# ============================================================================

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.autor import Autor


class AutorRepository(ABC):

    @abstractmethod
    def listar(self) -> List[Autor]:
        ...
