# ============================================================================
# INTERFAZ de repositorio: LibroRepository
# ============================================================================
# Contrato abstracto. Dice QUE hace un repositorio, no COMO.
# La implementacion concreta vive en:
#   infrastructure/repositories/libro_sqlite_repository.py
#
# Asi podriamos cambiar SQLite por Postgres, Mongo, memoria, etc. sin tocar
# ni el dominio ni los use cases.
# ============================================================================

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.libro import Libro


class LibroRepository(ABC):

    @abstractmethod
    def listar(self) -> List[Libro]:
        ...

    @abstractmethod
    def obtener_por_id(self, libro_id: int) -> Optional[Libro]:
        ...

    @abstractmethod
    def crear(self, libro: Libro) -> Libro:
        ...

    @abstractmethod
    def actualizar(self, libro: Libro) -> Optional[Libro]:
        ...

    @abstractmethod
    def eliminar(self, libro_id: int) -> bool:
        ...
