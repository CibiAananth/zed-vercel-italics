from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Literal, Protocol


UserRole = Literal["admin", "member", "guest"]


@dataclass(frozen=True)
class User:
    id: str
    name: str
    role: UserRole
    active: bool = True


class UserRepository(Protocol):
    def find_by_id(self, user_id: str) -> User | None: ...

    def save(self, user: User) -> None: ...


def hash_user(user: User) -> str:
    """Return a stable hash for cache keys."""
    payload = f"{user.id}:{user.role}:{user.active}"
    return sha256(payload.encode("utf-8")).hexdigest()


def load_user(repo: UserRepository, user_id: str) -> User | None:
    # Skip lookup for empty ids.
    if not user_id.strip():
        return None

    user = repo.find_by_id(user_id)
    if user and user.active:
        print(f"Loaded {user.name} ({user.role})")

    return user
