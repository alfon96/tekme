from schemas import schemas, custom_types
from bson import ObjectId, json_util
from typing import Union
import pymongo
from schemas import schemas, custom_types
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
    pipeline: list = None,
    multi: bool = False,
) -> Union[dict, list]:
    """
    Read one or multiple documents from the specified collection.
    Can be used to read a specific user or perform a general query.
    """
    cursor = db[collection].aggregate(pipeline)
    if multi:
        return await cursor.to_list(length=None)
    else:
        try:
            documents = await cursor.to_list(length=1)
            return documents[0] if documents else None
        except Exception as e:
            raise e


async def update_n_documents(
    collection: str,
    search_query: dict,
    update_query: dict,
    db: AsyncIOMotorDatabase,
    multi: bool = False,
) -> int:
    """
    Update an existing user in the right collection.
    """

    if multi:
        return await db[collection].update_many(search_query, update_query)
    else:
        try:
            return await db[collection].update_one(search_query, update_query)
        except Exception as e:
            raise e


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
