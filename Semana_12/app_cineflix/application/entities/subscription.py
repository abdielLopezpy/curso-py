from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Subscription:
    id: Optional[int]
    group_id: int
    plan_id: int
    expires_at: datetime
    started_at: Optional[datetime] = None
    is_active: bool = True

    def is_expired(self, now: Optional[datetime] = None) -> bool:
        now = now or datetime.utcnow()
        return now >= self.expires_at
