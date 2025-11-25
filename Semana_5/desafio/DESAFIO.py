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
║  REQUISITOS:                                                         ║
║  ✅ Definir 3 entidades (clases) relacionadas entre sí              ║
║  ✅ Crear un sistema de gestión que las maneje                      ║
║  ✅ Implementar operaciones CRUD para cada entidad                  ║
║  ✅ Realizar operaciones que relacionen las entidades               ║
║  ✅ Demostrar que los datos se guardan en JSON correctamente        ║
║                                                                      ║
║  EJEMPLOS DE SISTEMAS QUE PUEDES CREAR:                             ║
║                                                                      ║
║  🏥 Sistema Hospitalario:                                           ║
║     • Doctores, Pacientes, Citas                                    ║
║                                                                      ║
║  📚 Sistema Bibliotecario:                                          ║
║     • Libros, Autores, Préstamos                                    ║
║                                                                      ║
║  🎓 Sistema Educativo:                                              ║
║     • Estudiantes, Profesores, Cursos                               ║
║                                                                      ║
║  🍕 Sistema de Restaurante:                                         ║
║     • Platillos, Ingredientes, Pedidos                              ║
║                                                                      ║
║  🏨 Sistema Hotelero:                                               ║
║     • Habitaciones, Huéspedes, Reservaciones                        ║
║                                                                      ║
║  🚗 Sistema de Renta de Autos:                                      ║
║     • Vehículos, Clientes, Rentas                                   ║
║                                                                      ║
║  💪 Sistema de Gimnasio:                                            ║
║     • Miembros, Entrenadores, Clases                                ║
║                                                                      ║
║  🎮 Sistema de Videojuegos:                                         ║
║     • Jugadores, Partidas, Logros                                   ║
║                                                                      ║
║  ¡Elige el que más te guste o inventa el tuyo!                      ║
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
#                    🏗️ PASO 1: DEFINIR TUS ENTIDADES
# ═══════════════════════════════════════════════════════════════════

# TODO: Define tu PRIMERA entidad aquí
# Ejemplo: Si haces un sistema de biblioteca, podría ser "Libro"
#
# @dataclass
# class MiPrimeraEntidad(Entidad):
#     """Descripción de tu entidad."""
#     id: int
#     # ... más campos ...
#
#     def obtener_id(self) -> int:
#         return self.id
#
#     @classmethod
#     def desde_diccionario(cls, datos: Dict[str, Any]) -> MiPrimeraEntidad:
#         return cls(**datos)
#
#     def validar(self) -> bool:
#         """Valida que los datos sean correctos."""
#         # TODO: Agregar validaciones
#         return True

@dataclass
class MiPrimeraEntidad(Entidad):
    """
    TODO: Cambia el nombre de esta clase y agrega una descripción.

    TODO: Define los campos que necesita tu entidad.
    Recuerda que DEBE tener un campo 'id'.

    Ejemplo:
        id: int
        nombre: str
        descripcion: str
    """
    id: int
    # TODO: Agrega más campos aquí

    def obtener_id(self) -> int:
        return self.id

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> MiPrimeraEntidad:
        return cls(**datos)

    def validar(self) -> bool:
        """
        TODO: Implementa validaciones para tu entidad.

        Puedes usar las funciones de ayuda:
        - validar_no_vacio(valor, "nombre_campo")
        - validar_positivo(valor, "nombre_campo")
        - validar_rango(valor, minimo, maximo, "nombre_campo")

        Retorna True si todo es válido, False si hay errores.
        """
        # TODO: Agrega validaciones aquí
        return True


# TODO: Define tu SEGUNDA entidad aquí
@dataclass
class MiSegundaEntidad(Entidad):
    """
    TODO: Cambia el nombre de esta clase y agrega una descripción.
    Esta entidad debería estar relacionada con la primera.

    Ejemplo: Si la primera es "Libro", esta podría ser "Autor"
    """
    id: int
    # TODO: Agrega más campos aquí

    def obtener_id(self) -> int:
        return self.id

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> MiSegundaEntidad:
        return cls(**datos)

    def validar(self) -> bool:
        """TODO: Implementa validaciones."""
        return True


