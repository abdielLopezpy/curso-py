#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    🎯 DESAFÍO SEMANA 5                              ║
║              Sistema de Gestión con Archivos JSON                   ║
║                                                                      ║
║  OBJETIVO:                                                           ║
║  Crear un sistema completo de gestión con 3 entidades que           ║
║  guarde toda la información en archivos JSON.                       ║
║                                                                      ║
║  SISTEMA IMPLEMENTADO: 💪 GESTIÓN DE GIMNASIO                       ║
║                                                                      ║
║  ENTIDADES:                                                          ║
║  ✅ Miembro - Personas registradas en el gimnasio                   ║
║  ✅ Entrenador - Profesionales que imparten clases                  ║
║  ✅ Clase - Sesiones de entrenamiento (relaciona Miembro-Entrenador)║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
import sys

# Agregar la carpeta framework al path para poder importar
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

# Importamos las clases del framework que YA ESTÁ LISTO
from Semana_5.framework.database_framework import validar_cedula, validar_fecha
from database_framework import (
    Entidad,
    RepositorioJSON,
    SistemaGestion,
    validar_no_vacio,
    validar_positivo,
    validar_rango,
    mostrar_tabla
)


# ═══════════════════════════════════════════════════════════════════
#                    🏗️ PASO 1: DEFINIR LAS ENTIDADES
# ═══════════════════════════════════════════════════════════════════

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
class Suscripcion:
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


# ═══════════════════════════════════════════════════════════════════
#              🎮 PASO 2: CREAR EL SISTEMA DE GESTIÓN
# ═══════════════════════════════════════════════════════════════════

