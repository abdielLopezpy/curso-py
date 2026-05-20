"""Excepciones de dominio.

Se lanzan cuando las entidades reciben datos invalidos o cuando una regla
de negocio se rompe. Son agnosticas de la capa tecnica (no saben de HTTP
ni de SQL); las capas externas las traducen a su formato (404, mensaje, etc.).
"""


class DomainError(Exception):
    """Raiz de todas las excepciones de dominio."""


class ValidationError(DomainError):
    """Datos invalidos al construir o mutar una entidad."""


class BusinessRuleError(DomainError):
    """Se viola una regla de negocio (estado valido pero operacion no permitida)."""


class NotFoundError(DomainError):
    """No existe la entidad solicitada."""


class DuplicatedError(DomainError):
    """Conflicto de unicidad (email ya registrado, etc.)."""
