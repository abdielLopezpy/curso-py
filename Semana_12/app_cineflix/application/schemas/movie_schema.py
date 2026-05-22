# ============================================================================
# SCHEMAS (Pydantic): Movie
# ============================================================================
# Son DTOs puros: validan/serializan datos de entrada y salida de la API.
# NO son entidades de dominio (esas viven en application/entities/movie.py).
#
#   MovieCreate -> body del POST /api/movies
#   MovieRead   -> respuesta del GET (incluye id + created_at)
#   MovieUpdate -> body del PUT (todos opcionales -> permite actualizacion parcial)
#
# Convencion: el schema valida tipos basicos; las reglas de negocio (ej:
# "age_rating no puede ser negativo") tambien pueden vivir aqui via validators
# de Pydantic, o en el use case si son mas complejas.
# ============================================================================

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MovieCreate(BaseModel):
    """Datos minimos para crear una pelicula."""
    title: str = Field(min_length=1, max_length=200)
    url: str = Field(min_length=1)
    age_rating: int = Field(default=0, ge=0, le=21)


class MovieRead(BaseModel):
    """Lo que el API devuelve al cliente."""
    id: int
    title: str
    url: str
    age_rating: int
    created_at: Optional[datetime] = None


class MovieUpdate(BaseModel):
    """Todos los campos opcionales -> actualizacion parcial."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    url: Optional[str] = Field(default=None, min_length=1)
    age_rating: Optional[int] = Field(default=None, ge=0, le=21)
