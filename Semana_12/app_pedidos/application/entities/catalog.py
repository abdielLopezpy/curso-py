from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Catalog:
    id: Optional[int]
    name: str
    owner_id: int
    is_public: bool = False
    created_at: Optional[datetime] = None
    movie_ids: List[int] = field(default_factory=list)
