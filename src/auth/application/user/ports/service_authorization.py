from auth.application.user.errors import AuthorizationError
from auth.application.user.ports.identity_provider import IdentityProvider
from auth.domain.user.enums import UserRoleEnum


class AuthorizationService:
    def __init__(
        self,
        identity_provider: IdentityProvider,
    ):
        self._identity_provider = identity_provider

    async def check_authorization(self, role_required: UserRoleEnum) -> None:
        """
        :raises AuthenticationError:
        :raises AuthorizationError:
        """

        current_user_roles: set[UserRoleEnum] = (
            await self._identity_provider.get_current_user_roles()
        )

        if role_required not in current_user_roles:
            raise AuthorizationError("Authorization failed.")