from bson import ObjectId
from datetime import datetime, date, timedelta
from utils.setup import Setup
from schemas import schemas
from services import data_service
import re


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

        elif f"_{Setup.id}" in x:
            # Converts the id or ids in objectId
            mongo_db_query[x] = convert_id_to_object_id(y)

        else:
            mongo_db_query[x] = y

    return mongo_db_query


def convert_id_to_object_id(value) -> ObjectId | list[ObjectId]:
    # If there are fields that end with _id,
    # it means these refer to other collection documents,
    # thus we need to use the objectId type for other queries.
    if isinstance(value, list):
        # if y is a list all its element must be converted to objectId
        return [ObjectId(id) for id in value]
    else:
        return ObjectId(value)


def check_creation_query(data: dict):
    transformed_data = {}
    for x, y in data.items():
        # Don't copy the id if its present
        if x == f"{Setup.id}":
            continue

        if f"_{Setup.id}" in x:
            transformed_data[x] = convert_id_to_object_id(y)
        else:
            transformed_data[x] = y

    return transformed_data


def get_create_query_for_mongo(document: dict | list[dict]) -> dict | list:
    if isinstance(document, list):
        document = [check_creation_query(x) for x in document]
    else:
        document = check_creation_query(document)

    return document


def generate_lookup_stages(key_to_schema_map: str, pattern: str):
    """
    Generates lookup stages for an aggregation pipeline.
    """
    base_class_fields = schemas.complete_schema_mapping[key_to_schema_map].__fields__
    return [
        {
            "$lookup": {
                "from": field[:-3],
                "localField": field,
                "foreignField": "_id",
                "as": f"{field[:-3]}_details",
            }
        }
        for field in base_class_fields
        if re.match(pattern, field)
    ]


def generate_set_stages(key_to_schema_map: str, pattern: str):
    """
    Generates set stages to process lookup results in an aggregation pipeline.
    """
    base_class_fields = schemas.complete_schema_mapping[key_to_schema_map].__fields__
    sensitive_fields = set(schemas.UserSensitiveData.__fields__.keys())
    base_fields = set(schemas.UserBase.__fields__.keys())
    fields_to_exclude = sensitive_fields - base_fields
    return [
        {
            "$set": {
                f"{field[:-3]}_details": {
                    "$map": {
                        "input": f"${field[:-3]}_details",
                        "as": "item",
                        "in": {
                            "$mergeObjects": [
                                {"id": {"$toString": "$$item._id"}},
                                {
                                    k: "$$item." + k
                                    for k in schemas.complete_schema_mapping[
                                        field[:-3]
                                    ].__fields__
                                    if k not in fields_to_exclude and k != "_id"
                                },
                            ]
                        },
                    }
                }
            }
        }
        for field in base_class_fields
        if re.match(pattern, field)
    ]


def get_lookup_query(key_to_schema_map: str) -> list | None:
    """
    Generates a complete lookup query for an aggregation pipeline.
    """
    pattern = r".*[^_]_id$"
    lookup_stages = generate_lookup_stages(key_to_schema_map, pattern)
    if len(lookup_stages) == 0:
        return None

    set_stages = generate_set_stages(key_to_schema_map, pattern)

    # Remove original id fields
    unset_stages = [
        {
            "$unset": [
                field
                for field in schemas.complete_schema_mapping[
                    key_to_schema_map
                ].__fields__
                if re.match(pattern, field)
            ]
        }
    ]

    return lookup_stages + unset_stages + set_stages


def get_read_query_for_mongo(
    search_query: dict = {},
    sensitive_data: bool = False,
    is_user_query: bool = True,
    strict_mode: bool = False,
    key_to_schema_map: str = "",
):
    search_query = transform_data_types_for_mongodb(
        query=search_query,
        isSearching=True,
        strict_mode=strict_mode,
    )

    set_query = convert_id_to_str(key_to_schema_map=key_to_schema_map, just_id=True)
    lookup_query = get_lookup_query(key_to_schema_map)

    projections = {"_id": 0}
    if not sensitive_data and is_user_query:
        projections.update({"password": 0, "phone": 0})

    pipeline = [
        {"$match": search_query},
        {"$set": set_query},
        {"$project": projections},
    ]

    if lookup_query:
        pipeline.extend(lookup_query)

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


def convert_id_to_str(
    key_to_schema_map: str,
    just_id: bool = False,
):
    if just_id:
        return {"id": {"$toString": "$_id"}}
    base_class_fields = schemas.complete_schema_mapping[key_to_schema_map].__fields__
    # Find all the fields that have_id in the name and setup the query for mongodb to convert in string.
    project_fields = {
        field: {
            "$map": {
                "input": f"${field}",
                "as": "temp_id",
                "in": {"$toString": "$$temp_id"},
            }
        }
        for field in base_class_fields
        if "_id" in field
    }
    # Additonally in mongo db every document will have an id that needs to be renamed and converted.
    project = {"id": {"$toString": "$_id"}, **project_fields}
    return project
