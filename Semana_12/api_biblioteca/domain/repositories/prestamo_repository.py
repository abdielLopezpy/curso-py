# ============================================================================
# INTERFAZ de repositorio: PrestamoRepository
# ============================================================================
# Completar siguiendo el patron de domain/repositories/libro_repository.py.
#
# Metodos esperados:
#   listar()                     -> List[Prestamo]
#   obtener_por_id(prestamo_id)  -> Optional[Prestamo]
#   crear(prestamo)              -> Prestamo
#   actualizar(prestamo)         -> Optional[Prestamo]
#   eliminar(prestamo_id)        -> bool
#
# Extras opcionales:
#   listar_por_libro(libro_id)   -> List[Prestamo]
#   listar_activos()             -> List[Prestamo]  (fecha_devolucion IS NULL)
# ============================================================================

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.prestamo import Prestamo


class PrestamoRepository(ABC):

    @abstractmethod
    def listar(self) -> List[Prestamo]:
        ...