# TODO: Define tu TERCERA entidad aquí
@dataclass
class MiTerceraEntidad(Entidad):
    """
    TODO: Cambia el nombre de esta clase y agrega una descripción.
    Esta entidad debería relacionar las dos anteriores.

    Ejemplo: Si tienes "Libro" y "Autor", esta podría ser "Prestamo"
    que relaciona libros con usuarios.

    IMPORTANTE: Esta entidad debe tener campos que referencien
    los IDs de las otras dos entidades.

    Ejemplo:
        id: int
        libro_id: int  # <-- Referencia a la primera entidad
        usuario_id: int  # <-- Referencia a alguna entidad
        fecha: str
    """
    id: int
    # TODO: Agrega campos aquí, incluyendo referencias a otras entidades

    def obtener_id(self) -> int:
        return self.id

    @classmethod
    def desde_diccionario(cls, datos: Dict[str, Any]) -> MiTerceraEntidad:
        return cls(**datos)


# ═══════════════════════════════════════════════════════════════════
#              🎮 PASO 2: CREAR TU SISTEMA DE GESTIÓN
# ═══════════════════════════════════════════════════════════════════

class MiSistema(SistemaGestion):
    """
    TODO: Cambia el nombre de esta clase según tu sistema.

    Ejemplo: "SistemaBiblioteca", "SistemaHospital", etc.

    Esta clase debe:
    1. Crear repositorios para cada una de tus entidades
    2. Implementar métodos para operaciones comunes
    3. Implementar métodos que relacionen las entidades
    """

    def __init__(self):
        # TODO: Cambia "mi_sistema" por el nombre de tu sistema
        super().__init__("mi_sistema")

        # TODO: Crea repositorios para cada entidad
        # Ejemplo:
        # self.libros = RepositorioJSON("libros", Libro, self.directorio_datos)
        # self.autores = RepositorioJSON("autores", Autor, self.directorio_datos)
        # self.prestamos = RepositorioJSON("prestamos", Prestamo, self.directorio_datos)

        # TODO: Crea tus tres repositorios aquí
        self.repo1 = RepositorioJSON(
            "nombre_coleccion_1",  # TODO: Cambia esto
            MiPrimeraEntidad,       # TODO: Cambia esto por tu entidad
            self.directorio_datos
        )

        self.repo2 = RepositorioJSON(
            "nombre_coleccion_2",  # TODO: Cambia esto
            MiSegundaEntidad,       # TODO: Cambia esto por tu entidad
            self.directorio_datos
        )

        self.repo3 = RepositorioJSON(
            "nombre_coleccion_3",  # TODO: Cambia esto
            MiTerceraEntidad,       # TODO: Cambia esto por tu entidad
            self.directorio_datos
        )

    # ══════════════════════════════════════════════════════════════
    #        📝 PASO 3: IMPLEMENTAR OPERACIONES BÁSICAS
    # ══════════════════════════════════════════════════════════════

    # TODO: Implementa métodos para agregar entidades
    # Ejemplo:
    #
    # def agregar_libro(self, libro: Libro) -> bool:
    #     """Agrega un nuevo libro al sistema."""
    #     if not libro.validar():
    #         return False
    #     return self.libros.insertar(libro)

    def agregar_primera_entidad(self, entidad: MiPrimeraEntidad) -> bool:
        """
        TODO: Cambia el nombre del método y los parámetros.
        Agrega una instancia de tu primera entidad al sistema.
        """
        # TODO: Valida la entidad y agrégala al repositorio
        if not entidad.validar():
            return False
        return self.repo1.insertar(entidad)

    def agregar_segunda_entidad(self, entidad: MiSegundaEntidad) -> bool:
        """TODO: Implementa este método."""
        # TODO: Valida y agrega la entidad
        if not entidad.validar():
            return False
        return self.repo2.insertar(entidad)

    # TODO: Implementa métodos para listar entidades
    def listar_primera_entidad(self) -> List[MiPrimeraEntidad]:
        """TODO: Implementa este método."""
        return self.repo1.consultar_todos()

    def listar_segunda_entidad(self) -> List[MiSegundaEntidad]:
        """TODO: Implementa este método."""
        return self.repo2.consultar_todos()

    # TODO: Implementa métodos para buscar por ID
    def buscar_primera_entidad(self, id: int) -> MiPrimeraEntidad | None:
        """TODO: Implementa este método."""
        return self.repo1.consultar_por_id(id)

    # ══════════════════════════════════════════════════════════════
    #    🔗 PASO 4: IMPLEMENTAR OPERACIONES QUE RELACIONEN ENTIDADES
    # ══════════════════════════════════════════════════════════════

    # TODO: Implementa un método que relacione tus entidades
    #
    # Ejemplo para biblioteca:
    # def prestar_libro(self, libro_id: int, usuario_id: int) -> bool:
    #     """Registra el préstamo de un libro."""
    #     # 1. Verificar que el libro existe
    #     libro = self.buscar_libro(libro_id)
    #     if libro is None:
    #         print("❌ Libro no encontrado")
    #         return False
    #
    #     # 2. Verificar que está disponible
    #     if not libro.disponible:
    #         print("❌ Libro no disponible")
    #         return False
    #
    #     # 3. Crear el préstamo
    #     prestamo = Prestamo(...)
    #     self.prestamos.insertar(prestamo)
    #
    #     # 4. Actualizar el libro
    #     libro.disponible = False
    #     self.libros.actualizar(libro)
    #
    #     return True

    def operacion_relacionada(self, id1: int, id2: int) -> bool:
        """
        TODO: Implementa un método que relacione tus entidades.

        Este método debe:
        1. Verificar que las entidades relacionadas existan
        2. Realizar validaciones necesarias
        3. Crear una instancia de tu tercera entidad (la relación)
        4. Actualizar el estado de las entidades si es necesario
        5. Guardar todo en los repositorios

        Retorna True si la operación fue exitosa.
        """
        # TODO: Implementa la lógica aquí

        # Ejemplo de estructura:
        # 1. Buscar primera entidad
        # entidad1 = self.repo1.consultar_por_id(id1)
        # if entidad1 is None:
        #     print("❌ Primera entidad no encontrada")
        #     return False

        # 2. Buscar segunda entidad
        # ...

        # 3. Validar condiciones
        # ...

        # 4. Crear la relación (tercera entidad)
        # ...

        # 5. Guardar y actualizar
        # ...

        return False  # TODO: Cambia esto

    # ══════════════════════════════════════════════════════════════
    #              📊 PASO 5: IMPLEMENTAR REPORTES
    # ══════════════════════════════════════════════════════════════

    def mostrar_resumen(self) -> None:
        """
        TODO: Muestra un resumen del sistema.

        Debe mostrar:
        - Cantidad de cada tipo de entidad
        - Estadísticas relevantes
        - Cualquier información útil
        """
        super().mostrar_resumen()

        # TODO: Agrega estadísticas de tu sistema
        total_entidad1 = self.repo1.contar()
        total_entidad2 = self.repo2.contar()
        total_entidad3 = self.repo3.contar()

        print(f"   TODO: Nombre entidad 1: {total_entidad1}")
        print(f"   TODO: Nombre entidad 2: {total_entidad2}")
        print(f"   TODO: Nombre entidad 3: {total_entidad3}")
        print(f"{'='*60}\n")

    # TODO: Implementa otros métodos útiles
    # Ejemplos:
    # - Buscar por campo específico
    # - Generar reportes
    # - Calcular estadísticas
    # - Filtrar por condiciones
    # - Actualizar entidades
    # - Eliminar entidades


