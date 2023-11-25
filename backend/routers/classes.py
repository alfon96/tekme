from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Optional, Union
from schemas import schemas, custom_types
from crud import crud
from pymongo.database import Database
from utils import encryption
from db.db_handler import get_db
from pymongo import errors as pymongo_errors
from utils.setup import Setup
import json
from utils.decorators import handle_mongodb_exceptions
from routers.users import read_token_from_header_factory
from pydantic import BaseModel

classes = APIRouter(prefix="/classes", tags=["Classes"])


@classes.post("/")
@handle_mongodb_exceptions
async def create_n_classes(
    classes: Union[schemas.ClassBase, list[schemas.ClassBase]],
    db: Database = Depends(get_db),
    token: str = Depends(read_token_from_header_factory),
):
    """Create one or multiple class records. Accepts either a single class object or a list of class objects."""

    # Check if it is multi
    multi = isinstance(classes, list)
    # Prepare the documents data
    document_data = [x.dict() for x in classes] if multi else classes.dict()

    # Send Query to dB
    inserted_ids = await crud.create_n_documents(
        collection=schemas.Data.CLASS.value,
        document_data=document_data,
        multi=multi,
        db=db,
    )
    # Handle Results Exceptions
    if not inserted_ids:
        raise HTTPException(status_code=500, detail="Creation was NOT successful")

    # Prepare Response
    if multi:
        response = [
            {**schemas.ClassBase(**{**obj_.dict(), "id": str(id_)}).dict()}
            for obj_, id_ in zip(classes, inserted_ids)
        ]
    else:
        response = {
            **schemas.ClassBase(**{**classes.dict(), "id": str(inserted_ids)}).dict()
        }

    # Send Response
    return response


@classes.get("/")
@handle_mongodb_exceptions
async def read_n_classes(
    name: str,
    grade: int,
    multi: bool = False,
    db: Database = Depends(get_db),
    _: str = Depends(read_token_from_header_factory),
):
    """Read one or multiple class records. Accepts optional parameters name and/or grade, otherwise will return any document."""

    search_query = {"name": name, "grade": grade}

    # Query should respect schemas and not have null values
    notValidQuery = schemas.check_input_query(
        input_query=search_query, schema=schemas.ClassBase
    )
    if notValidQuery:
        raise HTTPException(status_code=422, detail=notValidQuery)

    # Send Query To dB
    results = await crud.read_n_documents(
        collection=schemas.Data.CLASS.value,
        search_query=search_query,
        db=db,
        multi=multi,
    )
    # Handle responseif not data:
    if len(results) == 0:
        raise HTTPException(status_code=404, detail="Content NOT found")

    # Prepare response
    response = {"results": results}

    # Send Response
    return response


@classes.patch("/")
@handle_mongodb_exceptions
async def update_n_classes(
    update_obj: schemas.ClassBase,
    multi: bool = False,
    db: Database = Depends(get_db),
    _: str = Depends(read_token_from_header_factory),
):
    # Query the dB
    result = await crud.update_n_documents(
        collection=schemas.Data.CLASS.value,
        search_query=update_obj.search_query,
        update_data=update_obj.values_to_update(),
        db=db,
        multi=multi,
    )
    # Handle results
    # No match
    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Cannot find the document to update. Check the find query",
        )
    # No change
    if not result.modified_count > 0:
        raise HTTPException(status_code=400, detail="Fields have NOT been modified.")

    # Send response
    return {"message": "Updated was successful", "count": result.modified_count}


@classes.delete("/")
@handle_mongodb_exceptions
async def delete_n_classes(
    delete_query: dict,
    multi: bool = False,
    db: Database = Depends(get_db),
    token: str = Depends(read_token_from_header_factory),
):
    # Query should respect schemas and not have null values
    notValidQuery = schemas.check_input_query(
        input_query=delete_query, schema=schemas.ClassBase
    )
    if notValidQuery:
        raise HTTPException(status_code=422, detail=notValidQuery)

    # Query the dB
    collection = schemas.Data.CLASS.value

    await crud.delete_n_documents(
        collection=collection, search_query=delete_query, db=db, multi=multi
    )

    # Return response
    return {"message": "Deletion acknowledged"}
