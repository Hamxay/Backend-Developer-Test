from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
ALGORITHM = "HS256"
JWT_SECRET_KEY = "your-secret-key"

from jose import jwt
from pydantic import ValidationError

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/pre/user/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(reuseable_oauth)):
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        print(payload)
        token_data = payload

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = None

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user


from jose import jwt, JWTError
import datetime

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def verify_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Check token expiration
        expiration = payload.get("exp")
        if expiration:
            expiration_datetime = datetime.datetime.fromtimestamp(expiration)
            if expiration_datetime < datetime.datetime.utcnow():
                # Token has expired
                return False
        return True  # Token is valid
    except JWTError:
        # Invalid token
        return False


# Example usage:
provided_token = "..."  # Replace with the provided token string
token_validity = verify_token(provided_token)
if token_validity:
    print("Token is valid.")
else:
    print("Token is invalid.")
