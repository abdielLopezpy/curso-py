#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    MODELOS DE ENTIDADES - GIMNASIO                  ║
║                                                                      ║
║  Define las entidades del sistema:                                  ║
║  - Miembro                                                           ║
║  - Entrenador                                                        ║
║  - Clase                                                             ║
║  - Suscripcion                                                       ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict
import sys

# Agregar la carpeta framework al path para poder importar
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

from database_framework import (
    Entidad,
    validar_no_vacio,
    validar_positivo,
    validar_rango,
    validar_cedula,
    validar_fecha,
)


@dataclass
class Miembro(Entidad):
    """
    Representa un miembro del gimnasio.

    Atributos:
        id: Identificador único del miembro
        nombre: Nombre completo del miembro
        edad: Edad del miembro (debe ser mayor de 16 años)
        email: Correo electrónico de contacto
        telefono: Número de teléfono
        membresia_activa: Estado de la membresía (True si está activa)
        fecha_registro: Fecha en que se registró el miembro
        cedula: Cédula de identidad del miembro
    """
    id: int
    nombre: str
    edad: int
    email: str
    telefono: str
    membresia_activa: bool
    fecha_registro: str
    cedula: str = ""

    def obtener_id(self) -> int:
        return self.id

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> Miembro:
        return cls(**datos)

    def validar(self) -> bool:
        """
        Valida que los datos del miembro sean correctos.

        Validaciones:
        - El nombre no puede estar vacío
        - La edad debe ser mayor a 16 años
        - El email no puede estar vacío
        - El teléfono no puede estar vacío
        - La cédula debe ser válida

        Retorna True si todo es válido, False si hay errores.
        """
        if not validar_no_vacio(self.nombre, "nombre"):
            return False

        if not validar_rango(self.edad, 16, 100, "edad"):
            return False

        if not validar_no_vacio(self.email, "email"):
            return False

        if not validar_no_vacio(self.telefono, "telefono"):
            return False

        if not validar_cedula(self.cedula, "cédula"):
            return False

        return True


@dataclass
class Entrenador(Entidad):
    """
    Representa un entrenador del gimnasio.

    Atributos:
        id: Identificador único del entrenador
        nombre: Nombre completo del entrenador
        especialidad: Área de especialización (ej: "CrossFit", "Yoga", "Spinning")
        años_experiencia: Años de experiencia profesional
        certificaciones: Certificaciones que posee
        email: Correo electrónico de contacto
        disponible: Indica si está disponible para nuevas clases
    """
    id: int
    nombre: str
    especialidad: str
    años_experiencia: int
    certificaciones: str
    email: str
    disponible: bool

    def obtener_id(self) -> int:
        return self.id

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> Entrenador:
        return cls(**datos)

    def validar(self) -> bool:
        """
        Valida que los datos del entrenador sean correctos.

        Validaciones:
        - El nombre no puede estar vacío
        - La especialidad no puede estar vacía
        - Los años de experiencia deben ser positivos
        - El email no puede estar vacío
        """
        if not validar_no_vacio(self.nombre, "nombre"):
            return False

        if not validar_no_vacio(self.especialidad, "especialidad"):
            return False

        if not validar_positivo(self.años_experiencia, "años de experiencia"):
            return False

        if not validar_no_vacio(self.email, "email"):
            return False

        return True


@dataclass
class Clase(Entidad):
    """
    Representa una clase de entrenamiento en el gimnasio.
    Esta entidad RELACIONA a Miembros con Entrenadores.

    Atributos:
        id: Identificador único de la clase
        nombre_clase: Nombre de la clase (ej: "Spinning Matutino", "Yoga Principiantes")
        entrenador_id: ID del entrenador que imparte la clase
        miembro_id: ID del miembro inscrito en la clase
        fecha: Fecha de la clase (formato: YYYY-MM-DD)
        hora: Hora de la clase (formato: HH:MM)
        duracion_minutos: Duración en minutos
        salon: Número de salón donde se imparte
        estado: Estado de la clase ("programada", "completada", "cancelada")
    """
    id: int
    nombre_clase: str
    entrenador_id: int  # 🔗 Referencia a Entrenador
    miembro_id: int     # 🔗 Referencia a Miembro
    fecha: str
    hora: str
    duracion_minutos: int
    salon: str
    estado: str

    def obtener_id(self) -> int:
        return self.id

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> Clase:
        return cls(**datos)

    def validar(self) -> bool:
        """
        Valida que los datos de la clase sean correctos.

        Validaciones:
        - El nombre de la clase no puede estar vacío
        - Los IDs deben ser positivos
        - La duración debe ser positiva
        - El estado debe ser válido
        """
        if not validar_no_vacio(self.nombre_clase, "nombre de clase"):
            return False

        if not validar_positivo(self.entrenador_id, "ID del entrenador"):
            return False

        if not validar_positivo(self.miembro_id, "ID del miembro"):
            return False

        if not validar_positivo(self.duracion_minutos, "duración"):
            return False

        estados_validos = ["programada", "completada", "cancelada"]
        if self.estado not in estados_validos:
            print(f"❌ Error: El estado debe ser uno de {estados_validos}")
            return False

        return True


@dataclass
class Suscripcion(Entidad):
    """
    Representa una suscripción de un miembro en el gimnasio.

    Atributos:
        id: Identificador único de la suscripción
        miembro_id: ID del miembro que tiene la suscripción
        fecha_inicio: Fecha de inicio de la suscripción
        fecha_fin: Fecha de fin de la suscripción
        tipo: Tipo de suscripción (ej: "mensual", "anual")
    """
    id: int
    miembro_id: int
    fecha_inicio: str
    fecha_fin: str
    tipo: str

    def obtener_id(self) -> int:
        return self.id

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> Suscripcion:
        return cls(**datos)

    def validar(self) -> bool:
        """
        Valida que los datos de la suscripción sean correctos.

        Validaciones:
        - El ID del miembro debe ser positivo
        - Las fechas deben ser válidas
        - El tipo debe ser uno de los tipos permitidos
        """
        if not validar_positivo(self.miembro_id, "ID del miembro"):
            return False

        if not validar_fecha(self.fecha_inicio, "fecha de inicio"):
            return False

        if not validar_fecha(self.fecha_fin, "fecha de fin"):
            return False

        tipos_permitidos = ["mensual", "anual"]
        if self.tipo not in tipos_permitidos:
            print(f"❌ Error: El tipo debe ser uno de {tipos_permitidos}")
            return False

        return True
