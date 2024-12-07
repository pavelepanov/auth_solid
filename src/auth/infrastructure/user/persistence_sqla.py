__all__ = ("User",)

from sqlalchemy import (
    ARRAY,
    UUID,
    Boolean,
    Column,
    Enum,
    ExecutionContext,
    LargeBinary,
    String,
    Table,
    event,
)
from sqlalchemy.ext.mutable import MutableSet
from sqlalchemy.orm import composite

from auth.domain.user.entity import User
from auth.domain.user.enums import UserRoleEnum
from auth.domain.user.validation.constants import USERNAME_MAX_LEN
from auth.domain.user.value_objects import UserId, Username, UserPasswordHash
from auth.infrastructure.persistence.sqla.orm_registry import mapper_registry

users_table = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("username", String(USERNAME_MAX_LEN), nullable=False, unique=True),
    Column("password_hash", LargeBinary, nullable=False),
    Column(
        "roles",
        MutableSet.as_mutable(ARRAY(Enum(UserRoleEnum))),
        default=[UserRoleEnum.USER],
        nullable=False,
    ),
    Column("is_active", Boolean, default=True, nullable=False),
)

mapper_registry.map_imperatively(
    User,
    users_table,
    properties={
        "id_": composite(UserId, users_table.c.id),
        "username": composite(Username, users_table.c.username),
        "password_hash": composite(UserPasswordHash, users_table.c.password_hash),
        "roles": users_table.c.roles,
        "is_active": users_table.c.is_active,
    },
    column_prefix="_",
)


@event.listens_for(User, "load")
def receive_load(target: User, _: ExecutionContext) -> None:
    target.roles = set(target.roles) if isinstance(target.roles, list) else target.roles