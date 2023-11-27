from fastapi import APIRouter, HTTPException, Depends, Body
from typing import Optional, Union
from schemas import schemas, custom_types
from crud import crud, queries
from pymongo.database import Database
from services import encryption
from db.db_handler import get_db
from pymongo import errors as pymongo_errors
from utils.setup import Setup
import json
from utils.decorators import handle_mongodb_exceptions
from routers.users import read_token_from_header_factory
from pydantic import BaseModel
from services import data_service


classes = APIRouter(prefix="/classes", tags=["Classes"])


@classes.post("/")
@handle_mongodb_exceptions
async def create_n_classes(
    classes_data: Union[schemas.ClassBase, list[schemas.ClassBase]],
    db: Database = Depends(get_db),
    _: str = Depends(
        read_token_from_header_factory(
            roles=[
                schemas.User.ADMIN.value,
            ]
        )
    ),
):
    """Create one or multiple class records. Accepts either a single class object or a list of class objects."""

    classes_ids = await data_service.create_service(
        data=classes_data,
        key_to_schema_map=schemas.Data.CLASS.value,
        db=db,
    )

    if isinstance(classes_data, list):
        return [
            {"id": id_, "info": obj_.get_class_info()}
            for obj_, id_ in zip(classes_data, classes_ids)
        ]
    else:
        return {"id": classes_ids, "info": classes_data.get_class_info()}


@classes.get("/")
@handle_mongodb_exceptions
async def read_n_classes(
    query: str,
    multi: bool = False,
    db: Database = Depends(get_db),
    _: str = Depends(read_token_from_header_factory()),
):
    """Read one or multiple class records. Accepts optional parameters name and/or grade, otherwise will return any document."""

    classes_data = await data_service.read_service(
        search_query=query,
        key_to_schema_map=schemas.Data.CLASS,
        db=db,
        multi=multi,
        is_user_query=False,
    )

    # Prepare response
    response = {
        "results": classes_data,
        "count": len(classes_data) if isinstance(classes_data, list) else None,
    }
    print(response)

    # Send Response
    return response


@classes.patch("/")
@handle_mongodb_exceptions
async def update_n_classes(
    query: str,
    update_data: dict,
    multi: bool = False,
    db: Database = Depends(get_db),
    _: str = Depends(read_token_from_header_factory(schemas.User.ADMIN)),
):
    # Query the dB

    return await data_service.update_service(
        search_query=query,
        update_query=update_data,
        key_to_schema_map=schemas.Data.CLASS,
        multi=multi,
        db=db,
    )


@classes.delete("/")
@handle_mongodb_exceptions
async def delete_n_classes(
    query: str,
    multi: bool = False,
    db: Database = Depends(get_db),
    _: str = Depends(
        read_token_from_header_factory(
            roles=[
                schemas.User.ADMIN,
            ]
        )
    ),
):
    return await data_service.delete_service(
        search_query=query,
        key_to_schema_map=schemas.Data.CLASS,
        multi=multi,
        db=db,
    )
