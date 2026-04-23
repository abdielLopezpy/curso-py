# ============================================================================
# IMPLEMENTACION CONCRETA: LibroSQLModelRepository
# ============================================================================
# Traduce operaciones del dominio a queries sobre SQLite usando SQLModel.
# Solo esta clase sabe que la BD es SQLite. Si manana cambiamos a Postgres,
# este es el unico archivo que habria que reemplazar.
# ============================================================================

from typing import List, Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from domain.entities.libro import Libro
from domain.exceptions import EntidadDuplicada
from domain.repositories.libro_repository import LibroRepository


class LibroSQLModelRepository(LibroRepository):

    def __init__(self, session: Session) -> None:
        self.session = session

    def listar(self) -> List[Libro]:
        statement = select(Libro).order_by(Libro.id)
        return list(self.session.exec(statement).all())

    def obtener_por_id(self, libro_id: int) -> Optional[Libro]:
        return self.session.get(Libro, libro_id)

    def crear(self, libro: Libro) -> Libro:
        self.session.add(libro)
        try:
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            raise EntidadDuplicada(f"ISBN ya registrado: {libro.isbn}") from e
        self.session.refresh(libro)
        return libro

    def actualizar(self, libro: Libro) -> Optional[Libro]:
        if libro.id is None:
            return None
        existente = self.session.get(Libro, libro.id)
        if existente is None:
            return None
        # SQLModel detecta los cambios en el objeto adherido a la sesion.
        self.session.add(libro)
        try:
            self.session.commit()
        except IntegrityError as e:
            self.session.rollback()
            raise EntidadDuplicada(f"ISBN ya registrado: {libro.isbn}") from e
        self.session.refresh(libro)
        return libro

    def eliminar(self, libro_id: int) -> bool:
        libro = self.session.get(Libro, libro_id)
        if libro is None:
            return False
        self.session.delete(libro)
        self.session.commit()
        return True
