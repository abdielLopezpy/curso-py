#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simula el guardado de objetos JSON en una base de datos."""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).parent
DATOS_DIR = BASE_DIR / "datos"
DATOS_DIR.mkdir(exist_ok=True)

REGISTROS_PATH = DATOS_DIR / "registros.json"
BITACORA_PATH = DATOS_DIR / "bitacora.json"


def _leer_json(path: Path) -> Any:
    """Carga el contenido JSON del path indicado o retorna una lista vacía."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as archivo:
        return json.load(archivo)


def _escribir_json(path: Path, data: Any) -> None:
    """Serializa datos en disco con indentación y codificación UTF-8."""
    with path.open("w", encoding="utf-8") as archivo:
        json.dump(data, archivo, ensure_ascii=False, indent=2)


@dataclass
class Cliente:
    """Entidad liviana que representa un registro dentro de la colección."""

    id: int
    nombre: str
    ciudad: str
    saldo: float

    def to_record(self) -> Dict[str, Any]:
        """Convierte la instancia en un diccionario listo para serializar."""
        return asdict(self)


class JsonDatabase:
    """Almacena registros en archivos JSON simulando persistencia."""

    def __init__(self, registros_path: Path, bitacora_path: Path) -> None:
        self.registros_path = registros_path
        self.bitacora_path = bitacora_path
        self.registros: List[Dict[str, Any]] = _leer_json(self.registros_path)
        self.historial: List[Dict[str, Any]] = _leer_json(self.bitacora_path)
        print(f"Base inicializada con {len(self.registros)} registros.")

    def insertar_registro(self, data: Dict[str, Any]) -> None:
        """Inserta un registro y escribe la operación en bitácora."""
        if "id" not in data:
            raise ValueError("Todo registro necesita un 'id' único")

        if any(reg["id"] == data["id"] for reg in self.registros):
            raise ValueError(f"Ya existe un registro con id {data['id']}")

        self.registros.append(data)
        self._registrar_evento("INSERT", data["id"], data)
        self._persistir()
        print(f"Registro {data['id']} almacenado correctamente.")

    def consultar(self, campo: Optional[str] = None, valor: Any = None) -> List[Dict[str, Any]]:
        """Filtra registros en memoria simulando una consulta simple."""
        if campo is None:
            return list(self.registros)
        return [registro for registro in self.registros if registro.get(campo) == valor]

    def _registrar_evento(self, tipo: str, registro_id: Any, payload: Dict[str, Any]) -> None:
        """Inserta una entrada de auditoría y persiste la bitácora."""
        evento = {
            "tipo": tipo,
            "registro_id": registro_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }
        self.historial.append(evento)
        _escribir_json(self.bitacora_path, self.historial)

    def _persistir(self) -> None:
        """Escribe el estado de registros en disco (persistencia)."""
        _escribir_json(self.registros_path, self.registros)


def poblar_base(json_db: JsonDatabase) -> None:
    """Crea clientes y los inserta en la base simulada."""
    clientes = [
        Cliente(id=101, nombre="Ana", ciudad="Bogotá", saldo=150.0),
        Cliente(id=102, nombre="Carlos", ciudad="Lima", saldo=89.99),
        Cliente(id=103, nombre="María", ciudad="Quito", saldo=120.5),
    ]

    for cliente in clientes:
        json_db.insertar_registro(cliente.to_record())


def mostrar_consultas(json_db: JsonDatabase) -> None:
    """Imprime en consola ejemplos de consultas generales y filtradas."""
    print("\nConsulta general (todos los registros):")
    for registro in json_db.consultar():
        print(f"- {registro['id']} | {registro['nombre']} | {registro['ciudad']}")

    print("\nConsulta filtrada por ciudad = Lima:")
    for registro in json_db.consultar(campo="ciudad", valor="Lima"):
        print(f"- {registro['id']} | {registro['nombre']} | saldo {registro['saldo']}")


def main() -> None:
    """Punto de entrada interactivo para la simulación."""
    db = JsonDatabase(REGISTROS_PATH, BITACORA_PATH)

    if not db.registros:
        poblar_base(db)
    else:
        print("Datos existentes detectados; no se llenó la base automáticamente.")

    try:
        db.insertar_registro(Cliente(id=104, nombre="Miguel", ciudad="Bogotá", saldo=99.0).to_record())
    except ValueError as exc:
        print(f"Error al insertar: {exc}")

    mostrar_consultas(db)
    print("\nRevisa los archivos en la carpeta datos para ver la persistencia en JSON.")


if __name__ == "__main__":
    main()
