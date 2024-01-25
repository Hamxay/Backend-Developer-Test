from src.core.exceptions import RequestException


class AuthErrors:
    ACCESS_TOKEN_INVALID = RequestException(
        "ACCESS_TOKEN_INVALID",
        "Access token is invalid or has expired",
        401,
    )

    FORBIDDEN = RequestException(
        "FORBIDDEN",
        "You're not allowed to perform this request",
        403,
    )

    FORBIDDEN_ORGANIZATION = RequestException(
        "FORBIDDEN_ORGANIZATION",
        "You're not allowed to access resources of this organization",
        403,
    )

    UNAUTHORIZED = RequestException(
        "UNAUTHORIZED",
        "You need to be authenticated to perform this request",
        401,
    )
