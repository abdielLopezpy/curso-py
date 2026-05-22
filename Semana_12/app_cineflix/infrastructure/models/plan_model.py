from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import sqlite3

from application.entities.plan import Plan, PlanKind


@dataclass
class PlanModel:
    """Representa una fila de la tabla `plans`."""
    id: Optional[int]
    name: str
    kind: str
    price: float
    duration_days: int
    max_members: int
    is_public: int
    is_active: int
    created_at: Optional[str]

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "PlanModel":
        return cls(
            id=row["id"],
            name=row["name"],
            kind=row["kind"],
            price=row["price"],
            duration_days=row["duration_days"],
            max_members=row["max_members"],
            is_public=row["is_public"],
            is_active=row["is_active"],
            created_at=row["created_at"],
        )

    def to_entity(self) -> Plan:
        return Plan(
            id=self.id,
            name=self.name,
            kind=PlanKind(self.kind),
            price=self.price,
            duration_days=self.duration_days,
            max_members=self.max_members,
            is_public=bool(self.is_public),
            is_active=bool(self.is_active),
            created_at=_parse_dt(self.created_at),
        )

    @classmethod
    def from_entity(cls, plan: Plan) -> "PlanModel":
        return cls(
            id=plan.id,
            name=plan.name,
            kind=plan.kind.value,
            price=plan.price,
            duration_days=plan.duration_days,
            max_members=plan.max_members,
            is_public=1 if plan.is_public else 0,
            is_active=1 if plan.is_active else 0,
            created_at=plan.created_at.isoformat() if plan.created_at else None,
        )


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace(" ", "T"))
