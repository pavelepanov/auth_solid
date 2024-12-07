from auth.application.user.errors import (
    AlreadyAuthenticatedError,
    AuthenticationError,
)
from auth.domain.user.entity import User
from auth.domain.user.errors.non_existence import UserNotFoundByUsername
from auth.domain.user.service import UserService
from auth.domain.user.value_objects import RawPassword, Username
from auth.infrastructure.adapters_application.identity_provider_session import (
    SessionIdentityProvider,
)
from auth.infrastructure.adapters_application.user_data_mapper_sqla import (
    SqlaUserDataMapper,
)
from auth.infrastructure.base.interactors import InteractorStrict
from auth.infrastructure.record_session import SessionRecord
from auth.infrastructure.session.services.jwt_token import JwtTokenService
from auth.infrastructure.session.services.session import SessionService
from auth.infrastructure.contracts.login import LogInRequest, LogInResponse


class LogInInteractor(InteractorStrict[LogInRequest, LogInResponse]):
    """
    :raises AlreadyAuthenticatedError:
    :raises DomainFieldError:
    :raises DataGatewayError:
    :raises UserNotFoundByUsername:
    """

    def __init__(
        self,
        session_identity_provider: SessionIdentityProvider,
        sqla_user_data_mapper: SqlaUserDataMapper,
        session_service: SessionService,
        jtw_token_service: JwtTokenService,
        user_service: UserService,
    ):
        self._session_identity_provider = session_identity_provider
        self._sqla_user_data_mapper = sqla_user_data_mapper
        self._session_service = session_service
        self._jwt_token_service = jtw_token_service
        self._user_service = user_service

    async def __call__(self, request_data: LogInRequest) -> LogInResponse:

        try:
            await self._session_identity_provider.get_current_user_id()
            raise AlreadyAuthenticatedError(
                "You are already authenticated. Consider logging out."
            )
        except AuthenticationError:
            pass

        username: Username = Username(request_data.username)
        password: RawPassword = RawPassword(request_data.password)

        user: User | None = await self._sqla_user_data_mapper.read_by_username(username)
        if user is None:
            raise UserNotFoundByUsername(username)

        if not self._user_service.is_password_valid(user, password):
            raise AuthenticationError("Invalid password.")

        if not user.is_active:
            raise AuthenticationError(
                "Your account is inactive. Please contact support."
            )

        session: SessionRecord = await self._session_service.create_session(user.id_)
        await self._session_service.save_session(session)

        access_token: str = self._jwt_token_service.issue_access_token(session.id_)
        self._jwt_token_service.add_access_token_to_request(access_token)

        return LogInResponse("Logged in: successful.")
    