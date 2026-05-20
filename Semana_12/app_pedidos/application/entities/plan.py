from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from application.exceptions import ValidationError


class PlanKind(str, Enum):
    SINGLE = "single"
    DUO = "duo"
    KIDS = "kids"
    FAMILY = "family"


# Maximo de miembros segun el tipo de plan (regla de negocio).
KIND_MAX_MEMBERS = {
    PlanKind.SINGLE: 1,
    PlanKind.DUO: 2,
    PlanKind.KIDS: 2,
    PlanKind.FAMILY: 5,
}


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

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("El nombre del plan no puede estar vacio")
        self.name = self.name.strip()

        if isinstance(self.kind, str):
            try:
                self.kind = PlanKind(self.kind)
            except ValueError as e:
                raise ValidationError(f"Tipo de plan invalido: {self.kind!r}") from e

        if self.price < 0:
            raise ValidationError("price no puede ser negativo")

        if self.duration_days <= 0:
            raise ValidationError("duration_days debe ser mayor a 0")

        if self.max_members <= 0:
            raise ValidationError("max_members debe ser mayor a 0")

        limit = KIND_MAX_MEMBERS[self.kind]
        if self.max_members > limit:
            raise ValidationError(
                f"max_members={self.max_members} excede el limite del plan "
                f"{self.kind.value} ({limit})"
            )
