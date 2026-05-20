"""Punto de entrada de App Pedidos.

Hoy: solo inicializa la base de datos (crea tablas + carga seed).
Manana: se conectaran los casos de uso desde aqui (CLI o API).

Ejecutar:
    cd Semana_12/app_pedidos
    python main.py
"""

from infrastructure.database.connection import DATABASE_PATH
from infrastructure.database.init_db import init_db


def main() -> None:
    init_db()
    print(f"Base de datos lista en: {DATABASE_PATH}")


if __name__ == "__main__":
    main()
