from fastapi import APIRouter
from fastapi.requests import Request

from auth.presentation.http.controllers.account import account_router
from auth.presentation.http.controllers.users import users_router

api_v1_router = APIRouter(
    prefix="/api/v1",
)


@api_v1_router.get("/", tags=["General"])
async def healthcheck(_: Request) -> dict[str, str]:
    return {"status": "ok"}


api_v1_sub_routers = (
    account_router,
    users_router,
)

for router in api_v1_sub_routers:
    api_v1_router.include_router(router)