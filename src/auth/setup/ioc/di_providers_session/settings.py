from dishka import Provider, Scope, provide

from auth.infrastructure.custom_types import (
    JwtAccessTokenTtlMin,
    JwtAlgorithm,
    JwtSecret,
    SessionRefreshThreshold,
)
from auth.presentation.http.cookie_params import CookieParams
from auth.setup.config.settings import Settings
from auth.setup.ioc.enum_component import ComponentEnum


class SessionSettingsProvider(Provider):
    component = ComponentEnum.SESSION
    scope = Scope.auth

    @provide
    def provide_jwt_secret(self, settings: Settings) -> JwtSecret:
        return JwtSecret(settings.security.session.jwt_secret)

    @provide
    def provide_jwt_algorithm(self, settings: Settings) -> JwtAlgorithm:
        return settings.security.session.jwt_algorithm

    @provide
    def provide_jwt_access_token_ttl_min(
        self, settings: Settings
    ) -> JwtAccessTokenTtlMin:
        return JwtAccessTokenTtlMin(settings.security.session.session_ttl_min)

    @provide
    def provide_session_refresh_threshold(
        self, settings: Settings
    ) -> SessionRefreshThreshold:
        return SessionRefreshThreshold(
            settings.security.session.session_refresh_threshold
        )

    @provide
    def provide_cookie_params(self, settings: Settings) -> CookieParams:
        is_cookies_secure: bool = settings.security.cookies.secure
        if is_cookies_secure:
            return CookieParams(secure=True, samesite="strict")
        return CookieParams(secure=False)