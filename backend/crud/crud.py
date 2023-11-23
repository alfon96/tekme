from schemas import schemas
from bson import ObjectId, json_util
from typing import Union
import pymongo
from schemas import schemas
from datetime import datetime
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase


# BASIC CRUD OPERATIONS


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
        try:
            result = await db[collection].insert_one(document_data)
        except Exception as e:
            print(e)
        return result.inserted_id


async def read_n_documents(
    collection: str,
    db: AsyncIOMotorDatabase,
    user_id: str = None,
    search_query: dict = None,
    sensitive_data: bool = False,
    multi: bool = False,
) -> Union[dict, list]:
    """
    Read one or multiple documents from the specified collection.
    Can be used to read a specific user or perform a general query.
    """

    # Determine the match condition based on user_id or search_query
    set_condition = {
        "id": {"$toString": "$_id"},
    }

    if user_id:
        match_condition = {"_id": ObjectId(user_id)}
        set_condition.update(
            {
                "password": {
                    "$cond": {
                        "if": sensitive_data,
                        "then": "$password",
                        "else": "$$REMOVE",
                    }
                },
                "phone": {
                    "$cond": {
                        "if": sensitive_data,
                        "then": "$phone",
                        "else": "$$REMOVE",
                    }
                },
                "email": {
                    "$cond": {
                        "if": sensitive_data,
                        "then": "$email",
                        "else": "$$REMOVE",
                    }
                },
            }
        )
    else:
        match_condition = search_query or {}

    pipeline = [
        {"$match": match_condition},
        {"$set": set_condition},
        {"$project": {"_id": 0}},  # Rimuovi solo il campo '_id' originale
    ]

    cursor = db[collection].aggregate(pipeline)
    if multi:
        return await cursor.to_list(length=None)
    else:
        documents = await cursor.to_list(length=1)
        return documents[0] if documents else None


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
