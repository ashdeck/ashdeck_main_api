from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from pydantic import EmailStr
from .tokens import decode_jwt_token
from app.db import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)


def hash_password(password):
    return password_context.hash(password)


def get_unauthenticated_user(db_collection, email: EmailStr):
    user = db_collection.find_one({"email": email})
    if user:
        if not user.get("email_verified"):
            raise HTTPException(
                status_code=403, detail="Please verify your email address."
            )
        return user
    else:
        # print(user)
        return False


def authenticate_user(db_collection, username: str, password: str):
    user = get_unauthenticated_user(db_collection, username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=401, detail="Invalid email or password."
        )
    return user


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # return {"email": "joshuamjv9@gmail.com"}

    if not token:
        raise credentials_exception

    try:
        payload = decode_jwt_token(token)
        user_id: str = payload.get("sub")

        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # check redis by user_id
    user = db["users"].find_one({"_id": user_id})
    return user
