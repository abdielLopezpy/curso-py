from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    ADMIN = "admin"
    STANDARD = "standard"
    KID = "kid"


@dataclass
class User:
    id: Optional[int]
    name: str
    email: str
    password_hash: str
    birthday: date
    role: UserRole = UserRole.STANDARD
    group_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def is_adult(self) -> bool:
        today = date.today()
        years = today.year - self.birthday.year - (
            (today.month, today.day) < (self.birthday.month, self.birthday.day)
        )
        return years >= 18
