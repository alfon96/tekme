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


def get_kid_log_in_month(kid_name: str, month: int, year:int,  db: pymongo.database.Database):
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
