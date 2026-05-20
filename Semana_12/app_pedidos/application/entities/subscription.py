from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from application.exceptions import BusinessRuleError, ValidationError


@dataclass
class Subscription:
    id: Optional[int]
    group_id: int
    plan_id: int
    expires_at: datetime
    started_at: Optional[datetime] = None
    is_active: bool = True

    def __post_init__(self) -> None:
        if self.group_id <= 0:
            raise ValidationError("group_id debe ser positivo")
        if self.plan_id <= 0:
            raise ValidationError("plan_id debe ser positivo")
        if not isinstance(self.expires_at, datetime):
            raise ValidationError("expires_at debe ser datetime")
        if self.started_at and self.started_at >= self.expires_at:
            raise ValidationError("started_at debe ser anterior a expires_at")

    def is_expired(self, now: Optional[datetime] = None) -> bool:
        return (now or datetime.utcnow()) >= self.expires_at

    def is_valid(self, now: Optional[datetime] = None) -> bool:
        return self.is_active and not self.is_expired(now)

    def cancel(self) -> None:
        if not self.is_active:
            raise BusinessRuleError("La suscripcion ya estaba cancelada")
        self.is_active = False

    def renew(self, new_expires_at: datetime) -> None:
        if new_expires_at <= self.expires_at:
            raise BusinessRuleError(
                "La nueva fecha de expiracion debe ser posterior a la actual"
            )
        self.expires_at = new_expires_at
        self.is_active = True
