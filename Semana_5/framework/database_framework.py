#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Framework de Base de Datos JSON
================================
Este módulo proporciona toda la infraestructura necesaria para crear
un sistema de gestión de datos usando archivos JSON.

NO NECESITAS MODIFICAR ESTE ARCHIVO.
Solo importa las clases y úsalas en tu proyecto.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, TypeVar, Generic, Type
from enum import Enum


class TipoOperacion(Enum):
    """Tipos de operaciones que se pueden registrar en la bitácora."""
    CREAR = "CREATE"
    LEER = "READ"
    ACTUALIZAR = "UPDATE"
    ELIMINAR = "DELETE"
    CONSULTAR = "QUERY"


@dataclass
class Entidad(ABC):
    """
    Clase base para todas las entidades del sistema.

    Todas tus entidades deben heredar de esta clase y tener un campo 'id'.

    Ejemplo:
        @dataclass
        class Producto(Entidad):
            id: int
            nombre: str
            precio: float
    """

    @abstractmethod
    def obtener_id(self) -> Any:
        """Retorna el identificador único de la entidad."""
        pass

    def a_diccionario(self) -> Dict[str, Any]:
        """Convierte la entidad a un diccionario para serialización JSON."""
        return asdict(self)

    @classmethod
    @abstractmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> Entidad:
        """Crea una instancia de la entidad desde un diccionario."""
        pass

    def __str__(self) -> str:
        """Representación en texto de la entidad."""
        campos = ", ".join(f"{k}={v}" for k, v in self.a_diccionario().items())
        return f"{self.__class__.__name__}({campos})"


T = TypeVar('T', bound=Entidad)