class SistemaGimnasio(SistemaGestion):
    """
    Sistema completo de gestión para un gimnasio.

    Este sistema permite:
    - Registrar miembros y entrenadores
    - Programar clases que relacionan miembros con entrenadores
    - Consultar información de miembros, entrenadores y clases
    - Generar reportes y estadísticas
    - Gestionar la disponibilidad de entrenadores
    - Activar/desactivar membresías

    Todos los datos se persisten en archivos JSON.
    """

    def __init__(self):
        super().__init__("gimnasio")

        # Crear los tres repositorios para cada entidad
        self.miembros = RepositorioJSON(
            "miembros",
            Miembro,
            self.directorio_datos
        )

        self.entrenadores = RepositorioJSON(
            "entrenadores",
            Entrenador,
            self.directorio_datos
        )

        self.clases = RepositorioJSON(
            "clases",
            Clase,
            self.directorio_datos
        )

    # ══════════════════════════════════════════════════════════════
    #        📝 PASO 3: OPERACIONES BÁSICAS - MIEMBROS
    # ══════════════════════════════════════════════════════════════

    def agregar_miembro(self, miembro: Miembro) -> bool:
        """
        Agrega un nuevo miembro al gimnasio.

        Args:
            miembro: Instancia de Miembro con los datos del nuevo miembro

        Returns:
            True si se agregó correctamente, False si hubo un error
        """
        if not miembro.validar():
            return False

        resultado = self.miembros.insertar(miembro)
        if resultado:
            print(f"✅ Miembro {miembro.nombre} registrado exitosamente (ID: {miembro.id})")
        return resultado

    def listar_miembros(self) -> List[Miembro]:
        """Retorna todos los miembros registrados."""
        return self.miembros.consultar_todos()

    def buscar_miembro(self, id: int) -> Miembro | None:
        """Busca un miembro por su ID."""
        return self.miembros.consultar_por_id(id)

    def activar_membresia(self, miembro_id: int) -> bool:
        """
        Activa la membresía de un miembro.

        Args:
            miembro_id: ID del miembro

        Returns:
            True si se activó correctamente
        """
        miembro = self.buscar_miembro(miembro_id)
        if miembro is None:
            print(f"❌ Miembro con ID {miembro_id} no encontrado")
            return False

        miembro.membresia_activa = True
        self.miembros.actualizar(miembro)
        print(f"✅ Membresía activada para {miembro.nombre}")
        return True

    def desactivar_membresia(self, miembro_id: int) -> bool:
        """
        Desactiva la membresía de un miembro.

        Args:
            miembro_id: ID del miembro

        Returns:
            True si se desactivó correctamente
        """
        miembro = self.buscar_miembro(miembro_id)
        if miembro is None:
            print(f"❌ Miembro con ID {miembro_id} no encontrado")
            return False

        miembro.membresia_activa = False
        self.miembros.actualizar(miembro)
        print(f"✅ Membresía desactivada para {miembro.nombre}")
        return True

    # ══════════════════════════════════════════════════════════════
    #        📝 PASO 3: OPERACIONES BÁSICAS - ENTRENADORES
    # ══════════════════════════════════════════════════════════════

    def agregar_entrenador(self, entrenador: Entrenador) -> bool:
        """
        Agrega un nuevo entrenador al gimnasio.

        Args:
            entrenador: Instancia de Entrenador con los datos del nuevo entrenador

        Returns:
            True si se agregó correctamente, False si hubo un error
        """
        if not entrenador.validar():
            return False

        resultado = self.entrenadores.insertar(entrenador)
        if resultado:
            print(f"✅ Entrenador {entrenador.nombre} registrado exitosamente (ID: {entrenador.id})")
        return resultado

    def listar_entrenadores(self) -> List[Entrenador]:
        """Retorna todos los entrenadores registrados."""
        return self.entrenadores.consultar_todos()

    def buscar_entrenador(self, id: int) -> Entrenador | None:
        """Busca un entrenador por su ID."""
        return self.entrenadores.consultar_por_id(id)

    def listar_entrenadores_disponibles(self) -> List[Entrenador]:
        """
        Retorna solo los entrenadores que están disponibles.

        Returns:
            Lista de entrenadores con disponible=True
        """
        return [e for e in self.listar_entrenadores() if e.disponible]

    def cambiar_disponibilidad_entrenador(self, entrenador_id: int, disponible: bool) -> bool:
        """
        Cambia la disponibilidad de un entrenador.

        Args:
            entrenador_id: ID del entrenador
            disponible: True para marcar como disponible, False para no disponible

        Returns:
            True si se actualizó correctamente
        """
        entrenador = self.buscar_entrenador(entrenador_id)
        if entrenador is None:
            print(f"❌ Entrenador con ID {entrenador_id} no encontrado")
            return False

        entrenador.disponible = disponible
        self.entrenadores.actualizar(entrenador)
        estado = "disponible" if disponible else "no disponible"
        print(f"✅ Entrenador {entrenador.nombre} marcado como {estado}")
        return True

    # ══════════════════════════════════════════════════════════════
    #    🔗 PASO 4: OPERACIONES QUE RELACIONAN ENTIDADES - CLASES
    # ══════════════════════════════════════════════════════════════

    def programar_clase(
        self,
        nombre_clase: str,
        entrenador_id: int,
        miembro_id: int,
        fecha: str,
        hora: str,
        duracion_minutos: int,
        salon: str
    ) -> bool:
        """
        Programa una nueva clase relacionando un miembro con un entrenador.

        Esta es la operación principal que RELACIONA las entidades.

        Proceso:
        1. Verifica que el entrenador existe y está disponible
        2. Verifica que el miembro existe y tiene membresía activa
        3. Crea la clase con estado "programada"
        4. Guarda la clase en el repositorio

        Args:
            nombre_clase: Nombre descriptivo de la clase
            entrenador_id: ID del entrenador que impartirá la clase
            miembro_id: ID del miembro que tomará la clase
            fecha: Fecha en formato YYYY-MM-DD
            hora: Hora en formato HH:MM
            duracion_minutos: Duración de la clase
            salon: Número o nombre del salón

        Returns:
            True si la clase se programó exitosamente
        """
        print(f"\n📅 Programando clase: {nombre_clase}...")

        # 1. Verificar que el entrenador existe
        entrenador = self.buscar_entrenador(entrenador_id)
        if entrenador is None:
            print(f"❌ Entrenador con ID {entrenador_id} no encontrado")
            return False

        # 2. Verificar que el entrenador está disponible
        if not entrenador.disponible:
            print(f"❌ El entrenador {entrenador.nombre} no está disponible actualmente")
            return False

        # 3. Verificar que el miembro existe
        miembro = self.buscar_miembro(miembro_id)
        if miembro is None:
            print(f"❌ Miembro con ID {miembro_id} no encontrado")
            return False

        # 4. Verificar que el miembro tiene membresía activa
        if not miembro.membresia_activa:
            print(f"❌ El miembro {miembro.nombre} no tiene membresía activa")
            return False

        # 5. Crear la clase
        # Generar un ID único para la clase
        nuevo_id = self.clases.contar() + 1

        clase = Clase(
            id=nuevo_id,
            nombre_clase=nombre_clase,
            entrenador_id=entrenador_id,
            miembro_id=miembro_id,
            fecha=fecha,
            hora=hora,
            duracion_minutos=duracion_minutos,
            salon=salon,
            estado="programada"
        )

        # 6. Validar y guardar la clase
        if not clase.validar():
            return False

        resultado = self.clases.insertar(clase)
        if resultado:
            print(f"✅ Clase programada exitosamente")
            print(f"   📚 Clase: {nombre_clase}")
            print(f"   👨‍🏫 Entrenador: {entrenador.nombre}")
            print(f"   👤 Miembro: {miembro.nombre}")
            print(f"   📅 Fecha: {fecha} a las {hora}")
            print(f"   🏛️ Salón: {salon}")

        return resultado

    def completar_clase(self, clase_id: int) -> bool:
        """
        Marca una clase como completada.

        Args:
            clase_id: ID de la clase

        Returns:
            True si se actualizó correctamente
        """
        clase = self.clases.consultar_por_id(clase_id)
        if clase is None:
            print(f"❌ Clase con ID {clase_id} no encontrada")
            return False

        if clase.estado != "programada":
            print(f"❌ La clase no está en estado 'programada' (estado actual: {clase.estado})")
            return False

        clase.estado = "completada"
        self.clases.actualizar(clase)
        print(f"✅ Clase {clase.nombre_clase} marcada como completada")
        return True

    def cancelar_clase(self, clase_id: int) -> bool:
        """
        Cancela una clase programada.

        Args:
            clase_id: ID de la clase

        Returns:
            True si se canceló correctamente
        """
        clase = self.clases.consultar_por_id(clase_id)
        if clase is None:
            print(f"❌ Clase con ID {clase_id} no encontrada")
            return False

        if clase.estado != "programada":
            print(f"❌ Solo se pueden cancelar clases en estado 'programada'")
            return False

        clase.estado = "cancelada"
        self.clases.actualizar(clase)
        print(f"✅ Clase {clase.nombre_clase} cancelada")
        return True

    def listar_clases(self) -> List[Clase]:
        """Retorna todas las clases registradas."""
        return self.clases.consultar_todos()

    # ══════════════════════════════════════════════════════════════
    #              📊 PASO 5: REPORTES Y CONSULTAS
    # ══════════════════════════════════════════════════════════════

    def mostrar_resumen(self) -> None:
        """
        Muestra un resumen completo del estado del gimnasio.

        Incluye:
        - Total de miembros (activos e inactivos)
        - Total de entrenadores (disponibles y no disponibles)
        - Total de clases por estado
        """
        super().mostrar_resumen()

        # Estadísticas de miembros
        total_miembros = self.miembros.contar()
        miembros_activos = sum(1 for m in self.listar_miembros() if m.membresia_activa)

        # Estadísticas de entrenadores
        total_entrenadores = self.entrenadores.contar()
        entrenadores_disponibles = sum(1 for e in self.listar_entrenadores() if e.disponible)

        # Estadísticas de clases
        clases = self.listar_clases()
        clases_programadas = sum(1 for c in clases if c.estado == "programada")
        clases_completadas = sum(1 for c in clases if c.estado == "completada")
        clases_canceladas = sum(1 for c in clases if c.estado == "cancelada")

        print(f"   👥 Miembros: {total_miembros} (Activos: {miembros_activos})")
        print(f"   👨‍🏫 Entrenadores: {total_entrenadores} (Disponibles: {entrenadores_disponibles})")
        print(f"   📚 Clases Totales: {len(clases)}")
        print(f"      • Programadas: {clases_programadas}")
        print(f"      • Completadas: {clases_completadas}")
        print(f"      • Canceladas: {clases_canceladas}")
        print(f"{'='*60}\n")

    def obtener_clases_de_miembro(self, miembro_id: int) -> List[Clase]:
        """
        Obtiene todas las clases en las que está inscrito un miembro.

        Args:
            miembro_id: ID del miembro

        Returns:
            Lista de clases del miembro
        """
        return [c for c in self.listar_clases() if c.miembro_id == miembro_id]

    def obtener_clases_de_entrenador(self, entrenador_id: int) -> List[Clase]:
        """
        Obtiene todas las clases que imparte un entrenador.

        Args:
            entrenador_id: ID del entrenador

        Returns:
            Lista de clases del entrenador
        """
        return [c for c in self.listar_clases() if c.entrenador_id == entrenador_id]

    def mostrar_clases_con_detalles(self) -> None:
        """
        Muestra todas las clases con información detallada de miembros y entrenadores.

        Esta función demuestra cómo usar las RELACIONES entre entidades.
        """
        print("\n" + "="*80)
        print("📚 LISTADO DE CLASES CON DETALLES")
        print("="*80)

        clases = self.listar_clases()
        if not clases:
            print("No hay clases registradas.")
            return

        for clase in clases:
            # Obtener información del entrenador (usando la relación)
            entrenador = self.buscar_entrenador(clase.entrenador_id)
            nombre_entrenador = entrenador.nombre if entrenador else "Desconocido"

            # Obtener información del miembro (usando la relación)
            miembro = self.buscar_miembro(clase.miembro_id)
            nombre_miembro = miembro.nombre if miembro else "Desconocido"

            # Mostrar información completa
            print(f"\n🎯 {clase.nombre_clase} (ID: {clase.id})")
            print(f"   👨‍🏫 Entrenador: {nombre_entrenador}")
            print(f"   👤 Miembro: {nombre_miembro}")
            print(f"   📅 Fecha: {clase.fecha} | ⏰ Hora: {clase.hora}")
            print(f"   ⏱️ Duración: {clase.duracion_minutos} minutos")
            print(f"   🏛️ Salón: {clase.salon}")
            print(f"   📊 Estado: {clase.estado.upper()}")

        print("="*80)


