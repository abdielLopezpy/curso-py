# ============================================================================
# Conexion SQLite
# ============================================================================
# Punto unico donde se sabe DONDE esta la BD y COMO abrir una conexion.
# Usado tanto por init_db (one-shot) como por la API (una conexion por request,
# inyectada en los endpoints via interfaces/dependencies.get_db).
# ============================================================================

import os
import sqlite3
from contextlib import contextmanager
from typing import Iterator


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATABASE_PATH = os.path.join(BASE_DIR, "cineflix.db")


def _connect() -> sqlite3.Connection:
    con = sqlite3.connect(DATABASE_PATH)
    con.row_factory = sqlite3.Row             # filas accesibles por nombre
    con.execute("PRAGMA foreign_keys = ON;")  # SQLite las apaga por defecto
    return con


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Conexion transaccional: commit al salir limpio, rollback si hay error."""
    con = _connect()
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
