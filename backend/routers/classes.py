from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Optional, Union
from schemas import schemas
from crud import crud
from pymongo.database import Database
from utils import encryption
from db.db_handler import get_db
from pymongo import errors as pymongo_errors
from utils.setup import Setup
import json
from utils.decorators import handle_mongodb_exceptions
from routers.users import oauth2_scheme

classes = APIRouter(prefix="/classes", tags=["Classes"])


@classes.post("/")
@handle_mongodb_exceptions
async def create_n_classes(
    classes: Union[schemas.ClassBase, list[schemas.ClassBase]],
    db: Database = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Create one or multiple class records. Accepts either a single class object or a list of class objects."""
    if not encryption.check_admin(token):
        raise HTTPException(status_code=401, detail="Only Admins can create classes")

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
            {"_id": str(id_), "name": class_.name, "grade": class_.grade}
            for class_, id_ in zip(classes, inserted_ids)
        ]
    else:
        response = {
            "_id": str(inserted_ids),
            "name": classes.name,
            "grade": classes.grade,
        }

    # Send Response
    return response


@classes.get("/")
@handle_mongodb_exceptions
async def read_n_classes(
    name: Optional[str] = None,
    grade: Optional[int] = None,
    multi: bool = False,
    db: Database = Depends(get_db),
    _: str = Depends(oauth2_scheme),
):
    """Read one or multiple class records. Accepts optional parameters name and/or grade, otherwise will return any document."""

    # Create search query
    search_query = {}
    if name:
        search_query.update({"name": name})
    if grade:
        search_query.update({"grade": grade})
    # Send Query To dB
    results = await crud.read_n_documents(
        collection=schemas.Data.CLASS.value,
        search_query=search_query,
        db=db,
        multi=multi,
    )
    # Handle responseif not data:
    if not results:
        raise HTTPException(status_code=404, detail="Content NOT found")

    # Prepare response
    response = {"results": results}
    # Send Response
    return response


@classes.patch("/")
@handle_mongodb_exceptions
async def update_n_classes(
    search_query: dict,
    update_data: dict,
    multi: bool = False,
    db: Database = Depends(get_db),
    _: str = Depends(oauth2_scheme),
):
    # Validate queries keys
    schemas.check_keys_in_schema(schemas.ClassWithId, search_query)
    schemas.check_keys_in_schema(schemas.ClassWithId, update_data)
    # Query the dB
    updated_count = await crud.update_n_documents(
        collection=schemas.Data.CLASS.value,
        search_query=search_query,
        update_data=update_data,
        db=db,
        multi=multi,
    )
    # Handle results
    if updated_count < 1:
        HTTPException(status_code=410, detail="Update was NOT successful")
    # Send response
    return {"message": "Updated was successful", "count": updated_count}


@classes.delete("/")
@handle_mongodb_exceptions
async def delete_n_classes(
    deletion_keys: dict,
    multi: bool = False,
    db: Database = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    if not encryption.check_admin(token):
        raise HTTPException(status_code=401, detail="Only Admins can create classes")
    # Validates the keys given in the schema, only goes forward if the keys are valid
    schemas.check_keys_in_schema(schemas.ClassWithId, deletion_keys)

    collection = schemas.Data.CLASS.value

    await crud.delete_n_documents(
        collection=collection, search_query=deletion_keys, db=db, multi=multi
    )

    return HTTPException(status_code=200, detail=f"Deletion acknowledged")
