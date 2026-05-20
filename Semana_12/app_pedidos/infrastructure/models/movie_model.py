from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import sqlite3

from application.entities.movie import Movie


@dataclass
class MovieModel:
    """Representa una fila de la tabla `movies`."""
    id: Optional[int]
    title: str
    url: str
    age_rating: int
    created_at: Optional[str]

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "MovieModel":
        return cls(
            id=row["id"],
            title=row["title"],
            url=row["url"],
            age_rating=row["age_rating"],
            created_at=row["created_at"],
        )

    def to_entity(self) -> Movie:
        return Movie(
            id=self.id,
            title=self.title,
            url=self.url,
            age_rating=self.age_rating,
            created_at=_parse_dt(self.created_at),
        )

    @classmethod
    def from_entity(cls, movie: Movie) -> "MovieModel":
        return cls(
            id=movie.id,
            title=movie.title,
            url=movie.url,
            age_rating=movie.age_rating,
            created_at=movie.created_at.isoformat() if movie.created_at else None,
        )


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace(" ", "T"))
