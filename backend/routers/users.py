from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Optional, Union, Annotated
from schemas import schemas, custom_types
from crud import crud
from pymongo.database import Database
from services import encryption
from db.db_handler import get_db
from pymongo import errors as pymongo_errors
from utils.setup import Setup
from bson import ObjectId
from utils.decorators import handle_mongodb_exceptions
from fastapi.security import OAuth2PasswordBearer
from pydantic import TypeAdapter
import json
from crud import queries
from services import data_service

users = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/signin")


def read_token_from_header_factory(roles: list[str] = None):
    def read_token_from_header(token: Annotated[str, Depends(oauth2_scheme)]):
        payload = encryption.read_token(token)
        if roles and payload["role"] not in roles:
            raise HTTPException(
                status_code=401, detail=f"Only {roles} can do this action."
            )
        return payload

    return read_token_from_header


def password_validator(password: str) -> str:
    return TypeAdapter(custom_types.Password).validate_python(password)


@users.post("/signup")
@handle_mongodb_exceptions
async def signup(
    user_data: schemas.AdminSensitiveData
    | schemas.TeacherSensitiveData
    | schemas.ScoreBase
    | schemas.RelativeSensitiveData,
    user_role: custom_types.User,
    db: Database = Depends(get_db),
):
    """Register a new user. Encrypts the password and adds user-specific data based on their role."""

    # Hash Password
    hashed_password = encryption.encrypt_password(user_data.password)
    user_data.password = hashed_password

    user_id = await data_service.create_service(
        data=user_data,
        key_to_schema_map=user_role,
        db=db,
    )

    # Create a JWT token
    token = encryption.create_jwt_token(user_id, user_role)

    # Return response
    return {"token": token, "id": user_id}


@users.post("/signin")
@handle_mongodb_exceptions
async def signin(
    user_role: schemas.User,
    credentials: schemas.Signin,
    db: Database = Depends(get_db),
):
    # Find User
    user_data = await data_service.read_service(
        search_query=credentials.get_email_query(),
        key_to_schema_map=user_role,
        db=db,
        isSensitive=True,
    )

    # Verify password
    if not encryption.check_password(credentials.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    # Create a JWT
    token = encryption.create_jwt_token(
        user_id=str(user_data[f"{Setup.id}"]),
        user_role=user_role,
    )

    # Return the response
    return {
        "token": token,
        f"{Setup.id}": user_data[f"{Setup.id}"],
        f"{Setup.role}": user_role,
    }


@users.get("/search")
@handle_mongodb_exceptions
async def read_other_user(
    role: schemas.User,
    search_query: str,
    db: Database = Depends(get_db),
    _: dict = Depends(read_token_from_header_factory()),
) -> dict:
    """Retries a user from database without sensitive information"""

    # Use the Read Service
    user_data = data_service.read_service(
        search_query=search_query,
        key_to_schema_map=role,
        db=db,
    )

    # Build Response
    response = schemas.UserFactory.create_user(role, user_data)
    return response.dict()


@users.get("/")
@handle_mongodb_exceptions
async def read_user(
    db: Database = Depends(get_db),
    token_payload: dict = Depends(read_token_from_header_factory()),
) -> dict:
    """Retries a user from database without sensitive information"""
    # Collect inputs
    user_id = token_payload[f"{Setup.id}"]
    user_role = token_payload[f"{Setup.role}"]
    search_query = {f"{Setup.id}": user_id}

    # Use the Read Service
    user_data = await data_service.read_service(
        search_query=search_query,
        key_to_schema_map=user_role,
        db=db,
    )

    # Build Response
    response = schemas.UserFactory.create_user(user_role, user_data)
    return response.dict()


@users.patch("/change_password")
@handle_mongodb_exceptions
async def update_user_password(
    old_password: str = Depends(password_validator),
    new_password: str = Depends(password_validator),
    db: Database = Depends(get_db),
    token_payload: dict = Depends(
        read_token_from_header_factory(),
    ),
) -> dict:
    # Validate passwords
    if old_password == new_password:
        raise HTTPException(
            status_code=422, detail="Old password and New Passwords are the same"
        )

    role = token_payload[f"{Setup.role}"]
    user_id = token_payload[f"{Setup.id}"]

    user_data = await crud.get_user_by_email(
        collection=role,
        user_id=user_id,
        db=db,
    )

    if not user_data:
        HTTPException(status_code=404, detail="User not found on dB.")

    if encryption.check_password(old_password, user_data["password"]):
        result = await crud.update_n_documents(
            collection=role,
            update_data={"password": new_password},
            search_query={"_id": ObjectId(user_id)},
            db=db,
            multi=False,
        )

        if result.modified_count > 0:
            return {"message": "Password Changed successfully"}
        else:
            raise HTTPException(status_code=410, detail="Password was NOT updated.")


@users.patch("/")
@handle_mongodb_exceptions
async def update_user(
    update_query: dict,
    db: Database = Depends(get_db),
    token_payload: dict = Depends(read_token_from_header_factory()),
) -> dict:
    """Update user data based on the user role."""
    # Extract user ID and role from the token payload
    user_id = token_payload[f"{Setup.id}"]
    user_role = token_payload[f"{Setup.role}"]
    search_query = {f"{Setup.id}": user_id}

    return await data_service.update_service(
        search_query=search_query,
        update_query=update_query,
        key_to_schema_map=user_role,
        db=db,
    )


@users.delete("/")
@handle_mongodb_exceptions
async def delete_user(
    password: str = Depends(password_validator),
    db: Database = Depends(get_db),
    token_payload: str = Depends(read_token_from_header_factory()),
):
    """Delete a user after verifying their password."""

    # Extract user ID and role from the token payload
    user_id = token_payload[f"{Setup.id}"]
    user_role = token_payload[f"{Setup.role}"]
    search_query = {f"{Setup.id}": user_id}

    user_data = await data_service.read_service(
        search_query=search_query,
        key_to_schema_map=user_role,
        db=db,
        isSensitive=True,
    )

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if the provided password matches the user's password
    if not encryption.check_password(password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return await data_service.delete_service(
        search_query=search_query,
        key_to_schema_map=user_role,
        db=db,
    )
