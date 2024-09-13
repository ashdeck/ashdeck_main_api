from jose import jwt
from fastapi import HTTPException
from .models import TokenData, TokenExpiry
from datetime import timedelta, datetime, timezone
from .env_vars import JWT_ALGORITHM, JWT_SECRET_KEY
import secrets


# create tokens
def create_token(data: TokenData, secret_key=JWT_SECRET_KEY):
    expiry = datetime.now(timezone.utc) + timedelta(minutes=data.expires)
    token_info = {
        "sub": data.id,
        "exp": expiry,
        "jti": secrets.token_hex(16),
        "iat": datetime.now(timezone.utc)
    }
    encoded_jwt = jwt.encode(token_info, key=secret_key, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token: str):
    decoded_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
    return decoded_payload


def check_token_expiry(token_info: TokenExpiry):
    expiry = token_info.expiry
    current_time = datetime.now(timezone.utc)
    if current_time > expiry:
        raise HTTPException(status_code=401, detail="Token is expired")


# validate tokens
# invalidate tokens
# encrypt and decrypt
