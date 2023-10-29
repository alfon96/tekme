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


def get_kid_log_in_month(kid_name: str, month: int, db: pymongo.database.Database):
    try:
        collection = db.get_collection("Kids")

        end_month = month + 1
        end_year = 2023
        if month == 12:
            end_month = 1
            end_year = 2024

        search_query = {
            "name": kid_name,
            "date": {
                "$gte": datetime(2023, month, 1),
                "$lt": datetime(end_year, end_month, 1),
            },
        }

        results = collection.find(search_query).sort("date", pymongo.ASCENDING)

        return [{**document, "_id": str(document["_id"])} for document in results]

    except Exception as e:
        print(e)
        return False
