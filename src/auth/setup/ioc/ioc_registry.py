from typing import Iterable

from dishka import Provider

from auth.setup.ioc.di_providers_common.connection import CommonConnectionInfraProvider
from auth.setup.ioc.di_providers_common.settings import (
    CommonSettingsProvider,
    SettingsProvider,
)
from auth.setup.ioc.di_providers_session.connection import SessionConnectionInfraProvider
from auth.setup.ioc.di_providers_session.infrastructure import (
    SessionInfraConcreteProvider,
    SessionInfraDataMappersProvider,
    SessionInfraInteractorProvider,
    SessionInfraPortsProvider,
)
from auth.setup.ioc.di_providers_session.settings import SessionSettingsProvider
from auth.setup.ioc.di_providers_user.application import (
    UserApplicationDataGatewaysProvider,
    UserApplicationInteractorsProvider,
    UserApplicationPortsProvider,
    UserApplicationServicesProvider,
)
from auth.setup.ioc.di_providers_user.connection import UserConnectionInfraProvider
from auth.setup.ioc.di_providers_user.domain import (
    UserDomainPortsProvider,
    UserDomainServicesProvider,
)
from auth.setup.ioc.di_providers_user.settings import UserSettingsProvider


def get_providers() -> Iterable[Provider]:
    settings = (
        SettingsProvider(),
        CommonSettingsProvider(),
        UserSettingsProvider(),
        SessionSettingsProvider(),
    )

    connection_common = (CommonConnectionInfraProvider(),)
    connection_user = (UserConnectionInfraProvider(),)
    connection_session = (SessionConnectionInfraProvider(),)

    domain_user = (
        UserDomainServicesProvider(),
        UserDomainPortsProvider(),
    )

    application_user = (
        UserApplicationServicesProvider(),
        UserApplicationDataGatewaysProvider(),
        UserApplicationPortsProvider(),
        UserApplicationInteractorsProvider(),
    )

    infrastructure_session = (
        SessionInfraDataMappersProvider(),
        SessionInfraPortsProvider(),
        SessionInfraConcreteProvider(),
        SessionInfraInteractorProvider(),
    )

    return (
        *settings,
        *connection_common,
        *connection_user,
        *connection_session,
        *domain_user,
        *application_user,
        *infrastructure_session,
    )