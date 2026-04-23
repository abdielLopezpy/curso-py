# ============================================================================
# INICIALIZACION de la base de datos
# ============================================================================
# Ejecuta sql/schema.sql y sql/seed.sql sobre biblioteca.db.
# Usamos SQL crudo para que los alumnos vean CREATE TABLE y FOREIGN KEY
# escritos a mano (no generados por un ORM).
#
# Se llama una sola vez al arrancar la app (ver main.py startup event).
# ============================================================================

import os
import sqlite3

from infrastructure.database.connection import DATABASE_PATH


SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sql"))
SCHEMA_FILE = os.path.join(SQL_DIR, "schema.sql")
SEED_FILE = os.path.join(SQL_DIR, "seed.sql")


def _read_sql(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def init_db() -> None:
    """Crea las tablas y carga datos de ejemplo si la BD esta vacia."""
    schema_sql = _read_sql(SCHEMA_FILE)
    seed_sql = _read_sql(SEED_FILE)

    con = sqlite3.connect(DATABASE_PATH)
    try:
        con.executescript(schema_sql)
        con.executescript(seed_sql)
        con.commit()
    finally:
        con.close()