class RepositorioJSON(Generic[T]):
    """
    Repositorio genérico que maneja el almacenamiento de entidades en JSON.

    Proporciona operaciones CRUD completas:
    - Crear (insertar)
    - Leer (consultar)
    - Actualizar (modificar)
    - Eliminar (borrar)

    Parámetros:
        nombre_coleccion: Nombre del archivo JSON (sin extensión)
        tipo_entidad: La clase de la entidad que se va a almacenar
        directorio_datos: Carpeta donde se guardarán los archivos

    Ejemplo:
        repositorio = RepositorioJSON("productos", Producto, Path("datos"))
        repositorio.insertar(producto1)
        productos = repositorio.consultar_todos()
    """

    def __init__(
        self,
        nombre_coleccion: str,
        tipo_entidad: Type[T],
        directorio_datos: Path
    ):
        self.nombre_coleccion = nombre_coleccion
        self.tipo_entidad = tipo_entidad
        self.directorio_datos = directorio_datos
        self.directorio_datos.mkdir(parents=True, exist_ok=True)

        self.ruta_datos = self.directorio_datos / f"{nombre_coleccion}.json"
        self.ruta_bitacora = self.directorio_datos / f"{nombre_coleccion}_bitacora.json"

        self._datos: List[Dict[str, Any]] = self._cargar_datos()
        self._bitacora: List[Dict[str, Any]] = self._cargar_bitacora()

        print(f"📦 Repositorio '{nombre_coleccion}' inicializado con {len(self._datos)} registros.")

    # ==================== MÉTODOS PRIVADOS ====================

    def _cargar_datos(self) -> List[Dict[str, Any]]:
        """Carga los datos desde el archivo JSON."""
        if not self.ruta_datos.exists():
            return []

        with self.ruta_datos.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def _cargar_bitacora(self) -> List[Dict[str, Any]]:
        """Carga la bitácora de operaciones desde el archivo JSON."""
        if not self.ruta_bitacora.exists():
            return []

        with self.ruta_bitacora.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def _guardar_datos(self) -> None:
        """Persiste los datos en el archivo JSON."""
        with self.ruta_datos.open("w", encoding="utf-8") as archivo:
            json.dump(self._datos, archivo, ensure_ascii=False, indent=2)

    def _guardar_bitacora(self) -> None:
        """Persiste la bitácora en el archivo JSON."""
        with self.ruta_bitacora.open("w", encoding="utf-8") as archivo:
            json.dump(self._bitacora, archivo, ensure_ascii=False, indent=2)

    def _registrar_operacion(
        self,
        tipo: TipoOperacion,
        entidad_id: Any,
        datos: Optional[Dict[str, Any]] = None,
        mensaje: str = ""
    ) -> None:
        """Registra una operación en la bitácora para auditoría."""
        evento = {
            "tipo": tipo.value,
            "entidad_id": entidad_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "mensaje": mensaje,
            "datos": datos
        }
        self._bitacora.append(evento)
        self._guardar_bitacora()

    def _existe_id(self, entidad_id: Any) -> bool:
        """Verifica si ya existe una entidad con el ID dado."""
        return any(
            self.tipo_entidad.desde_diccionario(dato).obtener_id() == entidad_id
            for dato in self._datos
        )

    def _encontrar_indice(self, entidad_id: Any) -> Optional[int]:
        """Encuentra el índice de una entidad por su ID."""
        for idx, dato in enumerate(self._datos):
            if self.tipo_entidad.desde_diccionario(dato).obtener_id() == entidad_id:
                return idx
        return None

    # ==================== OPERACIONES CRUD ====================

    def insertar(self, entidad: T) -> bool:
        """
        Inserta una nueva entidad en el repositorio.

        Args:
            entidad: La entidad a insertar

        Returns:
            True si se insertó correctamente, False si ya existe

        Ejemplo:
            exito = repositorio.insertar(producto)
        """
        entidad_id = entidad.obtener_id()

        if self._existe_id(entidad_id):
            print(f"❌ Error: Ya existe una entidad con ID {entidad_id}")
            return False

        datos_entidad = entidad.a_diccionario()
        self._datos.append(datos_entidad)
        self._guardar_datos()
        self._registrar_operacion(
            TipoOperacion.CREAR,
            entidad_id,
            datos_entidad,
            f"Entidad {entidad_id} creada"
        )

        print(f"✅ Entidad {entidad_id} insertada correctamente")
        return True

    def consultar_por_id(self, entidad_id: Any) -> Optional[T]:
        """
        Busca una entidad por su ID.

        Args:
            entidad_id: El ID de la entidad a buscar

        Returns:
            La entidad encontrada o None si no existe

        Ejemplo:
            producto = repositorio.consultar_por_id(1)
        """
        indice = self._encontrar_indice(entidad_id)
        if indice is None:
            return None

        self._registrar_operacion(
            TipoOperacion.LEER,
            entidad_id,
            mensaje=f"Consulta de entidad {entidad_id}"
        )

        return self.tipo_entidad.desde_diccionario(self._datos[indice])

    def consultar_todos(self) -> List[T]:
        """
        Retorna todas las entidades del repositorio.

        Returns:
            Lista con todas las entidades

        Ejemplo:
            todos = repositorio.consultar_todos()
        """
        self._registrar_operacion(
            TipoOperacion.CONSULTAR,
            "ALL",
            mensaje=f"Consulta de todas las entidades ({len(self._datos)} registros)"
        )

        return [
            self.tipo_entidad.desde_diccionario(dato)
            for dato in self._datos
        ]

    def consultar_por_campo(self, campo: str, valor: Any) -> List[T]:
        """
        Busca entidades que tengan un valor específico en un campo.

        Args:
            campo: Nombre del campo a filtrar
            valor: Valor que debe tener el campo

        Returns:
            Lista de entidades que cumplen la condición

        Ejemplo:
            productos_caros = repositorio.consultar_por_campo("precio", 100.0)
        """
        resultados = [
            self.tipo_entidad.desde_diccionario(dato)
            for dato in self._datos
            if dato.get(campo) == valor
        ]

        self._registrar_operacion(
            TipoOperacion.CONSULTAR,
            "FILTRO",
            {"campo": campo, "valor": valor},
            f"Consulta filtrada: {campo}={valor} ({len(resultados)} resultados)"
        )

        return resultados

    def actualizar(self, entidad: T) -> bool:
        """
        Actualiza una entidad existente.

        Args:
            entidad: La entidad con los datos actualizados

        Returns:
            True si se actualizó, False si no existe

        Ejemplo:
            producto.precio = 150.0
            exito = repositorio.actualizar(producto)
        """
        entidad_id = entidad.obtener_id()
        indice = self._encontrar_indice(entidad_id)

        if indice is None:
            print(f"❌ Error: No existe una entidad con ID {entidad_id}")
            return False

        datos_entidad = entidad.a_diccionario()
        self._datos[indice] = datos_entidad
        self._guardar_datos()
        self._registrar_operacion(
            TipoOperacion.ACTUALIZAR,
            entidad_id,
            datos_entidad,
            f"Entidad {entidad_id} actualizada"
        )

        print(f"✅ Entidad {entidad_id} actualizada correctamente")
        return True

    def eliminar(self, entidad_id: Any) -> bool:
        """
        Elimina una entidad por su ID.

        Args:
            entidad_id: El ID de la entidad a eliminar

        Returns:
            True si se eliminó, False si no existe

        Ejemplo:
            exito = repositorio.eliminar(1)
        """
        indice = self._encontrar_indice(entidad_id)

        if indice is None:
            print(f"❌ Error: No existe una entidad con ID {entidad_id}")
            return False

        dato_eliminado = self._datos.pop(indice)
        self._guardar_datos()
        self._registrar_operacion(
            TipoOperacion.ELIMINAR,
            entidad_id,
            dato_eliminado,
            f"Entidad {entidad_id} eliminada"
        )

        print(f"✅ Entidad {entidad_id} eliminada correctamente")
        return True

    def contar(self) -> int:
        """
        Retorna el número total de entidades.

        Returns:
            Cantidad de entidades en el repositorio

        Ejemplo:
            total = repositorio.contar()
        """
        return len(self._datos)

    def existe(self, entidad_id: Any) -> bool:
        """
        Verifica si existe una entidad con el ID dado.

        Args:
            entidad_id: El ID a verificar

        Returns:
            True si existe, False si no

        Ejemplo:
            if repositorio.existe(1):
                print("El producto existe")
        """
        return self._existe_id(entidad_id)

    # ==================== MÉTODOS DE UTILIDAD ====================

    def limpiar_todo(self) -> None:
        """
        ADVERTENCIA: Elimina TODOS los datos y la bitácora.
        Usar solo para resetear completamente el repositorio.
        """
        self._datos = []
        self._bitacora = []
        self._guardar_datos()
        self._guardar_bitacora()
        print(f"🗑️  Repositorio '{self.nombre_coleccion}' limpiado completamente")

    def mostrar_estadisticas(self) -> None:
        """Muestra estadísticas del repositorio."""
        print(f"\n📊 Estadísticas del repositorio '{self.nombre_coleccion}':")
        print(f"   Total de registros: {len(self._datos)}")
        print(f"   Total de operaciones: {len(self._bitacora)}")
        print(f"   Archivo de datos: {self.ruta_datos}")
        print(f"   Archivo de bitácora: {self.ruta_bitacora}")

    def mostrar_bitacora(self, ultimas: int = 10) -> None:
        """
        Muestra las últimas operaciones registradas en la bitácora.

        Args:
            ultimas: Número de operaciones a mostrar (por defecto 10)
        """
        print(f"\n📜 Últimas {ultimas} operaciones:")
        for evento in self._bitacora[-ultimas:]:
            timestamp = evento["timestamp"].split("T")[1][:8]
            print(f"   [{timestamp}] {evento['tipo']:10} | ID: {evento['entidad_id']:10} | {evento['mensaje']}")


