from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi import status
from schemas.schemas import KidLog
from crud import crud
import re
import pymongo
from typing import Annotated
from db.db_handler import get_db


teachers = APIRouter(prefix="/teachers")



@teachers.post('/log')
async def write_kid_log(kid_log : KidLog, db: pymongo.database.Database = Depends(get_db)):
    id = crud.save_kid_log(kid_log, db)
    return {"id":id}

@teachers.get('/{kid_name}/{month}/{year}') 
async def get_kid_month(kid_name: str, month: int, year: int, db: pymongo.database.Database = Depends(get_db)):
    return crud.get_kid_log_in_month(kid_name=kid_name, month=month, year=year, db=db)
