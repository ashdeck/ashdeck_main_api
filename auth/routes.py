from fastapi import APIRouter, HTTPException, Depends
from .models import SignUp, LoginResponse, SignUpResponse
from uuid import uuid4
from deps.auth.auth import (
    hash_password,
    authenticate_user,
    get_current_user
    )
from deps.auth.tokens import create_token
from deps.auth.models import TokenData
from app.db import db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timezone


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")

router = APIRouter()


@router.post("", status_code=201, description="Create account")
async def create_account(user: SignUp) -> SignUpResponse:
    user_collection = db["users"]
    check_user = user_collection.find_one({"email": user.email.lower()})
    if check_user:
        HTTPException(status_code=405, detail="User with this email already exists!")
    user_dict = user.model_dump()
    user_dict["_id"] = str(uuid4())
    user_dict["password"] = hash_password(user.password)

    # add user to DB
    user_collection.insert_one(user_dict)

    user_res = SignUpResponse(
        id=user_dict["_id"],
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email.lower()
    )

    # send welcome email and activation link
    return user_res


@router.post("/login", status_code=200, description="Login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> LoginResponse:
    user = authenticate_user(db["users"], form_data.username, form_data.password)

    access_token = create_token(TokenData(id=user["_id"], expires=60))
    refresh_token = create_token(TokenData(id=user["_id"], expires=2880))

    db["users"].update_one(
            {"_id": user["_id"]},
            {"$set": {"updated_at": datetime.now(timezone.utc), "last_login": datetime.now(timezone.utc)}}
            )

    # add user to redis with key as user_id

    # authenticate user with email
    res = LoginResponse(
        id=user["_id"],
        email=form_data.username,
        first_name=user["first_name"],
        last_name=user["last_name"],
        access_token=access_token,
        refresh_token=refresh_token
    )
    return res


# change password

# forgot password

# logout
@router.get("/logout", status_code=200, description="Logout")
async def logout(user=Depends(get_current_user)):
    # remove user from redis
    print(user)
    return {"detail": "User logged out successfully."}
