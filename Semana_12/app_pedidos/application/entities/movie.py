from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Movie:
    id: Optional[int]
    title: str
    url: str
    age_rating: int = 0
    created_at: Optional[datetime] = None
