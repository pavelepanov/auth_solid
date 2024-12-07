from auth.application.errors import DataGatewayError
from auth.application.user.errors import AuthenticationError
from auth.application.user.ports.identity_provider import IdentityProvider
from auth.domain.user.entity import User
from auth.domain.user.enums import UserRoleEnum
from auth.domain.user.errors.non_existence import UserNotFoundById
from auth.domain.user.value_objects import UserId
from auth.infrastructure.adapters_application.user_data_mapper_sqla import (
    SqlaUserDataMapper,
)
from auth.infrastructure.record_session import SessionRecord
from auth.infrastructure.session.errors import (
    AdapterError,
    SessionExpired,
    SessionNotFoundById,
)
from auth.infrastructure.session.services.jwt_token import JwtTokenService
from auth.infrastructure.session.services.session import SessionService



class SessionIdentityProvider(IdentityProvider):
    def __init__(
        self,
        jwt_token_service: JwtTokenService,
        session_service: SessionService,
        sqla_user_data_mapper: SqlaUserDataMapper,
    ):
        self._jwt_token_service = jwt_token_service
        self._session_service = session_service
        self._sqla_user_data_mapper = sqla_user_data_mapper

    async def get_current_user_id(self) -> UserId:
        """
        :raises AuthenticationError:
        """

        try:
            access_token: str = self._jwt_token_service.get_access_token_from_request()
            session_id: str = self._jwt_token_service.get_session_id_from_access_token(
                access_token
            )
        except AdapterError as error:
            raise AuthenticationError("Not authenticated") from error

        try:
            session: SessionRecord = await self._session_service.get_session(
                session_id, for_update=True
            )
        except (DataGatewayError, SessionNotFoundById) as error:
            raise AuthenticationError("Not authenticated") from error

        try:
            self._session_service.check_session_expiration(session)
        except SessionExpired as error:
            raise AuthenticationError("Not authenticated") from error

        if self._session_service.is_session_near_expiry(session):
            await self._session_service.prolong_session(session)

        return session.user_id

    async def get_current_user_roles(self) -> set[UserRoleEnum]:
        """
        :raises AuthenticationError:
        """

        user_id: UserId = await self.get_current_user_id()

        try:
            user: User | None = await self._sqla_user_data_mapper.read_by_id(user_id)
            if user is None:
                raise UserNotFoundById(user_id)
        except (DataGatewayError, UserNotFoundById) as error:
            raise AuthenticationError("Not authenticated") from error

        return user.roles