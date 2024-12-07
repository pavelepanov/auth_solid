from datetime import datetime, timedelta

from auth.domain.user.value_objects import UserId
from auth.infrastructure.persistence.sqla.committer import SqlaCommitter
from auth.infrastructure.record_session import SessionRecord
from auth.infrastructure.session.errors import SessionExpired, SessionNotFoundById
from auth.infrastructure.session.services.jwt_token import JwtTokenService
from auth.infrastructure.session.data_mapper_sqla import SqlaSessionDataMapper
from auth.infrastructure.session.id_generator_str import StrSessionIdGenerator
from auth.infrastructure.session.timer_utc import UtcSessionTimer


class SessionService:
    def __init__(
        self,
        str_session_id_generator: StrSessionIdGenerator,
        utc_session_timer: UtcSessionTimer,
        sqla_session_data_mapper: SqlaSessionDataMapper,
        sqla_committer: SqlaCommitter,
        jwt_token_service: JwtTokenService,
    ):
        self._str_session_id_generator = str_session_id_generator
        self._utc_session_timer = utc_session_timer
        self._sqla_session_data_mapper = sqla_session_data_mapper
        self._sqla_committer = sqla_committer
        self._jwt_token_service = jwt_token_service

    async def create_session(self, user_id: UserId) -> SessionRecord:

        session_id: str = self._str_session_id_generator()
        expiration: datetime = self._utc_session_timer.access_expiration
        session_record: SessionRecord = SessionRecord(
            id_=session_id,
            user_id=user_id,
            expiration=expiration,
        )

        return session_record

    async def save_session(self, session_record: SessionRecord) -> None:
        """
        :raises DataGatewayError:
        """
        await self._sqla_session_data_mapper.save(session_record)

        await self._sqla_committer.commit()

    async def get_session(
        self, session_id: str, for_update: bool = False
    ) -> SessionRecord:
        """
        :raises DataGatewayError:
        :raises SessionNotFoundById:
        """

        session: SessionRecord | None = await self._sqla_session_data_mapper.read(
            session_id, for_update=for_update
        )
        if session is None:
            raise SessionNotFoundById(session_id)

        return session

    async def get_current_session(self) -> SessionRecord:
        """
        :raises AdapterError:
        :raises DataGatewayError:
        :raises SessionNotFoundById:
        """

        access_token: str = self._jwt_token_service.get_access_token_from_request()
        session_id: str = self._jwt_token_service.get_session_id_from_access_token(
            access_token
        )

        session: SessionRecord = await self.get_session(session_id)

        return session

    def check_session_expiration(self, session: SessionRecord) -> None:
        """
        :raises SessionExpired:
        """

        if session.expiration <= self._utc_session_timer.current_time:
            raise SessionExpired(session.id_)

    def is_session_near_expiry(self, session: SessionRecord) -> bool:

        time_remaining: timedelta = (
            session.expiration - self._utc_session_timer.current_time
        )

        return time_remaining < self._utc_session_timer.refresh_trigger_interval

    async def prolong_session(self, session: SessionRecord) -> None:
        """
        :raises DataGatewayError:
        """

        new_expiration: datetime = self._utc_session_timer.access_expiration
        session.expiration = new_expiration

        await self._sqla_session_data_mapper.save(session)

        await self._sqla_committer.commit()

    async def delete_session(self, session_id: str) -> None:
        """
        :raises DataGatewayError:
        :raises SessionNotFoundById:
        """

        if not await self._sqla_session_data_mapper.delete(session_id):
            raise SessionNotFoundById(session_id)

        await self._sqla_committer.commit()
