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
    collection: str, user_id: str, db: AsyncIOMotorDatabase, sensitive_data=False
) -> Union[
    schemas.StudentBase,
    schemas.StudentSensitiveData,
    schemas.TeacherBase,
    schemas.TeacherSensitiveData,
    schemas.RelativeBase,
    schemas.RelativeSensitiveData,
]:
    """Read a user's data from the specified collection."""

    query = {"_id": ObjectId(user_id)}
    if not sensitive_data:
        query.update({"password": 0, "phone": 0, "email": 0})

    user_data = await db[collection].find_one(query)
    if not user_data:
        raise ValueError(f"The id {user_id} does not correspond to any user!")

    return user_data


@handle_pymongo_exceptions
async def read_n_documents(
    collection: str, search_query: dict, db: AsyncIOMotorDatabase, multi: bool = False
) -> list[Union[schemas.ClassWithId, schemas.ClassBase]]:
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
        return await cursor.to_list(length=1)


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
        result = await db[collection].update_many(search_query, update_query)
    else:
        result = await db[collection].update_one(search_query, update_query)

    return result.modified_count


@handle_pymongo_exceptions
async def delete_n_documents(
    collection: str, search_query: dict, db: AsyncIOMotorDatabase, multi: bool = False
) -> None:
    """
    Create a new user in the right collection.
    """

    deleted = None
    if multi:
        deleted = await db[collection].delete_many(search_query)
    else:
        deleted = await db[collection].delete_one(search_query)

    if not deleted:
        raise HTTPException(status_code=410, detail="Deletion NOT performed")


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
