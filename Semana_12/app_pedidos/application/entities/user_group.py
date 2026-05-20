from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from application.exceptions import ValidationError


@dataclass
class UserGroup:
    id: Optional[int]
    name: str
    owner_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("El nombre del grupo no puede estar vacio")
        self.name = self.name.strip()

        if self.owner_id <= 0:
            raise ValidationError("owner_id debe ser positivo")
