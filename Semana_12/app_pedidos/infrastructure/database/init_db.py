import os
import sqlite3

from infrastructure.database.connection import DATABASE_PATH


SQL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "sql"))
SCHEMA_FILE = os.path.join(SQL_DIR, "schema.sql")
SEED_FILE = os.path.join(SQL_DIR, "seed.sql")


def _read(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def init_db() -> None:
    con = sqlite3.connect(DATABASE_PATH)
    try:
        con.executescript(_read(SCHEMA_FILE))
        con.executescript(_read(SEED_FILE))
        con.commit()
    finally:
        con.close()
