from fastapi import APIRouter

from auth.presentation.http.routers.account_log_in import log_in_router
from auth.presentation.http.routers.account_log_out import log_out_router
from auth.presentation.http.routers.account_sign_up import sign_up_router

account_router = APIRouter(
    prefix="/account",
    tags=["Account"],
)

account_sub_routers = (
    sign_up_router,
    log_in_router,
    log_out_router,
)

for router in account_sub_routers:
    account_router.include_router(router)
