from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import sqlite3

from application.entities.subscription import Subscription


@dataclass
class SubscriptionModel:
    """Representa una fila de la tabla `subscriptions`."""
    id: Optional[int]
    group_id: int
    plan_id: int
    started_at: Optional[str]
    expires_at: str
    is_active: int

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "SubscriptionModel":
        return cls(
            id=row["id"],
            group_id=row["group_id"],
            plan_id=row["plan_id"],
            started_at=row["started_at"],
            expires_at=row["expires_at"],
            is_active=row["is_active"],
        )

    def to_entity(self) -> Subscription:
        return Subscription(
            id=self.id,
            group_id=self.group_id,
            plan_id=self.plan_id,
            started_at=_parse_dt(self.started_at),
            expires_at=_parse_dt(self.expires_at) or datetime.utcnow(),
            is_active=bool(self.is_active),
        )

    @classmethod
    def from_entity(cls, sub: Subscription) -> "SubscriptionModel":
        return cls(
            id=sub.id,
            group_id=sub.group_id,
            plan_id=sub.plan_id,
            started_at=sub.started_at.isoformat() if sub.started_at else None,
            expires_at=sub.expires_at.isoformat(),
            is_active=1 if sub.is_active else 0,
        )


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace(" ", "T"))
