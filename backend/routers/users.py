from fastapi import APIRouter, HTTPException, Depends, Body
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
from pydantic import TypeAdapter
import json
from crud import queries

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


def decode_and_validate_query(query: str) -> dict:
    try:
        # decode Query
        decoded_query = encryption.decode_query(query)

        return schemas.validate_query_over_schema(
            base_model=schemas.UserBase,
            query=decoded_query,
        )

    except Exception as e:
        raise e


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

    document_data = queries.get_create_query_for_mongo(user_data.dict())
    # Query the dB
    user_id = await crud.create_n_documents(
        collection=user_role, document_data=document_data, db=db
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


@users.get("/search")
@handle_mongodb_exceptions
async def read_other_user(
    role: schemas.User,
    search_query: dict = Depends(decode_and_validate_query),
    db: Database = Depends(get_db),
    _: dict = Depends(read_token_from_header_factory()),
) -> dict:
    """Retries a user from database without sensitive information"""

    pipeline = queries.get_read_query_for_mongo(search_query)
    user_data = await crud.read_n_documents(
        collection=role,
        pipeline=pipeline,
        db=db,
    )
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found.")

    # Handle & Return response

    response = schemas.UserFactory.create_user(role, user_data)
    return response.dict()


@users.get("/")
@handle_mongodb_exceptions
async def read_user(
    db: Database = Depends(get_db),
    token_payload: dict = Depends(read_token_from_header_factory()),
) -> dict:
    """Retries a user from database without sensitive information"""

    user_id = token_payload[f"{Setup.id}"]
    user_role = token_payload[f"{Setup.role}"]
    search_query = {f"{Setup.id}": user_id}

    # Query the dB
    pipeline = queries.get_read_query_for_mongo(
        search_query=search_query,
        sensitive_data=False,
    )
    user_data = await crud.read_n_documents(
        collection=user_role,
        pipeline=pipeline,
        multi=False,
        db=db,
    )
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found.")

    # Handle & Return response

    response = schemas.UserFactory.create_user(user_role, user_data)
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
    update_data: dict,
    db: Database = Depends(get_db),
    token_payload: dict = Depends(read_token_from_header_factory()),
) -> dict:
    """Update user data based on the user role."""
    # Extract user ID and role from the token payload
    user_id = token_payload[f"{Setup.id}"]
    user_role = token_payload[f"{Setup.role}"]

    update_data = schemas.validate_query_over_schema(
        base_model=schemas.role_schema_update_map[user_role],
        query=update_data,
    )

    search_query = {f"{Setup.id}": user_id}

    search_query_mongo, update_query_mongo = queries.get_update_query_for_mongo(
        search_query=search_query,
        update_data=update_data,
    )
    # Attempt to update the user data in the database
    result = await crud.update_n_documents(
        collection=user_role,
        search_query=search_query_mongo,
        update_query=update_query_mongo,
        db=db,
    )

    # Check if the update was successful
    if result.matched_count == 0:
        raise HTTPException(
            status_code=404, detail=f"No user found with id '{user_id}'."
        )

    if result.modified_count < 1:
        raise HTTPException(
            status_code=200,
            detail="New information was already found in the dB, no modifications were done.",
        )

    # Return a success response if the update is successful
    return {"detail": "Fields have been modified successfully"}


@users.patch("/admin_update")
@handle_mongodb_exceptions
async def update_other_user(
    id: str,
    role: schemas.User,
    update_data: dict,
    db: Database = Depends(get_db),
    _: dict = Depends(
        read_token_from_header_factory(
            roles=[
                schemas.User.ADMIN,
            ]
        )
    ),
) -> dict:
    """Update user data based on the user role."""

    # select only fields that can be edited by admin
    editable_schema_subset = schemas.find_unique_fields(
        base_class=schemas.UserBase, sub_class=schemas.role_schema_update_map[role]
    )

    schemas.validate_query_over_schema(
        base_model=editable_schema_subset,
        query=update_data,
    )

    search_query = {f"{Setup.id}": id}

    search_query_mongo, update_query_mongo = queries.get_update_query_for_mongo(
        search_query=search_query,
        update_data=update_data,
    )
    # Attempt to update the user data in the database
    result = await crud.update_n_documents(
        collection=role,
        search_query=search_query_mongo,
        update_query=update_query_mongo,
        db=db,
    )

    # Check if the update was successful
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"No user found with id '{id}'.")

    if result.modified_count < 1:
        raise HTTPException(
            status_code=200,
            detail="New information was already found in the dB, no modifications were done.",
        )

    # Return a success response if the update is successful
    return {"detail": "Fields have been modified successfully"}


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

    # Retrieve the user data to verify the password
    search_query = {f"{Setup.id}": user_id}
    pipeline = queries.get_read_query_for_mongo(
        search_query=search_query,
        sensitive_data=True,
    )

    user_data = await crud.read_n_documents(
        collection=user_role,
        pipeline=pipeline,
        multi=False,
        db=db,
    )

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    # Check if the provided password matches the user's password
    if not encryption.check_password(password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Prepare the search query for deletion

    search_query_for_mongo = queries.get_delete_query_for_mongo(search_query)

    # Delete the user from the database
    result = await crud.delete_n_documents(
        collection=user_role, search_query=search_query_for_mongo, db=db
    )

    if result.deleted_count < 1:
        raise HTTPException(status_code=410, detail="Couldn't delete user")
    # Return a success response upon successful deletion
    return {"status": "success", "detail": "User was deleted successfully"}


@users.delete("/{user_id}")
@handle_mongodb_exceptions
async def delete_other_user(
    user_id: str,
    user_role: schemas.User,
    db: Database = Depends(get_db),
    _: str = Depends(
        read_token_from_header_factory(
            roles=[
                schemas.User.ADMIN,
            ]
        )
    ),
):
    """Delete a user after verifying their password."""

    # The admins can remove any user

    # Prepare the search query for deletion
    search_query = queries.get_delete_query_for_mongo(user_id)

    # Delete the user from the database
    deletion = await crud.delete_n_documents(
        collection=user_role, search_query=search_query, db=db
    )

    if not deletion:
        raise HTTPException(status_code=410, detail="Couldn't delete user")
    # Return a success response upon successful deletion
    return {"status": "success", "detail": "User was deleted successfully"}
