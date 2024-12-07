from fastapi.requests import Request

from auth.infrastructure.session.errors import AdapterError
from auth.infrastructure.session.ports.access_token_request_handler import (
    AccessTokenRequestHandler,
)
from auth.presentation.http.cookie_params import CookieParams


class CookieAccessTokenRequestHandler(AccessTokenRequestHandler):
    def __init__(
        self,
        request: Request,
        cookie_params: CookieParams,
    ):
        self._request = request
        self._cookie_params = cookie_params

    def get_access_token_from_request(self) -> str:
        """
        :raises AdapterError:
        """
        if (access_token := self._request.cookies.get("access_token")) is None:
            raise AdapterError("No access token in cookies.")
        return access_token

    def add_access_token_to_request(self, new_access_token: str) -> None:
        self._request.state.new_access_token = new_access_token
        self._request.state.cookie_params = {
            "secure": self._cookie_params.secure,
            "samesite": self._cookie_params.samesite,
        }

    def delete_access_token_from_request(self) -> None:
        self._request.state.delete_access_token = True
        try:
            self._request.state.access_token = self.get_access_token_from_request()
        except AdapterError:
            ...
        