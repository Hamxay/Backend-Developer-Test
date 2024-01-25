from src.core.exceptions import RequestException


class AddressError:
    ADDRESS_NOT_FOUND = RequestException(
        "ADDRESS_NOT_FOUND",
        "The requested address was not found",
        404,
    )

    ADDRESS_INVALID_ERROR = RequestException(
        "ADDRESS_INVALID_ERROR",
        "The address provided is invalid",
        400,
    )
