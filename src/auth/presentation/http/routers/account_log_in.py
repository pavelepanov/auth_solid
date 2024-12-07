from typing import Annotated

from dishka import FromComponent
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, status

from auth.infrastructure.scenarios.account_log_in.interactor import LogInInteractor
from auth.infrastructure.contracts.login import  (
    LogInRequest,
    LogInResponse,
)
from auth.presentation.http.exception_handler import ExceptionSchema
from auth.setup.ioc.enum_component import ComponentEnum

log_in_router = APIRouter()


@log_in_router.post(
    "/login",
    responses={
        status.HTTP_200_OK: {"model": LogInResponse},
        status.HTTP_400_BAD_REQUEST: {"model": ExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionSchema},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ExceptionSchema},
    },
    status_code=status.HTTP_200_OK,
)
@inject
async def login(
    request_data: LogInRequest,
    interactor: Annotated[
        LogInInteractor,
        FromComponent(ComponentEnum.SESSION),
    ],
) -> LogInResponse:
    # :raises AlreadyAuthenticatedError 401:
    # :raises DomainFieldError 400:
    # :raises DataGatewayError 500:
    # :raises UserNotFoundByUsername 404:
    return await interactor(request_data)
