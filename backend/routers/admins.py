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


admins = APIRouter(prefix="/admins", tags=["Admins"])


@admins.patch("/{user_id}")
@handle_mongodb_exceptions
async def update_other_user(
    user_id: str,
    user_role: schemas.User,
    update_data: dict,
    multi: bool = False,
    db: Database = Depends(get_db),
    _: dict = Depends(
        read_token_from_header_factory(
            roles=[
                schemas.User.ADMIN,
            ]
        )
    ),
) -> dict:
    """Update user data based on the user role."""
    if user_role == schemas.User.ADMIN:
        raise HTTPException(status_code=422, detail="Admins can't modify other admins")
    search_query = {f"{Setup.id}": user_id}
    return await data_service.update_service(
        search_query=search_query,
        update_query=update_data,
        key_to_schema_map=user_role,
        db=db,
        multi=multi,
    )


@admins.delete("/{user_id}")
@handle_mongodb_exceptions
async def delete_other_user(
    user_id: str,
    user_role: schemas.User,
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
    """Delete a user after verifying their password."""
    if user_role == schemas.User.ADMIN:
        raise HTTPException(status_code=422, detail="Admins can't delete other admins")
    search_query = {f"{Setup.id}": user_id}
    return await data_service.delete_service(
        search_query=search_query, key_to_schema_map=user_role, db=db, multi=multi
    )
