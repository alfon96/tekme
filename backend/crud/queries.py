from bson import ObjectId
from datetime import datetime, date, timedelta
from utils.setup import Setup


def transform_data_types_for_mongodb(
    query: dict = {},
    isSearching: bool = True,
    strict_mode: bool = False,
) -> dict:
    mongo_db_query = {}

    for x, y in query.items():
        if isinstance(y, list) and isSearching and not strict_mode:
            mongo_db_query[x] = {"$in": [z for z in y]}

        elif isinstance(y, datetime) and isSearching:
            mongo_db_query[x] = {"$gte": y, "$lt": y + timedelta(days=1)}

        elif isinstance(y, date):
            birthday_datetime: datetime = datetime(y.year, y.month, y.day)
            if isSearching:
                mongo_db_query[x] = {
                    "$gte": birthday_datetime,
                    "$lt": birthday_datetime + timedelta(days=1),
                }
            else:
                mongo_db_query[x] = birthday_datetime

        elif x == f"{Setup.id}":
            mongo_db_query["_id"] = ObjectId(y)
        else:
            mongo_db_query[x] = y

    return mongo_db_query


def get_create_query_for_mongo(document: dict | list[dict]) -> dict | list:
    if isinstance(document, list):
        for x in document:
            if f"{Setup.id}" in x.keys():
                del x[f"{Setup.id}"]
    else:
        if f"{Setup.id}" in document.keys():
            del document[f"{Setup.id}"]

    return document


def get_read_query_for_mongo(
    search_query: dict = {},
    sensitive_data: bool = False,
    is_user_query: bool = True,
    strict_mode: bool = False,
):
    search_query = transform_data_types_for_mongodb(
        query=search_query,
        isSearching=True,
        strict_mode=strict_mode,
    )

    projections = {"_id": 0}
    if not sensitive_data and is_user_query:
        projections.update({"password": 0, "phone": 0})

    pipeline = [
        {"$match": search_query},
        {"$set": {"id": {"$toString": "$_id"}}},
        {"$project": projections},
    ]

    return pipeline


def get_update_query_for_mongo(
    search_query: dict = {},
    update_data: dict = {},
) -> (dict, dict):
    search_query = transform_data_types_for_mongodb(search_query)
    update_query = {
        "$set": transform_data_types_for_mongodb(update_data, isSearching=False)
    }

    return search_query, update_query


def get_delete_query_for_mongo(
    search_query: dict = {},
):
    search_query = transform_data_types_for_mongodb(search_query)
    return search_query