# ═══════════════════════════════════════════════════════════════════
#                  🚀 PASO 6: FUNCIÓN PRINCIPAL
# ═══════════════════════════════════════════════════════════════════

def main():
    """
    TODO: Implementa la función principal que demuestre tu sistema.

    Debe:
    1. Crear el sistema
    2. Agregar datos de ejemplo (al menos 3 de cada entidad)
    3. Realizar operaciones que relacionen las entidades
    4. Mostrar consultas y reportes
    5. Demostrar que todo se guarda en JSON
    """

    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║              🎯 MI SISTEMA DE GESTIÓN                       ║
║                  TODO: Cambia este título                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)

    # TODO: Crea tu sistema
    sistema = MiSistema()

    # ══════════════════════════════════════════════════════════════
    # TODO: PASO 6.1 - Agregar datos de ejemplo
    # ══════════════════════════════════════════════════════════════
    print("\n📥 Agregando datos de ejemplo...")

    # TODO: Crea y agrega instancias de tu primera entidad
    # Ejemplo:
    # entidad1_1 = MiPrimeraEntidad(1, "Dato 1", ...)
    # sistema.agregar_primera_entidad(entidad1_1)

    # TODO: Crea y agrega al menos 3 instancias de cada entidad

    # ══════════════════════════════════════════════════════════════
    # TODO: PASO 6.2 - Realizar operaciones
    # ══════════════════════════════════════════════════════════════
    print("\n🔄 Realizando operaciones...")

    # TODO: Realiza operaciones que relacionen tus entidades
    # Ejemplo:
    # sistema.operacion_relacionada(1, 1)

    # ══════════════════════════════════════════════════════════════
    # TODO: PASO 6.3 - Mostrar reportes y consultas
    # ══════════════════════════════════════════════════════════════

    # TODO: Muestra el resumen del sistema
    # sistema.mostrar_resumen()

    # TODO: Lista todas las entidades
    # mostrar_tabla(sistema.listar_primera_entidad(), "Mi Primera Entidad")

    # TODO: Realiza búsquedas y filtros

    # TODO: Muestra las bitácoras
    # sistema.repo1.mostrar_bitacora()

    # TODO: Muestra estadísticas
    # sistema.repo1.mostrar_estadisticas()

    print("\n✅ ¡Programa completado!")
    print("📁 Revisa la carpeta 'datos/mi_sistema' para ver los archivos JSON")


