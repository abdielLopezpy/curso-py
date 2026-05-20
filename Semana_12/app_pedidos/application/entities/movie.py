from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

from application.exceptions import ValidationError


MAX_AGE_RATING = 21


@dataclass
class Movie:
    id: Optional[int]
    title: str
    url: str
    age_rating: int = 0
    created_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not self.title or not self.title.strip():
            raise ValidationError("El titulo no puede estar vacio")
        self.title = self.title.strip()

        parsed = urlparse(self.url or "")
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise ValidationError(f"URL invalida: {self.url!r}")

        if not (0 <= self.age_rating <= MAX_AGE_RATING):
            raise ValidationError(
                f"age_rating fuera de rango [0, {MAX_AGE_RATING}]: {self.age_rating}"
            )

    def is_suitable_for(self, age: int) -> bool:
        return age >= self.age_rating
