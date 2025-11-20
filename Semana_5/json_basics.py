#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Demostraciones básicas sobre objetos JSON en Python."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

BASE_DIR = Path(__file__).parent
DATOS_DIR = BASE_DIR / "datos"
DATOS_DIR.mkdir(exist_ok=True)

CLIENTES_PATH = DATOS_DIR / "clientes.json"
EVENTOS_PATH = DATOS_DIR / "eventos.json"


def crear_objeto_python() -> Dict[str, Any]:
    """Crea un diccionario con información de ejemplo."""
    return {
        "id": 1,
        "nombre": "Lucía",
        "activo": True,
        "saldo": 250.75,
        "roles": ["admin", "editor"],
        "preferencias": {"idioma": "es", "tema": "oscuro"},
    }


def convertir_a_json(data: Dict[str, Any]) -> str:
    """Serializa un diccionario a texto JSON con indentación."""
    return json.dumps(data, ensure_ascii=False, indent=2)


def guardar_clientes_registro(clientes: List[Dict[str, Any]]) -> None:
    """Guarda una lista de clientes dentro de la carpeta de datos."""
    with CLIENTES_PATH.open("w", encoding="utf-8") as archivo:
        json.dump(clientes, archivo, ensure_ascii=False, indent=2)
    print(f"Archivo guardado en: {CLIENTES_PATH.relative_to(BASE_DIR.parent)}")


def leer_clientes_registro() -> List[Dict[str, Any]]:
    """Lee el archivo JSON y retorna la lista de clientes."""
    with CLIENTES_PATH.open(encoding="utf-8") as archivo:
        return json.load(archivo)


def registrar_evento(tipo: str, payload: Dict[str, Any]) -> None:
    """Agrega un evento al archivo eventos.json para simular logs."""
    eventos: List[Dict[str, Any]] = []
    if EVENTOS_PATH.exists():
        with EVENTOS_PATH.open(encoding="utf-8") as archivo:
            eventos = json.load(archivo)

    eventos.append(
        {
            "tipo": tipo,
            "payload": payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )

    with EVENTOS_PATH.open("w", encoding="utf-8") as archivo:
        json.dump(eventos, archivo, ensure_ascii=False, indent=2)


def main() -> None:
    print("=" * 60)
    print("Semana 5 - Objetos JSON".center(60))
    print("=" * 60)

    ejemplo = crear_objeto_python()
    print("\n1) Diccionario en Python:\n", ejemplo)

    json_string = convertir_a_json(ejemplo)
    print("\n2) Objeto serializado a JSON:\n", json_string)

    clientes = [
        {"id": 1, "nombre": "Lucía", "saldo": 250.75, "ciudad": "Bogotá"},
        {"id": 2, "nombre": "Samuel", "saldo": 99.99, "ciudad": "Lima"},
        {"id": 3, "nombre": "Valentina", "saldo": 120.0, "ciudad": "Quito"},
    ]
    guardar_clientes_registro(clientes)

    print("\n3) Contenido leído desde clientes.json:")
    clientes_desde_archivo = leer_clientes_registro()
    for cliente in clientes_desde_archivo:
        print(f"- {cliente['id']:02d} | {cliente['nombre']} | saldo: {cliente['saldo']}")

    registrar_evento("LECTURA", {"total_clientes": len(clientes_desde_archivo)})
    print("\n4) Evento registrado en eventos.json")

    print("\nConsulta rápida del archivo de eventos:")
    with EVENTOS_PATH.open(encoding="utf-8") as archivo:
        for evento in json.load(archivo):
            print(f"[{evento['timestamp']}] {evento['tipo']} -> {evento['payload']}")

    print("\nListo. Puedes abrir los archivos en la carpeta datos para revisarlos.")


if __name__ == "__main__":
    main()
