from auth.application.base.interactors import InteractorFlexible
from auth.application.errors import DataGatewayError
from auth.application.user.errors import AuthenticationError
from auth.domain.user.entity import User
from auth.domain.user.value_objects import UserId
from auth.infrastructure.adapters_application.identity_provider_session import (
    SessionIdentityProvider,
)
from auth.infrastructure.adapters_application.user_data_mapper_sqla import (
    SqlaUserDataMapper,
)
from auth.infrastructure.record_session import SessionRecord
from auth.infrastructure.session.errors import AdapterError, SessionNotFoundById
from auth.infrastructure.session.services.jwt_token import JwtTokenService
from auth.infrastructure.session.services.session import SessionService
from auth.infrastructure.contracts.logout import LogOutResponse


class LogOutInteractor(InteractorFlexible):
    """
    :raises AuthenticationError:
    :raises DataGatewayError:
    """

    def __init__(
        self,
        session_identity_provider: SessionIdentityProvider,
        sqla_user_data_mapper: SqlaUserDataMapper,
        session_service: SessionService,
        jtw_token_service: JwtTokenService,
    ):
        self._session_identity_provider = session_identity_provider
        self._sqla_user_data_mapper = sqla_user_data_mapper
        self._session_service = session_service
        self._jwt_token_service = jtw_token_service

    async def __call__(self) -> LogOutResponse:

        user_id: UserId = await self._session_identity_provider.get_current_user_id()

        user: User | None = await self._sqla_user_data_mapper.read_by_id(user_id)
        if user is None:
            raise AuthenticationError("Not authenticated.")

        try:
            current_session: SessionRecord = (
                await self._session_service.get_current_session()
            )
        except (AdapterError, DataGatewayError, SessionNotFoundById) as error:
            raise AuthenticationError("Not authenticated.") from error

        self._jwt_token_service.delete_access_token_from_request()

        try:
            await self._session_service.delete_session(current_session.id_)
        except (DataGatewayError, SessionNotFoundById) as error:
            raise DataGatewayError("Session deletion failed.") from error

        return LogOutResponse("Logged out: successful.")