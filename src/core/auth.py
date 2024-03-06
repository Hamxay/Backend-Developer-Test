from datetime import datetime, timezone
import logging
from typing import Annotated
from fastapi import Depends, Path
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt
from pydantic import BaseModel

from src.core.errors import AuthErrors
from src.settings import (
    ACCESS_TOKEN_ALGORITHM,
    ACCESS_TOKEN_SECRET_KEY,
)

log = logging.getLogger(__name__)


class AccessToken(BaseModel):
    email: str
    expiration_time: datetime


def require_access_token(
    auth: Annotated[
        HTTPAuthorizationCredentials,
        Depends(HTTPBearer(scheme_name="Access Token", auto_error=False)),
    ]
) -> AccessToken:
    if not auth:
        raise AuthErrors.UNAUTHORIZED

    try:
        payload = jwt.decode(
            auth.credentials,
            key=ACCESS_TOKEN_SECRET_KEY,
            algorithms=[ACCESS_TOKEN_ALGORITHM],
        )
    except jwt.InvalidTokenError as e:
        raise AuthErrors.ACCESS_TOKEN_INVALID from e

    try:
        return AccessToken(
            email=payload["email"],
            expiration_time=payload["exp"],
        )
    except (KeyError, ValueError) as e:
        log.warn("Received access token with invalid payload", exc_info=True)
        raise AuthErrors.ACCESS_TOKEN_INVALID from e


# def require_system_access_token(
#     access_token: Annotated[AccessToken, Depends(require_access_token)]
# ) -> None:
#     if access_token.context != AccessTokenContext.SYSTEM:
#         raise AuthErrors.FORBIDDEN


def require_valid_access_token(
    access_token: Annotated[AccessToken, Depends(require_access_token)],
) -> None:
    utc_now = datetime.now(timezone.utc)
    expiration_time_utc = access_token.expiration_time.replace(tzinfo=timezone.utc)
    if expiration_time_utc > utc_now:
        return
    else:
        raise AuthErrors.ACCESS_TOKEN_INVALID