# ═══════════════════════════════════════════════════════════════════
#                  🚀 PASO 6: FUNCIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════════

def main():
    """
    Función principal que demuestra todas las capacidades del sistema.

    Realiza las siguientes operaciones:
    1. Crea el sistema de gimnasio
    2. Registra miembros de ejemplo
    3. Registra entrenadores de ejemplo
    4. Programa clases (relacionando miembros con entrenadores)
    5. Realiza operaciones sobre las clases
    6. Muestra reportes y consultas
    7. Demuestra que todo se guarda en JSON
    """

    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              💪 SISTEMA DE GESTIÓN DE GIMNASIO              ║
║                                                              ║
║  Gestiona miembros, entrenadores y clases de entrenamiento  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    # Crear el sistema
    sistema = SistemaGimnasio()

    # ══════════════════════════════════════════════════════════════
    # PASO 6.1 - Agregar MIEMBROS de ejemplo
    # ══════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("📥 PASO 1: Registrando miembros del gimnasio...")
    print("="*60)

    miembro1 = Miembro(
        id=1,
        nombre="Carlos Rodríguez",
        edad=28,
        email="carlos.r@email.com",
        telefono="6789-1234",
        membresia_activa=True,
        fecha_registro="2025-01-15"
    )
    sistema.agregar_miembro(miembro1)

    miembro2 = Miembro(
        id=2,
        nombre="Ana María González",
        edad=35,
        email="ana.gonzalez@email.com",
        telefono="6789-5678",
        membresia_activa=True,
        fecha_registro="2025-01-20"
    )
    sistema.agregar_miembro(miembro2)

    miembro3 = Miembro(
        id=3,
        nombre="Luis Fernando Pérez",
        edad=42,
        email="luis.perez@email.com",
        telefono="6789-9012",
        membresia_activa=True,
        fecha_registro="2025-02-01"
    )
    sistema.agregar_miembro(miembro3)

    miembro4 = Miembro(
        id=4,
        nombre="María José Castro",
        edad=25,
        email="maria.castro@email.com",
        telefono="6789-3456",
        membresia_activa=False,  # Esta persona no tiene membresía activa
        fecha_registro="2024-12-10"
    )
    sistema.agregar_miembro(miembro4)

    # ══════════════════════════════════════════════════════════════
    # PASO 6.2 - Agregar ENTRENADORES de ejemplo
    # ══════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("📥 PASO 2: Registrando entrenadores...")
    print("="*60)

    entrenador1 = Entrenador(
        id=1,
        nombre="Roberto Martínez",
        especialidad="CrossFit",
        años_experiencia=8,
        certificaciones="CrossFit Level 2, Nutrición Deportiva",
        email="roberto.m@gym.com",
        disponible=True
    )
    sistema.agregar_entrenador(entrenador1)

    entrenador2 = Entrenador(
        id=2,
        nombre="Patricia Hernández",
        especialidad="Yoga",
        años_experiencia=5,
        certificaciones="Yoga Alliance RYT-500, Meditación",
        email="patricia.h@gym.com",
        disponible=True
    )
    sistema.agregar_entrenador(entrenador2)

    entrenador3 = Entrenador(
        id=3,
        nombre="Miguel Ángel Torres",
        especialidad="Spinning",
        años_experiencia=3,
        certificaciones="Spinning Instructor, Primeros Auxilios",
        email="miguel.t@gym.com",
        disponible=False  # Este entrenador no está disponible actualmente
    )
    sistema.agregar_entrenador(entrenador3)

    entrenador4 = Entrenador(
        id=4,
        nombre="Laura Sánchez",
        especialidad="Pilates",
        años_experiencia=6,
        certificaciones="Pilates Mat & Reformer, Fisioterapia",
        email="laura.s@gym.com",
        disponible=True
    )
    sistema.agregar_entrenador(entrenador4)

    # ══════════════════════════════════════════════════════════════
    # PASO 6.3 - PROGRAMAR CLASES (¡Aquí relacionamos las entidades!)
    # ══════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("🔄 PASO 3: Programando clases (relacionando miembros con entrenadores)...")
    print("="*60)

    # Clase 1: Carlos con Roberto (CrossFit)
    sistema.programar_clase(
        nombre_clase="CrossFit Intenso",
        entrenador_id=1,  # Roberto Martínez
        miembro_id=1,     # Carlos Rodríguez
        fecha="2025-12-05",
        hora="06:00",
        duracion_minutos=60,
        salon="Sala A"
    )

    # Clase 2: Ana María con Patricia (Yoga)
    sistema.programar_clase(
        nombre_clase="Yoga Matutino",
        entrenador_id=2,  # Patricia Hernández
        miembro_id=2,     # Ana María González
        fecha="2025-12-05",
        hora="07:30",
        duracion_minutos=90,
        salon="Sala Zen"
    )

    # Clase 3: Luis con Laura (Pilates)
    sistema.programar_clase(
        nombre_clase="Pilates Terapéutico",
        entrenador_id=4,  # Laura Sánchez
        miembro_id=3,     # Luis Fernando Pérez
        fecha="2025-12-06",
        hora="18:00",
        duracion_minutos=60,
        salon="Sala B"
    )

    # Clase 4: Carlos con Patricia (Yoga) - Mismo miembro, diferente entrenador
    sistema.programar_clase(
        nombre_clase="Yoga para Atletas",
        entrenador_id=2,  # Patricia Hernández
        miembro_id=1,     # Carlos Rodríguez
        fecha="2025-12-07",
        hora="08:00",
        duracion_minutos=75,
        salon="Sala Zen"
    )

    # Intentar programar con entrenador no disponible (debe fallar)
    print("\n🧪 Prueba: Intentando programar con entrenador no disponible...")
    sistema.programar_clase(
        nombre_clase="Spinning Extremo",
        entrenador_id=3,  # Miguel Ángel Torres (no disponible)
        miembro_id=2,
        fecha="2025-12-08",
        hora="19:00",
        duracion_minutos=45,
        salon="Sala Spinning"
    )

    # Intentar programar con miembro sin membresía activa (debe fallar)
    print("\n🧪 Prueba: Intentando programar con miembro sin membresía activa...")
    sistema.programar_clase(
        nombre_clase="CrossFit Principiantes",
        entrenador_id=1,
        miembro_id=4,  # María José Castro (sin membresía activa)
        fecha="2025-12-09",
        hora="17:00",
        duracion_minutos=60,
        salon="Sala A"
    )

    # ══════════════════════════════════════════════════════════════
    # PASO 6.4 - OPERACIONES SOBRE LAS CLASES
    # ══════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("🔄 PASO 4: Realizando operaciones sobre clases...")
    print("="*60)

    # Completar una clase
    print("\n📝 Completando clase...")
    sistema.completar_clase(1)  # Completar la clase de CrossFit

    # Cancelar una clase
    print("\n📝 Cancelando clase...")
    sistema.cancelar_clase(3)  # Cancelar la clase de Pilates

    # Activar membresía del miembro 4
    print("\n📝 Activando membresía...")
    sistema.activar_membresia(4)

    # Ahora sí podemos programarle una clase
    print("\n📝 Intentando programar nuevamente con membresía activa...")
    sistema.programar_clase(
        nombre_clase="CrossFit Principiantes",
        entrenador_id=1,
        miembro_id=4,
        fecha="2025-12-10",
        hora="17:00",
        duracion_minutos=60,
        salon="Sala A"
    )

    # ══════════════════════════════════════════════════════════════
    # PASO 6.5 - MOSTRAR REPORTES Y CONSULTAS
    # ══════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("📊 PASO 5: Generando reportes...")
    print("="*60)

    # Mostrar resumen del sistema
    print("\n")
    sistema.mostrar_resumen()

    # Listar todos los miembros
    print("\n" + "="*60)
    print("👥 LISTADO DE MIEMBROS")
    print("="*60)
    mostrar_tabla(sistema.listar_miembros(), "Miembros del Gimnasio")

    # Listar todos los entrenadores
    print("\n" + "="*60)
    print("👨‍🏫 LISTADO DE ENTRENADORES")
    print("="*60)
    mostrar_tabla(sistema.listar_entrenadores(), "Entrenadores del Gimnasio")

    # Listar entrenadores disponibles
    print("\n" + "="*60)
    print("✅ ENTRENADORES DISPONIBLES")
    print("="*60)
    entrenadores_disponibles = sistema.listar_entrenadores_disponibles()
    if entrenadores_disponibles:
        mostrar_tabla(entrenadores_disponibles, "Entrenadores Disponibles")
    else:
        print("No hay entrenadores disponibles actualmente.")

    # Mostrar clases con todos los detalles
    sistema.mostrar_clases_con_detalles()

    # Consultas específicas
    print("\n" + "="*60)
    print("🔍 CONSULTAS ESPECÍFICAS")
    print("="*60)

    # Clases de un miembro específico
    print("\n📚 Clases de Carlos Rodríguez (ID: 1):")
    clases_carlos = sistema.obtener_clases_de_miembro(1)
    if clases_carlos:
        for clase in clases_carlos:
            print(f"   • {clase.nombre_clase} - {clase.fecha} a las {clase.hora} (Estado: {clase.estado})")
    else:
        print("   No tiene clases registradas.")

    # Clases de un entrenador específico
    print("\n📚 Clases de Patricia Hernández (ID: 2):")
    clases_patricia = sistema.obtener_clases_de_entrenador(2)
    if clases_patricia:
        for clase in clases_patricia:
            miembro = sistema.buscar_miembro(clase.miembro_id)
            nombre_miembro = miembro.nombre if miembro else "Desconocido"
            print(f"   • {clase.nombre_clase} con {nombre_miembro} - {clase.fecha} (Estado: {clase.estado})")
    else:
        print("   No tiene clases asignadas.")

    # ══════════════════════════════════════════════════════════════
    # PASO 6.6 - MOSTRAR BITÁCORAS Y ESTADÍSTICAS
    # ══════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("📋 PASO 6: Bitácoras y estadísticas del sistema")
    print("="*60)

    # Mostrar bitácora de miembros
    print("\n📝 Bitácora de operaciones - MIEMBROS:")
    sistema.miembros.mostrar_bitacora()

    # Mostrar bitácora de clases
    print("\n📝 Bitácora de operaciones - CLASES:")
    sistema.clases.mostrar_bitacora()

    # Mostrar estadísticas de miembros
    print("\n📊 Estadísticas del repositorio - MIEMBROS:")
    sistema.miembros.mostrar_estadisticas()

    # Mostrar estadísticas de entrenadores
    print("\n📊 Estadísticas del repositorio - ENTRENADORES:")
    sistema.entrenadores.mostrar_estadisticas()

    # Mostrar estadísticas de clases
    print("\n📊 Estadísticas del repositorio - CLASES:")
    sistema.clases.mostrar_estadisticas()

    # ══════════════════════════════════════════════════════════════
    # FINALIZACIÓN
    # ══════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("✅ ¡PROGRAMA COMPLETADO EXITOSAMENTE!")
    print("="*60)
    print("""
📁 ARCHIVOS JSON GENERADOS:

Los siguientes archivos fueron creados en la carpeta 'datos/gimnasio/':

   • miembros.json       - Contiene todos los miembros registrados
   • entrenadores.json   - Contiene todos los entrenadores
   • clases.json         - Contiene todas las clases programadas

Puedes abrir estos archivos con cualquier editor de texto para ver
los datos en formato JSON.

🔗 RELACIONES DEMOSTRADAS:

   • Las clases relacionan miembros con entrenadores mediante IDs
   • Se validó que solo miembros activos pueden tomar clases
   • Se validó que solo entrenadores disponibles pueden impartir clases
   • Se demostró cómo consultar datos relacionados

💡 OPERACIONES CRUD IMPLEMENTADAS:

   ✅ CREATE - Agregar miembros, entrenadores y clases
   ✅ READ   - Listar y buscar entidades
   ✅ UPDATE - Cambiar estado de membresías y clases
   ✅ DELETE - (No implementado pero el framework lo soporta)
    """)


