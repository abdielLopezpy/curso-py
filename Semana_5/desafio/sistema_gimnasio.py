#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    SISTEMA DE GESTIÓN DE GIMNASIO                   ║
║                                                                      ║
║  Implementa toda la lógica de negocio para gestionar:               ║
║  - Miembros y sus membresías                                         ║
║  - Entrenadores y su disponibilidad                                  ║
║  - Clases y relaciones entre miembros y entrenadores                 ║
║  - Reportes y consultas                                              ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

from pathlib import Path
from typing import List
import sys

# Agregar la carpeta framework al path para poder importar
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

from database_framework import (
    RepositorioJSON,
    SistemaGestion,
    mostrar_tabla
)

from models import Miembro, Entrenador, Clase


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
    #              OPERACIONES BÁSICAS - MIEMBROS
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
    #              OPERACIONES BÁSICAS - ENTRENADORES
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
    #      OPERACIONES QUE RELACIONAN ENTIDADES - CLASES
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
    #                    REPORTES Y CONSULTAS
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
