# ============================================================================
# CONEXION A LA BASE DE DATOS
# ============================================================================
# Un solo engine compartido por toda la app.
# La sesion (Session) se crea por request via inyeccion de dependencias
# (ver interfaces/dependencies.py).
# ============================================================================

import os
from typing import Iterator

from sqlmodel import Session, create_engine


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATABASE_PATH = os.path.join(BASE_DIR, "biblioteca.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# check_same_thread=False porque FastAPI puede correr requests en hilos distintos.
engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


def get_session() -> Iterator[Session]:
    """Dependency de FastAPI: abre una sesion y la cierra al terminar el request."""
    with Session(engine) as session:
        yield session