class SistemaGestion:
    """
    Clase base para crear sistemas de gestión completos.

    Hereda de esta clase para crear tu propio sistema que maneje
    múltiples entidades de forma organizada.

    Ejemplo:
        class SistemaTienda(SistemaGestion):
            def __init__(self):
                super().__init__("datos_tienda")
                self.productos = RepositorioJSON("productos", Producto, self.directorio_datos)
                self.clientes = RepositorioJSON("clientes", Cliente, self.directorio_datos)
    """

    def __init__(self, nombre_sistema: str, directorio_base: Optional[Path] = None):
        self.nombre_sistema = nombre_sistema

        if directorio_base is None:
            directorio_base = Path(__file__).parent / "datos"

        self.directorio_datos = directorio_base / nombre_sistema
        self.directorio_datos.mkdir(parents=True, exist_ok=True)

        print(f"\n{'='*60}")
        print(f"🚀 Sistema '{nombre_sistema}' inicializado".center(60))
        print(f"{'='*60}")
        print(f"📁 Directorio de datos: {self.directorio_datos}\n")

    def mostrar_resumen(self) -> None:
        """Muestra un resumen de todos los repositorios del sistema."""
        print(f"\n{'='*60}")
        print(f"📋 Resumen del sistema '{self.nombre_sistema}'".center(60))
        print(f"{'='*60}")


