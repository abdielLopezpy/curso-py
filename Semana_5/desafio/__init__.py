#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    PAQUETE: SISTEMA DE GIMNASIO                     ║
║                                                                      ║
║  Sistema de gestión completo para un gimnasio que maneja:           ║
║  - Miembros y sus membresías                                         ║
║  - Entrenadores y su disponibilidad                                  ║
║  - Clases que relacionan miembros con entrenadores                   ║
║                                                                      ║
║  Todos los datos se persisten en archivos JSON.                     ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""

from .models import Miembro, Entrenador, Clase, Suscripcion
from .sistema_gimnasio import SistemaGimnasio

__all__ = [
    'Miembro',
    'Entrenador',
    'Clase',
    'Suscripcion',
    'SistemaGimnasio',
]

__version__ = '1.0.0'
__author__ = 'Desafío Semana 5'
