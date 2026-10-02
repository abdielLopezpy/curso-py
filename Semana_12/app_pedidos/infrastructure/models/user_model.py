from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

import sqlite3

from application.entities.user import User, UserRole


@dataclass
class UserModel:
    """Representa una fila de la tabla `users`."""
    id: Optional[int]
    name: str
    email: str
    password_hash: str
    birthday: str
    role: str
    group_id: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "UserModel":
        return cls(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            password_hash=row["password_hash"],
            birthday=row["birthday"],
            role=row["role"],
            group_id=row["group_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def to_entity(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            email=self.email,
            password_hash=self.password_hash,
            birthday=date.fromisoformat(self.birthday),
            role=UserRole(self.role),
            group_id=self.group_id,
            created_at=_parse_dt(self.created_at),
            updated_at=_parse_dt(self.updated_at),
        )

    @classmethod
    def from_entity(cls, user: User) -> "UserModel":
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            birthday=user.birthday.isoformat(),
            role=user.role.value,
            group_id=user.group_id,
            created_at=user.created_at.isoformat() if user.created_at else None,
            updated_at=user.updated_at.isoformat() if user.updated_at else None,
        )


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace(" ", "T"))