# ==================== FUNCIONES DE UTILIDAD ====================

def validar_no_vacio(valor: str, nombre_campo: str) -> bool:
    """Valida que un campo de texto no esté vacío."""
    if not valor or not valor.strip():
        print(f"❌ Error: El campo '{nombre_campo}' no puede estar vacío")
        return False
    return True


def validar_positivo(valor: float, nombre_campo: str) -> bool:
    """Valida que un número sea positivo."""
    if valor < 0:
        print(f"❌ Error: El campo '{nombre_campo}' debe ser positivo")
        return False
    return True


def validar_rango(valor: Any, minimo: Any, maximo: Any, nombre_campo: str) -> bool:
    """Valida que un valor esté dentro de un rango."""
    if not (minimo <= valor <= maximo):
        print(f"❌ Error: El campo '{nombre_campo}' debe estar entre {minimo} y {maximo}")
        return False
    return True


def validar_fecha(fecha: str, nombre_campo: str) -> bool:
    """Valida que una fecha esté en formato correcto (YYYY-MM-DD)."""
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        print(f"❌ Error: El campo '{nombre_campo}' debe estar en formato YYYY-MM-DD")
        return False
    return True


def validar_cedula(cedula: str, nombre_campo: str) -> bool:
    """Valida que una cédula tenga un formato correcto (números y longitud adecuada). 0-000-000 a 9-999-999-9"""
    import re
    patron = r'^\d-\d{3}-\d{3}-\d$'
    if not re.match(patron, cedula):
        print(f"❌ Error: El campo '{nombre_campo}' debe tener el formato X-XXX-XXX-X")
        return False
    return True

def mostrar_tabla(entidades: List[Entidad], titulo: str = "Registros") -> None:
    """
    Muestra una lista de entidades en formato de tabla.

    Args:
        entidades: Lista de entidades a mostrar
        titulo: Título de la tabla
    """
    if not entidades:
        print(f"\n📭 No hay {titulo.lower()} para mostrar")
        return

    print(f"\n{'='*60}")
    print(f"📋 {titulo} ({len(entidades)})".center(60))
    print(f"{'='*60}")

    for idx, entidad in enumerate(entidades, 1):
        print(f"{idx}. {entidad}")

    print(f"{'='*60}")


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           FRAMEWORK DE BASE DE DATOS JSON                   ║
║                                                              ║
║  Este es un módulo de infraestructura.                      ║
║  Importa las clases en tu proyecto para usarlas.            ║
║                                                              ║
║  Clases principales:                                         ║
║    • Entidad          - Clase base para tus entidades        ║
║    • RepositorioJSON  - Maneja operaciones CRUD              ║
║    • SistemaGestion   - Clase base para tu sistema           ║
║                                                              ║
║  Ver ejemplo_tienda.py para un ejemplo completo.            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
