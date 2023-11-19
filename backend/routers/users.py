from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Union
from schemas import schemas
from crud import crud
from pymongo.database import Database
from utils import encryption
from db.db_handler import get_db
from pymongo import errors as pymongo_errors
from utils.setup import Setup
from bson import ObjectId
from utils.decorators import handle_mongodb_exceptions

users = APIRouter(prefix="/users", tags=["Users"])


@users.post("/signup")
@handle_mongodb_exceptions
async def signup(
    user_data: schemas.Signup,
    subjects: Optional[list[str]] = [],
    details: Optional[list[str]] = [],
    db: Database = Depends(get_db),
):
    """Register a new user. Encrypts the password and adds user-specific data based on their role."""

    # Hash Password
    hashed_password = encryption.encrypt_password(user_data.password)
    user_data.password = hashed_password

    user_role = user_data.role
    new_user = {**user_data.dict()}

    # Teachers must have field value when they register
    if user_role == "teachers":
        if len(subjects) == 0:
            raise HTTPException(status_code=422, detail="Missing subject field!")
        new_user["subjects"] = subjects

    # Student can have empty details
    elif user_role == "students":
        new_user["details"] = details

    # Query the dB
    user_id = await crud.create_user(user_data.role, new_user, db)

    # Create a JWT token
    token = encryption.create_jwt_token(str(user_id), user_data.role)

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
    token_payolad: dict = Depends(encryption.read_token),
    db: Database = Depends(get_db),
) -> Union[schemas.RelativeBase, schemas.StudentBase, schemas.TeacherBase]:
    """Retries a user from database without sensitive information"""

    user_id = token_payolad[f"{Setup.id}"]
    user_role = token_payolad[f"{Setup.role}"]

    # Query the dB
    user_data = await crud.read_user(user_role, user_id, db)

    # Handle & Return response
    if user_role == schemas.User.TEACHER:
        return schemas.TeacherBase(**user_data)
    elif user_role == schemas.User.STUDENT:
        return schemas.StudentBase(**user_data)
    elif user_role == schemas.User.RELATIVE:
        return schemas.RelativeBase(**user_data)
    else:
        raise HTTPException(status_code=404, detail="User role not found")


def check_user_role_schema(user_role: str, update_data: dict):
    """Check if the update data matches the schema based on the user role."""

    # Mapping user roles to their respective schema
    role_schema_map = {
        schemas.User.TEACHER: schemas.TeacherSensitiveData,
        schemas.User.STUDENT: schemas.StudentSensitiveData,
        schemas.User.RELATIVE: schemas.RelativeSensitiveData,
    }

    # Validate update data against the role-specific schema
    if user_role not in role_schema_map or not schemas.check_keys_in_schema(
        role_schema_map[user_role], update_data
    ):
        raise HTTPException(
            status_code=400,
            detail=f"The input keys do not match with the {user_role} schema!",
        )


@users.patch("/")
@handle_mongodb_exceptions
async def update_user(
    update_data: dict,
    token_payload: dict = Depends(encryption.read_token),
    db: Database = Depends(get_db),
):
    """Update user data based on the user role."""
    # Extract user ID and role from the token payload
    user_id = token_payload[f"{Setup.id}"]
    user_role = token_payload[f"{Setup.role}"]

    # Check if the user data to be updated matches the schema for the user's role
    check_user_role_schema(user_role, update_data)

    # Prepare the search query
    search_query = {"_id": ObjectId(user_id)}

    # Attempt to update the user data in the database
    modified = await crud.update_n_documents(
        collection=user_role,
        search_query=search_query,
        update_data=update_data,
        db=db,
    )

    # Check if the update was successful
    if not modified == 1:
        raise HTTPException(status_code=400, detail="Fields have NOT been modified.")

    # Return a success response if the update is successful
    return {"status": "success", "detail": "Fields have been modified successfully"}


@users.delete("/")
@handle_mongodb_exceptions
async def delete_user(
    password: str,
    token_payload: dict = Depends(encryption.read_token),
    db: Database = Depends(get_db),
):
    """Delete a user after verifying their password."""
    # Extract user ID and role from the token payload
    user_id = token_payload[f"{Setup.id}"]
    user_role = token_payload[f"{Setup.role}"]

    # Retrieve the user data to verify the password
    user_data = await crud.read_user(user_role, user_id, db, sensitive_data=True)

    # Check if the provided password matches the user's password
    if not encryption.check_password(password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Prepare the search query for deletion
    search_query = {"_id": ObjectId(user_id)}

    # Delete the user from the database
    await crud.delete_n_documents(
        collection=user_role, search_query=search_query, db=db
    )

    # Return a success response upon successful deletion
    return {"status": "success", "detail": "User was deleted successfully"}
