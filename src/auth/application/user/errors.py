from auth.application.base.errors import ApplicationError


class AuthorizationError(ApplicationError):
    ...


class AuthenticationError(ApplicationError):
    ...


class AlreadyAuthenticatedError(ApplicationError):
    ...