# ═══════════════════════════════════════════════════════════════════
#                          PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # TODO: Antes de ejecutar, asegúrate de haber:
    # ✅ Definido tus 3 entidades
    # ✅ Creado tu sistema de gestión
    # ✅ Implementado los métodos necesarios
    # ✅ Agregado datos de ejemplo en main()

    main()


# ═══════════════════════════════════════════════════════════════════
#                       📝 CHECKLIST FINAL
# ═══════════════════════════════════════════════════════════════════
#
# Antes de entregar tu desafío, verifica que:
#
# ✅ Definiste 3 entidades diferentes y coherentes
# ✅ Cada entidad tiene al menos 4 campos (incluyendo id)
# ✅ Implementaste validaciones en tus entidades
# ✅ Creaste repositorios para las 3 entidades
# ✅ Implementaste métodos para agregar cada tipo de entidad
# ✅ Implementaste métodos para listar/buscar entidades
# ✅ Creaste al menos UN método que relacione las entidades
# ✅ Agregaste datos de ejemplo (mínimo 3 de cada tipo)
# ✅ El programa se ejecuta sin errores
# ✅ Se crean archivos JSON en la carpeta datos/
# ✅ Los archivos JSON tienen datos válidos
# ✅ La bitácora registra las operaciones
# ✅ Agregaste comentarios explicando tu código
# ✅ Cambiaste todos los nombres genéricos por nombres específicos
# ✅ El sistema tiene sentido y las entidades están relacionadas
#
# ═══════════════════════════════════════════════════════════════════
