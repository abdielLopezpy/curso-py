from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class PlanKind(str, Enum):
    SINGLE = "single"
    DUO = "duo"
    KIDS = "kids"
    FAMILY = "family"


@dataclass
class Plan:
    id: Optional[int]
    name: str
    kind: PlanKind
    price: float
    duration_days: int
    max_members: int = 1
    is_public: bool = True
    is_active: bool = True
    created_at: Optional[datetime] = None
