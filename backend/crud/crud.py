from schemas import schemas
from bson import ObjectId, json_util
from typing import Union
import pymongo
from schemas import schemas
from datetime import datetime
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase


async def create_document(
    document_data: dict,
    collection: str,
    db: AsyncIOMotorDatabase,
):
    """Create a document inside a collection."""
    try:
        result = await db[collection].insert_one(document_data)
        return result.inserted_id
    except Exception as e:
        raise Exception(f"An error occurred while inserting the student: {e}")


async def create_user(
    collection: str,
    user_data: dict,
    db: AsyncIOMotorDatabase,
):
    """
    Create a new user in the right collection.
    """
    try:
        new_user = await db[collection].insert_one(user_data)
        return new_user.inserted_id
    except Exception as e:
        raise e


async def read_user(
    collection: str, user_id: str, db: AsyncIOMotorDatabase, sensitive_data=False
):
    """
    Create a new user in the right collection.
    """
    try:
        query = {"_id": ObjectId(user_id)}
        if not sensitive_data:
            query.update({"password": 0, "phone": 0, "email": 0})

        user_data = await db[collection].find_one(query)
        if not user_data:
            raise ValueError(f"The id {user_id} does not correspond to any user!")

        return user_data
    except Exception as e:
        raise e


async def update_document(
    collection: str,
    document_id: str,
    update_data: dict,
    db: AsyncIOMotorDatabase,
):
    """
    Update an existing user in the right collection.
    """
    try:
        search_query = {"_id": ObjectId(document_id)}
        update_query = {"$set": update_data}

        result = await db[collection].update_one(search_query, update_query)

        return result.modified_count

    except Exception as e:
        raise e


async def delete_document(
    collection: str,
    document_id: str,
    db: AsyncIOMotorDatabase,
):
    """
    Create a new user in the right collection.
    """
    try:
        query = {"_id": ObjectId(document_id)}
        deleted = await db[collection].delete_one(query)
        if deleted.deleted_count > 0:
            return deleted.acknowledged
        else:
            raise HTTPException(
                status_code=500, detail="Deletion NOT performed, server error."
            )
    except Exception as e:
        raise e


def get_user_by_phone(
    collection: str,
    phone: str,
    db: AsyncIOMotorDatabase,
):
    """
    Fetch a user by email from a given collection.
    """
    try:
        user_data = db[collection].find_one({"phone": phone})
        return user_data
    except Exception as e:
        raise e


async def get_user_by_email(
    collection: str,
    email: str,
    db: AsyncIOMotorDatabase,
):
    """
    Fetch a user by email from a role-specific collection.
    """
    try:
        user_data = await db[collection].find_one({"email": email})
        return user_data
    except Exception as e:
        raise e


def delete_user_by_id(
    collection: str,
    user_id: str,
    db: AsyncIOMotorDatabase,
):
    """
    Delete a user by ID from a role-specific collection.
    """
    result = db[collection].delete_one({"_id": user_id})
    return result.deleted_count > 0


def get_class_by_name(
    class_name: str,
    class_grade: int,
    db: AsyncIOMotorDatabase,
):
    """
    Fetch a class by name.
    """
    try:
        class_data = db[schemas.CLASSES_COLLECTION].find_one(
            {"name": class_name, "grade": class_grade}
        )
        return class_data
    except Exception as e:
        raise e
