from schemas import schemas
from bson import ObjectId, json_util
from typing import Union
import pymongo
from schemas import schemas
from datetime import datetime
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase


def handle_pymongo_exceptions(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except pymongo.errors.PyMongoError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An unexpected error occurred: {e}"
            )

    return wrapper


@handle_pymongo_exceptions
async def create_user(
    collection: str,
    user_data: dict,
    db: AsyncIOMotorDatabase,
) -> ObjectId:
    """Create a new user in the specified collection."""

    new_user = await db[collection].insert_one(user_data)
    return new_user.inserted_id


@handle_pymongo_exceptions
async def create_n_documents(
    document_data: Union[dict, list],
    collection: str,
    db: AsyncIOMotorDatabase,
    multi: bool = False,
) -> Union[ObjectId, list[ObjectId]]:
    """Create one or multiple documents in a collection."""

    if multi:
        result = await db[collection].insert_many(document_data)
        return result.inserted_ids
    else:
        result = await db[collection].insert_one(document_data)
        return result.inserted_id


@handle_pymongo_exceptions
async def read_user(
    collection: str,
    user_id: str,
    db: AsyncIOMotorDatabase,
    sensitive_data: bool = False,
) -> Union[
    schemas.StudentBase,
    schemas.StudentSensitiveData,
    schemas.TeacherBase,
    schemas.TeacherSensitiveData,
    schemas.RelativeBase,
    schemas.RelativeSensitiveData,
    None,
]:
    """Read a user's data from the specified collection."""

    match = {"$match": {"_id": ObjectId(user_id)}}

    # Rimuovi o modifica i campi specifici
    modify_fields = {
        "$set": {
            "_id": {"$toString": "$_id"},
            "password": {
                "$cond": {"if": sensitive_data, "then": "$password", "else": "$$REMOVE"}
            },
            "phone": {
                "$cond": {"if": sensitive_data, "then": "$phone", "else": "$$REMOVE"}
            },
            "email": {
                "$cond": {"if": sensitive_data, "then": "$email", "else": "$$REMOVE"}
            },
        }
    }

    pipeline = [match, modify_fields]

    cursor = db[collection].aggregate(pipeline)
    user_data = await cursor.to_list(length=1)
    return user_data[0] if user_data else None


@handle_pymongo_exceptions
async def read_n_documents(
    collection: str, search_query: dict, db: AsyncIOMotorDatabase, multi: bool = False
) -> Union[schemas.ClassBase, list[schemas.ClassBase]]:
    """
    Create a new user in the right collection.
    """

    pipeline = [
        {"$match": search_query},
        {"$addFields": {"_id": {"$toString": "$_id"}}},
    ]
    if multi:
        cursor = db[collection].aggregate(pipeline)
        return await cursor.to_list(length=None)
    else:
        cursor = db[collection].aggregate(pipeline)
        data = await cursor.to_list(length=1)
        return data[0]


@handle_pymongo_exceptions
async def update_n_documents(
    collection: str,
    search_query: dict,
    update_data: dict,
    db: AsyncIOMotorDatabase,
    multi: bool = False,
) -> int:
    """
    Update an existing user in the right collection.
    """

    update_query = {"$set": update_data}
    if multi:
        return await db[collection].update_many(search_query, update_query)
    else:
        return await db[collection].update_one(search_query, update_query)



@handle_pymongo_exceptions
async def delete_n_documents(
    collection: str, search_query: dict, db: AsyncIOMotorDatabase, multi: bool = False
) -> None:
    """
    Create a new user in the right collection.
    """

    if multi:
        return await db[collection].delete_many(search_query)
    else:
        return await db[collection].delete_one(search_query)


@handle_pymongo_exceptions
async def get_user_by_email(
    collection: str,
    email: str,
    db: AsyncIOMotorDatabase,
) -> Union[
    schemas.StudentBase,
    schemas.StudentSensitiveData,
    schemas.TeacherBase,
    schemas.TeacherSensitiveData,
    schemas.RelativeBase,
    schemas.RelativeSensitiveData,
]:
    """
    Fetch a user by email from a role-specific collection.
    """

    user_data = await db[collection].find_one({"email": email})
    return user_data


@handle_pymongo_exceptions
async def get_user_by_email(
    collection: str,
    user_id: str,
    db: AsyncIOMotorDatabase,
) -> Union[
    schemas.StudentBase,
    schemas.StudentSensitiveData,
    schemas.TeacherBase,
    schemas.TeacherSensitiveData,
    schemas.RelativeBase,
    schemas.RelativeSensitiveData,
]:
    """
    Fetch a user by email from a role-specific collection.
    """
    _id = ObjectId(user_id)
    user_data = await db[collection].find_one({"_id": _id})
    return user_data
