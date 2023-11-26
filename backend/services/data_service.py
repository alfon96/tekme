from crud import crud, queries
from schemas import schemas
from services import encryption
from fastapi import HTTPException
from db.db_handler import get_db
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Generator, AsyncGenerator, Any
from utils.setup import Setup


def get_collection_name(
    key_to_schema_map: str | dict,
) -> str:
    collection_name = (
        key_to_schema_map.value
        if not isinstance(key_to_schema_map, str)
        else key_to_schema_map
    )
    return collection_name


def prepare_query(search_query: str | dict, key_to_schema_map: str):
    isEncoded: bool = isinstance(search_query, str)

    if isEncoded:
        search_query = encryption.decode_query(query=search_query)

    return schemas.validate_query_over_schema(
        base_model=schemas.complete_schema_mapping[key_to_schema_map],
        query=search_query,
    )


async def read_service(
    search_query: str | dict,
    key_to_schema_map: schemas.complete_schema_mapping,
    db: AsyncGenerator[AsyncIOMotorDatabase, None],
    isSensitive: bool = False,
    is_user_query: bool = True,
    multi: bool = False,
    strict_mode: bool = False,
):
    # Decode and validate input query against exact user class

    search_query = prepare_query(
        search_query=search_query,
        key_to_schema_map=key_to_schema_map,
    )

    # Creates a query suitable for the mongodb driver
    pipeline = queries.get_read_query_for_mongo(
        is_user_query=is_user_query,
        search_query=search_query,
        sensitive_data=isSensitive,
        strict_mode=strict_mode,
    )

    result = await crud.read_n_documents(
        collection=get_collection_name(key_to_schema_map),
        pipeline=pipeline,
        db=db,
        multi=multi,
    )

    # Handle query results
    if not result:
        raise HTTPException(status_code=404, detail="Item NOT found.")

    # Return response
    return result


async def update_service(
    search_query: str | dict,
    update_query: dict,
    key_to_schema_map: schemas.complete_schema_mapping,
    db: AsyncGenerator[AsyncIOMotorDatabase, None],
    multi: bool = False,
):
    # Validate and decode(if needed) queries
    search_query = prepare_query(
        search_query=search_query,
        key_to_schema_map=key_to_schema_map,
    )

    update_query = schemas.validate_query_over_schema(
        base_model=schemas.complete_schema_mapping[key_to_schema_map],
        query=update_query,
    )

    # Transform queries for mongo db
    search_query_mongo, update_query_mongo = queries.get_update_query_for_mongo(
        search_query=search_query,
        update_data=update_query,
    )

    # Send query to dB
    result = await crud.update_n_documents(
        collection=get_collection_name(key_to_schema_map),
        search_query=search_query_mongo,
        update_query=update_query_mongo,
        multi=multi,
        db=db,
    )

    # Check if the update was successful
    if result.matched_count == 0:
        raise HTTPException(
            status_code=404, detail=f"No item found with {search_query}."
        )

    if result.modified_count < 1:
        raise HTTPException(
            status_code=200,
            detail="The dB was already up to date.",
        )

    # Return a success response if the update is successful
    return {
        "status": "Fields have been modified successfully",
        "count": result.modified_count,
    }


async def create_service(
    data: list | dict,
    key_to_schema_map: schemas.complete_schema_mapping,
    db: AsyncGenerator[AsyncIOMotorDatabase, None],
    transform_results: Any = None,
) -> str | list[str]:
    # Check if it is multi
    multi = isinstance(data, list)

    # Prepare the documents data
    document_data = [x.dict() for x in data] if multi else data.dict()

    # Transform query for mongodB
    document_data = queries.get_create_query_for_mongo(document=document_data)

    # Send Query to dB
    inserted_ids = await crud.create_n_documents(
        collection=key_to_schema_map,
        document_data=document_data,
        multi=multi,
        db=db,
    )

    # Handle Results Exceptions
    if not inserted_ids:
        raise HTTPException(status_code=500, detail="Creation was NOT successful")

    if multi:
        result = [str(id) for id in inserted_ids]
    else:
        result = str(inserted_ids)

    # You may want to format data differently in different endpoints
    if transform_results:
        result = transform_results(result)

    return result


async def delete_service(
    search_query: str | dict,
    key_to_schema_map: schemas.complete_schema_mapping,
    db: AsyncGenerator[AsyncIOMotorDatabase, None],
    multi: bool = False,
):
    # Prepare the search query for deletion
    search_query = prepare_query(
        search_query=search_query,
        key_to_schema_map=key_to_schema_map,
    )
    # Transform the query for mongo dB
    search_query_for_mongo = queries.get_delete_query_for_mongo(search_query)

    # Delete the user from the database
    result = await crud.delete_n_documents(
        collection=get_collection_name(key_to_schema_map),
        search_query=search_query_for_mongo,
        db=db,
        multi=multi,
    )

    # Handle results
    if result.deleted_count < 1:
        raise HTTPException(status_code=410, detail="Deletion Failed")
    # Return a success response upon successful deletion
    return {
        "status": "Item deleted successfully",
        "count": result.deleted_count,
    }
