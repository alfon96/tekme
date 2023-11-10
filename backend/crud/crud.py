from schemas import schemas
from bson import ObjectId, json_util
from typing import Union
import pymongo
from datetime import datetime


def save_kid_log(
    kid_log: schemas.KidLog, db: pymongo.database.Database
) -> Union[ObjectId, bool]:
    try:
        collection = db.get_collection("Kids")
        result = collection.insert_one(kid_log.model_dump())
        return str(result.inserted_id)
    except Exception as e:
        print(e)
        return False


def get_kid_log_in_month(
    kid_name: str, month: int, year: int, db: pymongo.database.Database
):
    try:
        collection = db.get_collection("Kids")

        next_month = month + 1
        query_year = year

        if month == 12:
            next_month = 1
            query_year += 1

        search_query = {
            "name": kid_name,
            "date": {
                "$gte": datetime(query_year, month, 1),
                "$lt": datetime(query_year, next_month, 1),
            },
        }

        results = collection.find(search_query).sort("date", pymongo.ASCENDING)

        return [{**document, "_id": str(document["_id"])} for document in results]

    except Exception as e:
        print(e)
        return False


def get_collection(role: str, db: pymongo.database.Database):
    """
    Fetch a collection based on the user's role.

    :param role: The role of the user (e.g., 'Student', 'Teacher', 'Parent', 'Administrator').
    :return: The collection associated with the role.
    """
    # Verifica che il ruolo sia uno di quelli supportati
    valid_roles = ["Students", "Teachers", "Parents", "Administrator"]
    if role not in valid_roles:
        raise ValueError(f"Invalid role: {role}")

    return db[role]


def create_user(role: str, user_data: dict, db: pymongo.database.Database):
    """
    Create a new user in a role-specific collection.
    """
    collection = get_collection(role, db)
    return collection.insert_one(user_data)


def get_user_by_phone(role: str, phone: str, db: pymongo.database.Database):
    """
    Fetch a user by email from a role-specific collection.
    """
    collection = get_collection(role, db)
    return collection.find_one({"phone": phone})


def get_user_by_email(role: str, email: str, db: pymongo.database.Database):
    """
    Fetch a user by email from a role-specific collection.
    """
    collection = get_collection(role, db)
    return collection.find_one({"email": email})


def delete_user_by_id(role: str, user_id: str, db: pymongo.database.Database):
    """
    Delete a user by ID from a role-specific collection.
    """
    collection = get_collection(role, db)
    result = collection.delete_one({"_id": user_id})
    return result.deleted_count > 0
