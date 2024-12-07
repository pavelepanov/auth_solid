from dishka import Provider, Scope, provide

from auth.infrastructure.custom_types import PasswordPepper
from auth.setup.config.settings import Settings
from auth.setup.ioc.enum_component import ComponentEnum


class UserSettingsProvider(Provider):
    component = ComponentEnum.USER
    scope = Scope.APP

    @provide
    def provide_password_pepper(self, settings: Settings) -> PasswordPepper:
        return PasswordPepper(settings.security.password.pepper)
