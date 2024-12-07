from uuid import UUID

import uuid6

from auth.domain.user.ports.user_id_generator import UserIdGenerator


class UuidUserIdGenerator(UserIdGenerator):
    def __call__(self) -> UUID:
        return uuid6.uuid7()
