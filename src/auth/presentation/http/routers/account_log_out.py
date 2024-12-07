from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Security, status

from auth.infrastructure.scenarios.account_log_out import LogOutInteractor
from auth.infrastructure.contracts.logout import LogOutResponse
from auth.presentation.http.dependencies import cookie_scheme
from auth.presentation.http.exception_handler import ExceptionSchema
from auth.setup.ioc.enum_component import ComponentEnum

log_out_router = APIRouter()


@log_out_router.delete(
    "/logout",
    responses={
        status.HTTP_200_OK: {"model": LogOutResponse},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
    dependencies=[Security(cookie_scheme)],
)
@inject
async def logout(
    interactor: Annotated[
        LogOutInteractor,
        FromComponent(ComponentEnum.SESSION),
    ],
) -> LogOutResponse:
    # :raises AuthenticationError 401:
    # :raises DataGatewayError 500:
    return await interactor()
