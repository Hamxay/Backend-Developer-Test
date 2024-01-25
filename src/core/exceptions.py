import logging
from typing import Sequence, TYPE_CHECKING

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.core.schemas import Error, ErrorDetail

if TYPE_CHECKING:
    from pydantic.error_wrappers import ErrorDict


log = logging.getLogger(__name__)


class RequestException(Exception):
    def __init__(
        self,
        name: str,
        message: str,
        status_code: int = 400,
    ):
        self.name = name
        self.message = message
        self.status_code = status_code


def handle_validation_exception(exc: RequestValidationError) -> JSONResponse:
    return _create_error_response(
        name="VALIDATION_ERROR",
        message="The request is invalid",
        details=[_create_error_detail(err) for err in exc.errors()],
        status_code=422,
    )


def handle_request_exception(exc: RequestException) -> JSONResponse:
    return _create_error_response(
        name=exc.name,
        message=exc.message,
        status_code=exc.status_code,
    )


def handle_internal_exception(exc: Exception) -> JSONResponse:
    log.exception("Unhandled exception", exc_info=True)

    return _create_error_response(
        name="UNEXPECTED_ERROR",
        message="An unexpected error occurred.",
        status_code=500,
    )


def _create_error_detail(error: "ErrorDict") -> ErrorDetail:
    location, *path = error["loc"]

    if error["type"] == "value_error.jsondecode":
        field = None
    elif location == "body":
        # Convert key list to json pointer
        field = "/" + "/".join(str(x) for x in path)
    else:
        field = str(path[0])

    return ErrorDetail(
        field=field,
        issue=error["msg"],
        location=location,  # type: ignore
    )


def _create_error_response(
    name: str,
    message: str,
    status_code: int,
    details: Sequence[ErrorDetail] | None = None,
) -> JSONResponse:
    error = Error(name=name, message=message, details=details)
    return JSONResponse(jsonable_encoder(error, exclude_none=True), status_code)
