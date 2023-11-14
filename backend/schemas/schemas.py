from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


class KidLog(BaseModel):
    name: str
    classes: int
    breaks: int
    teacher: str
    date: date
    detail: Optional[str] = None


class SignInModel(BaseModel):
    email: EmailStr
    password: str


class SignUpModel(BaseModel):
    role: str
    name: str
    surname: str
    birth_date: date
    phone: str
    email: EmailStr
    password: str


class StudentBase(BaseModel):
    id: Optional[str] = None
    name: str
    surname: str
    birth_date: date
    details: str
    scores: Optional[str] = None
    parent_ids: list[str]


class StudentSignin(StudentBase):
    phone: str
    password: str
    email: str


class ParentBase(BaseModel):
    id: Optional[str] = None
    name: str
    surname: str
    birth_date: date
    details: str
    child_ids: list[str]


class ParentSignin(ParentBase):
    phone: str
    password: str
    email: str


class TeacherBase(BaseModel):
    name: str
    surname: str
    birth_date: date
    subjects: list[str]


class TeacherSignin(TeacherBase):
    phone: str
    password: str
    email: str


class Score(BaseModel):
    id: Optional[str] = None
    classes: int
    breaks: int
    date: date
    details: str
    teacher: TeacherBase


class Class(BaseModel):
    name: str
    grade: int
    teachers: list[TeacherBase]
    students: list[StudentBase]
