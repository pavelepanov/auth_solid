from abc import abstractmethod
from typing import Protocol

from auth.domain.user.enums import UserRoleEnum
from auth.domain.user.value_objects import UserId


class IdentityProvider(Protocol):
    @abstractmethod
    async def get_current_user_id(self) -> UserId:
        """
        :raises AuthenticationError:
        """

    @abstractmethod
    async def get_current_user_roles(self) -> set[UserRoleEnum]:
        """
        :raises AuthenticationError:
        """
