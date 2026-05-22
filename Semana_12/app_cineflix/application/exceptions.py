# ============================================================================
# Excepciones de DOMINIO
# ============================================================================
# Reglas:
#   - Son puras: no dependen de FastAPI, HTTP ni SQLite.
#   - Las capas de afuera (interfaces) las traducen a HTTP (404, 409, etc.).
#   - Todas heredan de DomainError para poder atraparlas en bloque.
#
# Como usarlas:
#   - El use case lanza la excepcion semantica de negocio.
#   - El router la atrapa y la convierte en HTTPException con el codigo correcto.
# ============================================================================


class DomainError(Exception):
    """Clase base para errores de dominio."""


class EntidadNoEncontrada(DomainError):
    """El recurso solicitado no existe (HTTP 404)."""


class EntidadDuplicada(DomainError):
    """Se intento crear un recurso que viola una restriccion UNIQUE (HTTP 409)."""


class ReglaDeNegocioViolada(DomainError):
    """Una regla de negocio no se cumple (HTTP 422).

    Ejemplos en Cineflix:
      - Suscripcion expirada al intentar ver una pelicula.
      - Grupo lleno al agregar un miembro mas.
      - Pelicula con age_rating > edad del usuario kid.
    """
