import os
import sqlite3
from contextlib import contextmanager
from typing import Iterator


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATABASE_PATH = os.path.join(BASE_DIR, "pedidos.db")


def _connect() -> sqlite3.Connection:
    con = sqlite3.connect(DATABASE_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON;")
    return con


@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    con = _connect()
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
