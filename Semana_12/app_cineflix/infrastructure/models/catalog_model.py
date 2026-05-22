from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

import sqlite3

from application.entities.catalog import Catalog


@dataclass
class CatalogModel:
    """Representa una fila de la tabla `catalogs` (+ ids de peliculas opcional)."""
    id: Optional[int]
    name: str
    is_public: int
    owner_id: int
    created_at: Optional[str]
    movie_ids: List[int] = field(default_factory=list)

    @classmethod
    def from_row(cls, row: sqlite3.Row, movie_ids: Optional[List[int]] = None) -> "CatalogModel":
        return cls(
            id=row["id"],
            name=row["name"],
            is_public=row["is_public"],
            owner_id=row["owner_id"],
            created_at=row["created_at"],
            movie_ids=movie_ids or [],
        )

    def to_entity(self) -> Catalog:
        return Catalog(
            id=self.id,
            name=self.name,
            owner_id=self.owner_id,
            is_public=bool(self.is_public),
            created_at=_parse_dt(self.created_at),
            movie_ids=list(self.movie_ids),
        )

    @classmethod
    def from_entity(cls, catalog: Catalog) -> "CatalogModel":
        return cls(
            id=catalog.id,
            name=catalog.name,
            is_public=1 if catalog.is_public else 0,
            owner_id=catalog.owner_id,
            created_at=catalog.created_at.isoformat() if catalog.created_at else None,
            movie_ids=list(catalog.movie_ids),
        )


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace(" ", "T"))
