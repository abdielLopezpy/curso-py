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
║  ✅ Entrenador - Profesionales que imparten clases                   ║
║  ✅ Clase - Sesiones de entrenamiento (relaciona Miembro-Entrenador)║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

from pathlib import Path
import sys

# Agregar la carpeta framework al path para poder importar
sys.path.insert(0, str(Path(__file__).parent.parent / "framework"))

from database_framework import mostrar_tabla
from models import Miembro, Entrenador
from sistema_gimnasio import SistemaGimnasio


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
    # PASO 1 - Agregar MIEMBROS de ejemplo
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
        fecha_registro="2025-01-15",
        cedula="1-123-456-7"
    )
    sistema.agregar_miembro(miembro1)

    miembro2 = Miembro(
        id=2,
        nombre="Ana María González",
        edad=35,
        email="ana.gonzalez@email.com",
        telefono="6789-5678",
        membresia_activa=True,
        fecha_registro="2025-01-20",
        cedula="2-234-567-8"
    )
    sistema.agregar_miembro(miembro2)

    miembro3 = Miembro(
        id=3,
        nombre="Luis Fernando Pérez",
        edad=42,
        email="luis.perez@email.com",
        telefono="6789-9012",
        membresia_activa=True,
        fecha_registro="2025-02-01",
        cedula="3-345-678-9"
    )
    sistema.agregar_miembro(miembro3)

    miembro4 = Miembro(
        id=4,
        nombre="María José Castro",
        edad=25,
        email="maria.castro@email.com",
        telefono="6789-3456",
        membresia_activa=False,  # Esta persona no tiene membresía activa
        fecha_registro="2024-12-10",
        cedula="4-456-789-0"
    )
    sistema.agregar_miembro(miembro4)

    # ══════════════════════════════════════════════════════════════
    # PASO 2 - Agregar ENTRENADORES de ejemplo
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
    # PASO 3 - PROGRAMAR CLASES (¡Aquí relacionamos las entidades!)
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
    # PASO 4 - OPERACIONES SOBRE LAS CLASES
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
    # PASO 5 - MOSTRAR REPORTES Y CONSULTAS
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
    # PASO 6 - MOSTRAR BITÁCORAS Y ESTADÍSTICAS
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

📦 ESTRUCTURA MODULAR:

   ✅ models.py - Definición de entidades
   ✅ sistema_gimnasio.py - Lógica de negocio
   ✅ main.py - Programa principal con ejemplos
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
# ✅ Código dividido en módulos para mejor organización
#
# ═══════════════════════════════════════════════════════════════════
