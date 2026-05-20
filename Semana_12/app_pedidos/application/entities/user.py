import re
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from typing import Optional

from application.exceptions import ValidationError


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MIN_PASSWORD_HASH_LEN = 8
ADULT_AGE = 18


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

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValidationError("El nombre no puede estar vacio")
        self.name = self.name.strip()

        if not EMAIL_RE.match(self.email or ""):
            raise ValidationError(f"Email invalido: {self.email!r}")
        self.email = self.email.lower()

        if not self.password_hash or len(self.password_hash) < MIN_PASSWORD_HASH_LEN:
            raise ValidationError("password_hash demasiado corto o vacio")

        if not isinstance(self.birthday, date):
            raise ValidationError("birthday debe ser datetime.date")
        if self.birthday > date.today():
            raise ValidationError("birthday no puede estar en el futuro")

        if isinstance(self.role, str):
            try:
                self.role = UserRole(self.role)
            except ValueError as e:
                raise ValidationError(f"Rol invalido: {self.role!r}") from e

        # Coherencia: un rol 'kid' no puede ser mayor de edad.
        if self.role == UserRole.KID and self._age() >= ADULT_AGE:
            raise ValidationError("Rol 'kid' solo aplica a menores de 18")

    def _age(self) -> int:
        today = date.today()
        return today.year - self.birthday.year - (
            (today.month, today.day) < (self.birthday.month, self.birthday.day)
        )

    @property
    def is_adult(self) -> bool:
        return self._age() >= ADULT_AGE

    def join_group(self, group_id: int) -> None:
        if group_id <= 0:
            raise ValidationError("group_id debe ser positivo")
        self.group_id = group_id

    def leave_group(self) -> None:
        self.group_id = None
