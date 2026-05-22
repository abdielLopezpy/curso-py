from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserGroup:
    id: Optional[int]
    name: str
    owner_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
