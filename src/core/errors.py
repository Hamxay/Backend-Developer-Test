from src.core.exceptions import RequestException


class AuthErrors:
    ACCESS_TOKEN_INVALID = RequestException(
        "ACCESS_TOKEN_INVALID",
        "Access token is invalid or has expired",
        401,
    )

    ACCESS_TOKEN_DECODE_ERROR = RequestException(
        "ACCESS_TOKEN_DECODE_ERROR",
        "Access token can not be decoded",
        401,
    )

    FORBIDDEN = RequestException(
        "FORBIDDEN",
        "You're not allowed to perform this request",
        403,
    )

    UNAUTHORIZED = RequestException(
        "UNAUTHORIZED",
        "You need to be authenticated to perform this request",
        401,
    )
