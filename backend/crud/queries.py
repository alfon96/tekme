from bson import ObjectId
from datetime import datetime, date, timedelta
from utils.setup import Setup


def transform_data_types_for_mongodb(query: dict = {}, user_id: str = None):
    for x, y in query.items():
        if isinstance(y, datetime):
            query[x] = {"$gte": y, "$lt": y + timedelta(days=1)}

        if isinstance(y, date):
            birthday_datetime: datetime = datetime(y.year, y.month, y.day)
            query[x] = {
                "$gte": birthday_datetime,
                "$lt": birthday_datetime + timedelta(days=1),
            }

    if user_id:
        query.update({"_id": ObjectId(user_id)})

    return query


def get_create_query_for_mongo(document: dict = {}) -> dict:
    if "id" in document.keys():
        del document["id"]

    return document


def get_read_query_for_mongo(
    search_query: dict = {},
    user_id: str = None,
    sensitive_data: bool = False,
):
    search_query = transform_data_types_for_mongodb(search_query, user_id)

    projections = {"_id": 0}
    if not sensitive_data:
        projections.update({"password": 0, "phone": 0})

    pipeline = [
        {"$match": search_query},
        {"$set": {"id": {"$toString": "$_id"}}},
        {"$project": projections},
    ]

    return pipeline


def get_update_query_for_mongo(
    user_id: str = "",
    search_query: dict = {},
    update_data: dict = {},
) -> (dict, dict):
    search_query = transform_data_types_for_mongodb(search_query, user_id)
    update_query = {"$set": transform_data_types_for_mongodb(update_data)}

    return search_query, update_query
