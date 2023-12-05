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


attendances = APIRouter(prefix="/attendances", tags=["Attendances"])


@attendances.post("/")
@handle_mongodb_exceptions
async def create_n_attendances(
    attendances_data: Union[schemas.AttendanceBase, list[schemas.AttendanceBase]],
    db: Database = Depends(get_db),
    token_payload: str = Depends(
        read_token_from_header_factory(
            roles=[
                schemas.User.TEACHER.value,
            ]
        )
    ),
):
    """Create one or multiple class records. Accepts either a single class object or a list of class objects."""

    attendances_ids = await data_service.create_service(
        data=attendances_data,
        key_to_schema_map=schemas.Data.ATTENDANCE.value,
        db=db,
    )

    return {"id": attendances_ids}


@attendances.get("/")
@handle_mongodb_exceptions
async def read_n_attendances(
    query: str,
    multi: bool = False,
    db: Database = Depends(get_db),
    _: str = Depends(read_token_from_header_factory()),
):
    """Read one or multiple class records. Will return any document."""

    attendances_data = await data_service.read_service(
        search_query=query,
        key_to_schema_map=schemas.Data.ATTENDANCE,
        db=db,
        multi=multi,
        is_user_query=False,
    )

    # Prepare response
    response = {
        "results": attendances_data,
        "count": len(attendances_data) if isinstance(attendances_data, list) else None,
    }

    # Send Response
    return response


@attendances.patch("/")
@handle_mongodb_exceptions
async def update_n_attendances(
    query: str,
    update_data: dict,
    multi: bool = False,
    db: Database = Depends(get_db),
    _: str = Depends(read_token_from_header_factory(schemas.User.TEACHER)),
):
    # Query the dB

    return await data_service.update_service(
        search_query=query,
        update_query=update_data,
        key_to_schema_map=schemas.Data.ATTENDANCE,
        multi=multi,
        db=db,
    )


@attendances.delete("/")
@handle_mongodb_exceptions
async def delete_n_attendances(
    query: str,
    multi: bool = False,
    db: Database = Depends(get_db),
    _: str = Depends(
        read_token_from_header_factory(
            roles=[
                schemas.User.TEACHER,
            ]
        )
    ),
):
    return await data_service.delete_service(
        search_query=query,
        key_to_schema_map=schemas.Data.ATTENDANCE,
        multi=multi,
        db=db,
    )
