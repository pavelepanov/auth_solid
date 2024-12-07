from dataclasses import dataclass

from auth.domain.base.entity import Entity
from auth.domain.user.enums import UserRoleEnum
from auth.domain.user.value_objects import UserId, Username, UserPasswordHash


@dataclass(eq=False, kw_only=True)
class User(Entity[UserId]):
    username: Username
    password_hash: UserPasswordHash
    roles: set[UserRoleEnum]
    is_active: bool
