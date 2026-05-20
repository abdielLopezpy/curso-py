from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from application.exceptions import BusinessRuleError, ValidationError


MAX_MOVIES_PER_CATALOG = 500


@dataclass
class Catalog:
    id: Optional[int]
    name: str
    owner_id: int
    is_public: bool = False
    created_at: Optional[datetime] = None
    movie_ids: List[int] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("El nombre del catalogo no puede estar vacio")
        self.name = self.name.strip()

        if self.owner_id <= 0:
            raise ValidationError("owner_id debe ser positivo")

        if len(self.movie_ids) != len(set(self.movie_ids)):
            raise ValidationError("movie_ids no puede contener duplicados")
        if any(mid <= 0 for mid in self.movie_ids):
            raise ValidationError("movie_ids debe contener enteros positivos")

    def add_movie(self, movie_id: int) -> None:
        if movie_id <= 0:
            raise ValidationError("movie_id debe ser positivo")
        if movie_id in self.movie_ids:
            raise BusinessRuleError(f"La pelicula {movie_id} ya esta en el catalogo")
        if len(self.movie_ids) >= MAX_MOVIES_PER_CATALOG:
            raise BusinessRuleError(
                f"El catalogo alcanzo el limite de {MAX_MOVIES_PER_CATALOG} peliculas"
            )
        self.movie_ids.append(movie_id)

    def remove_movie(self, movie_id: int) -> None:
        if movie_id not in self.movie_ids:
            raise BusinessRuleError(f"La pelicula {movie_id} no esta en el catalogo")
        self.movie_ids.remove(movie_id)
