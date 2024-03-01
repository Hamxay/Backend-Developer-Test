from src.core.exceptions import RequestException


class PostErrors:
    POST_NOT_FOUND = RequestException(
        "POST_NOT_FOUND",
        "The requested POST was not found",
        404,
    )
    UNAUTHORIZED_USER = RequestException(
        "UNAUTHORIZED_USER",
        "The user must have a valid token",
        404,
    )
    POST_ALREADY_EXISTS = RequestException(
        "POST_ALREADY_EXISTS",
        "This POST is already registered ",
        400,
    )
    POST_UPDATE_ERROR = RequestException(
        "POST_UPDATE_ERROR",
        "An error occurred during POST update",
        400,
    )

    @staticmethod
    def dynamic_error(
        code: str, message: str, status_code: int = 400
    ) -> RequestException:
        """
        Create a dynamic RequestException with the given code, message, and status code.
        :param code: The error code.
        :param message: The error message.
        :param status_code: The HTTP status code (default is 400).
        :return: A new instance of RequestException.
        """
        return RequestException(code, message, status_code)
