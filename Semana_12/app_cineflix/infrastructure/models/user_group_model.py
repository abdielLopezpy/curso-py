from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import sqlite3

from application.entities.user_group import UserGroup


@dataclass
class UserGroupModel:
    """Representa una fila de la tabla `user_groups`."""
    id: Optional[int]
    name: str
    owner_id: int
    created_at: Optional[str]
    updated_at: Optional[str]

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "UserGroupModel":
        return cls(
            id=row["id"],
            name=row["name"],
            owner_id=row["owner_id"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def to_entity(self) -> UserGroup:
        return UserGroup(
            id=self.id,
            name=self.name,
            owner_id=self.owner_id,
            created_at=_parse_dt(self.created_at),
            updated_at=_parse_dt(self.updated_at),
        )

    @classmethod
    def from_entity(cls, group: UserGroup) -> "UserGroupModel":
        return cls(
            id=group.id,
            name=group.name,
            owner_id=group.owner_id,
            created_at=group.created_at.isoformat() if group.created_at else None,
            updated_at=group.updated_at.isoformat() if group.updated_at else None,
        )


def _parse_dt(value: Optional[str]) -> Optional[datetime]:
    if value is None:
        return None
    return datetime.fromisoformat(value.replace(" ", "T"))
