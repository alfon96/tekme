from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class KidLog(BaseModel):
    name: str
    classes: int
    breaks: int
    teacher: str
    date: datetime
    detail: Optional[str] = None


class SignInModel(BaseModel):
    email: EmailStr
    password: str


class SignUpModel(BaseModel):
    role: str
    name: str
    surname: str
    birth_date: str
    phone: str
    email: EmailStr
    password: str
