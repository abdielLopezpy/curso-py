# ============================================================================
# Excepciones de DOMINIO
# ============================================================================
# Reglas:
#  - Son puras: no dependen de FastAPI, HTTP ni SQLite.
#  - Las capas de afuera (interfaces) las traducen a HTTP (404, 409, etc.).
#  - Heredan de DomainError para poder atraparlas todas juntas.
# ============================================================================


class DomainError(Exception):
    """Clase base para errores de dominio."""


class EntidadNoEncontrada(DomainError):
    """El recurso solicitado no existe."""


class EntidadDuplicada(DomainError):
    """Se intento crear un recurso que viola una restriccion UNIQUE."""


class ReglaDeNegocioViolada(DomainError):
    """Una regla de negocio no se cumple (ej: libro no disponible)."""
