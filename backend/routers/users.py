from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, Union, Annotated
from schemas import schemas, custom_types
from crud import crud
from pymongo.database import Database
from utils import encryption
from db.db_handler import get_db
from pymongo import errors as pymongo_errors
from utils.setup import Setup
from bson import ObjectId
from utils.decorators import handle_mongodb_exceptions
from fastapi.security import OAuth2PasswordBearer
import json

users = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/signin")


def read_token_from_header(token: Annotated[str, Depends(oauth2_scheme)]):
    return encryption.read_token(token)


def read_token_admin_only(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = encryption.read_token(token)
    if payload[f"{Setup.role}"] == custom_types.User.ADMIN.value:
        return payload
    else:
        raise HTTPException(status_code=401, detail="Only Admins can do this action")


def user_role_fun(user_role):
    """This is necessary because fastAPI doesn't let Query Parameters have complex types"""
    object = schemas.UserRoles(role=user_role)
    return object.role


@users.post("/signup")
@handle_mongodb_exceptions
async def signup(
    user_data: schemas.Signup,
    user_role: str = Depends(user_role_fun),
    db: Database = Depends(get_db),
):
    """Register a new user. Encrypts the password and adds user-specific data based on their role."""

    # Hash Password
    hashed_password = encryption.encrypt_password(user_data.password)
    user_data.password = hashed_password

    # Teachers must have field value when they register
    if user_role == "teachers":
        if not user_data.subjects or len(user_data.subjects) == 0:
            raise HTTPException(status_code=422, detail="Missing subject field!")

    # Query the dB
    user_id = await crud.create_n_documents(
        collection=user_role, document_data=user_data.dict(), db=db
    )

    # Create a JWT token
    token = encryption.create_jwt_token(str(user_id), user_role)

    # Return response
    return {"token": token, "message": "User created successfully"}


@users.post("/signin")
@handle_mongodb_exceptions
async def signin(
    credentials: schemas.Signin,
    db: Database = Depends(get_db),
):
    # Find User

    user = await crud.get_user_by_email(credentials.role, credentials.email, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    if not encryption.check_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create a JWT
    token = encryption.create_jwt_token(str(user["_id"]), credentials.role)

    # Return the response
    return {
        "token": token,
        f"{Setup.id}": str(user["_id"]),
        f"{Setup.role}": credentials.role,
    }


@users.get("/")
@handle_mongodb_exceptions
async def read_user(
    db: Database = Depends(get_db),
    token_payload: dict = Depends(read_token_from_header),
) -> dict:
    """Retries a user from database without sensitive information"""

    user_id = token_payload[f"{Setup.id}"]
    user_role = token_payload[f"{Setup.role}"]

    # Query the dB

    user_data = await crud.read_n_documents(
        collection=user_role,
        user_id=user_id,
        sensitive_data=False,
        db=db,
    )
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found.")

    user_obj = schemas.GenericUser(**user_data)
    # Handle & Return response

    response = custom_types.UserFactory.create_user(user_role, user_obj)
    return response.dict()


def check_user_role_schema(
    user_role: str,
    update_data: dict,
    role_schema_map: dict = schemas.role_schema_map,
    _: str = Depends(oauth2_scheme),
):
    """Check if the update data matches the schema based on the user role."""

    # Mapping user roles to their respective schema

    # Validate update data against the role-specific schema
    if user_role not in role_schema_map or not schemas.check_keys_in_schema(
        role_schema_map[user_role], update_data
    ):
        return False

    return True


@users.patch("/change_password")
@handle_mongodb_exceptions
async def update_user_password(
    old_password: custom_types.Password,
    new_password: custom_types.Password,
    db: Database = Depends(get_db),
    token_payload: dict = Depends(read_token_from_header),
) -> dict:
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
            return {"message": "Password Changed succesfully"}
        else:
            raise HTTPException(status_code=410, detail="Password was NOT updated.")


@users.patch("/")
@handle_mongodb_exceptions
async def update_user(
    update_data: dict,
    db: Database = Depends(get_db),
    token_payload: dict = Depends(read_token_from_header),
) -> dict:
    """Update user data based on the user role."""
    # Extract user ID and role from the token payload
    user_id = token_payload[f"{Setup.id}"]
    user_role = token_payload[f"{Setup.role}"]

    # Check if the user data to be updated matches the schema for the user's role
    if not check_user_role_schema(
        user_role, update_data, role_schema_map=schemas.role_schema_update_map
    ):
        raise HTTPException(
            status_code=422, detail="The input keys do not match the Schema!"
        )

    if not schemas.check_not_null_values(update_data):
        raise HTTPException(
            status_code=422, detail="Input dictionary can't contain null values"
        )

    # Prepare the search query
    search_query = {"_id": ObjectId(user_id)}

    # Attempt to update the user data in the database
    result = await crud.update_n_documents(
        collection=user_role,
        search_query=search_query,
        update_data=update_data,
        db=db,
    )

    # Check if the update was successful
    if not result.modified_count == 1:
        raise HTTPException(status_code=400, detail="Fields have NOT been modified.")

    # Return a success response if the update is successful
    return {"status": "success", "detail": "Fields have been modified successfully"}


@users.delete("/")
@handle_mongodb_exceptions
async def delete_user(
    password: str,
    db: Database = Depends(get_db),
    token_payload: dict = Depends(read_token_from_header),
):
    """Delete a user after verifying their password."""
    # Extract user ID and role from the token payload
    user_id = token_payload[f"{Setup.id}"]
    user_role = token_payload[f"{Setup.role}"]

    # Retrieve the user data to verify the password

    user_data = await crud.read_n_documents(
        collection=user_role, user_id=user_id, db=db, sensitive_data=True
    )

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    # Check if the provided password matches the user's password
    if not encryption.check_password(password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Prepare the search query for deletion
    search_query = {"_id": ObjectId(user_id)}

    # Delete the user from the database
    deletion = await crud.delete_n_documents(
        collection=user_role, search_query=search_query, db=db
    )

    if not deletion:
        raise HTTPException(status_code=410, detail="Couldn't delete user")
    # Return a success response upon successful deletion
    return {"status": "success", "detail": "User was deleted successfully"}