# ═══════════════════════════════════════════════════════════════════
#                          PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main()


# ═══════════════════════════════════════════════════════════════════
#                       ✅ CHECKLIST COMPLETADO
# ═══════════════════════════════════════════════════════════════════
#
# ✅ Definidas 3 entidades diferentes y coherentes (Miembro, Entrenador, Clase)
# ✅ Cada entidad tiene más de 4 campos (incluyendo id)
# ✅ Implementadas validaciones en todas las entidades
# ✅ Creados repositorios para las 3 entidades
# ✅ Implementados métodos para agregar cada tipo de entidad
# ✅ Implementados métodos para listar/buscar entidades
# ✅ Creado método programar_clase() que relaciona las entidades
# ✅ Agregados múltiples datos de ejemplo (4 de cada tipo)
# ✅ El programa se ejecuta sin errores
# ✅ Se crean archivos JSON en la carpeta datos/gimnasio/
# ✅ Los archivos JSON contienen datos válidos
# ✅ La bitácora registra las operaciones
# ✅ Código documentado con comentarios explicativos
# ✅ Nombres específicos (no genéricos) en todas las clases
# ✅ El sistema tiene lógica coherente y relaciones claras
# ✅ Demostradas operaciones de actualización (UPDATE)
# ✅ Demostradas validaciones de integridad referencial
# ✅ Incluidos reportes y consultas complejas
#
# ═══════════════════════════════════════════════════════════════════