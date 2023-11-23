from pydantic import BaseModel, Field, EmailStr, field_validator
from bson import ObjectId
from typing import List, Optional, Union
from datetime import datetime
import re
from utils import encryption
from fastapi import HTTPException
import json
import urllib.parse
from schemas.custom_types import (
    User,
    Data,
    UserRole,
    Password,
    NameSurname,
    Phone,
    Grade,
    Query,
)
from typing import Type


# SignInModel
class Signin(BaseModel):
    """Represents a basic schema for whatever user to signin."""

    role: UserRole
    email: EmailStr
    password: Password

    class Config:
        extra = "forbid"


class GenericUser(BaseModel):
    """Represents a basic schema for whatever user to signup."""

    id: Optional[str] = None
    name: NameSurname
    surname: NameSurname
    birthday: datetime
    profile_pic: Optional[str] = None
    subjects: Optional[list[str]] = []
    details: Optional[list[str]] = []

    class Config:
        extra = "forbid"


class Signup(GenericUser):
    email: EmailStr
    password: Password
    phone: Phone


# Admin schema
class AdminBase(BaseModel):
    """Represents a basic schema for a student."""

    id: Optional[str]
    name: NameSurname
    surname: NameSurname
    birthday: datetime
    profile_pic: Optional[str] = None

    class Config:
        extra = "forbid"


class AdminSensitiveData(AdminBase):
    """Schema for student sign-in, inheriting from StudentBase."""

    email: EmailStr
    password: Password
    phone: Phone


class AdminUpdateData(AdminBase):
    """Schema for student sign-in, inheriting from StudentBase."""

    email: EmailStr
    phone: Phone


# Teacher schema
class TeacherBase(BaseModel):
    """Represents a basic schema for a teacher."""

    id: Optional[str]
    name: NameSurname
    surname: NameSurname
    birthday: datetime
    profile_pic: Optional[str] = None
    subjects: list[str]

    class Config:
        extra = "forbid"


class TeacherSensitiveData(TeacherBase):
    """Schema for teacher sign-in, inheriting from TeacherBase."""

    email: EmailStr
    password: Password
    phone: Phone


class TeacherUpdateData(AdminBase):
    """Schema for student sign-in, inheriting from StudentBase."""

    email: EmailStr
    phone: Phone


# Student schema
class StudentBase(BaseModel):
    """Represents a basic schema for a student."""

    id: Optional[str]
    name: NameSurname
    surname: NameSurname
    birthday: datetime
    details: list[str] = []
    relatives_id: list[str] = []
    teachers_id: list[str] = []
    profile_pic: Optional[str] = None

    class Config:
        extra = "forbid"


class StudentSensitiveData(StudentBase):
    """Schema for student sign-in, inheriting from StudentBase."""

    email: EmailStr
    password: Password
    phone: Phone


class StudentUpdateData(AdminBase):
    """Schema for student sign-in, inheriting from StudentBase."""

    email: EmailStr
    phone: Phone


class UserRoles(BaseModel):
    role: UserRole


# Relative schema
class RelativeBase(BaseModel):
    """Represents a basic schema for a relative."""

    id: Optional[str]
    name: NameSurname
    surname: NameSurname
    birthday: datetime
    children_id: list[str] = []
    profile_pic: Optional[str] = None

    class Config:
        extra = "forbid"


class RelativeSensitiveData(RelativeBase):
    """Schema for relative sign-in, inheriting from RelativeBase."""

    email: EmailStr
    password: Password
    phone: Phone


class RelativeUpdateData(AdminBase):
    """Schema for student sign-in, inheriting from StudentBase."""

    email: EmailStr
    phone: Phone


class UserFactory(BaseModel):
    """
    Represents a general user and acts as a factory for specific user types.
    """

    @staticmethod
    def create_user(
        role: str, signup_data: GenericUser
    ) -> Union[AdminBase, TeacherBase, StudentBase, RelativeBase]:
        role_to_class = {
            User.ADMIN.value: AdminBase,
            User.TEACHER.value: TeacherBase,
            User.STUDENT.value: StudentBase,
            User.RELATIVE.value: RelativeBase,
        }

        target_class = role_to_class.get(role)
        if not target_class:
            raise ValueError("Invalid role")

        # Get specific class keys
        target_fields = target_class.__fields__.keys()

        # Filter out invalid keys for the specific class
        filtered_data = {
            k: v for k, v in signup_data.dict().items() if k in target_fields
        }

        # Create the user object
        return target_class(**filtered_data)


# Score schema
class ScoreBase(BaseModel):
    """Schema representing a score."""

    id: Optional[str]
    classes: int
    breaks: int
    date: datetime
    details: Optional[list[str]] = []
    teacher_id: str
    students_id: Union[str, List[str]]

    class Config:
        extra = "forbid"


class ScoreUpdate(ScoreBase):
    search_query: Query

    @field_validator("search_query")
    def validate_search_query(cls, v, values, **kwargs):
        base_fields = set(ClassBase.__fields__.keys())
        for key in v.keys():
            if key not in base_fields:
                raise ValueError(
                    f"Key '{key}' in search_query is not a valid field of ClassBase"
                )
        return v

    def values_to_update(self):
        # Return the object without search_query and filter out None or empty lists
        score_data = self.dict()
        score_data.pop("search_query", None)

        return {k: v for k, v in score_data.items() if v is not None and v != []}


# Class schema
class ClassBase(BaseModel):
    """Schema representing a class."""

    id: Optional[str] = None
    name: NameSurname
    grade: Grade
    students_id: Optional[list[str]] = []
    teachers_id: Optional[list[str]] = []
    details: Optional[list[str]] = []
    type: Optional[list[str]] = []

    class Config:
        extra = "forbid"


class ClassUpdate(ClassBase):
    """Schema for updating a class, with an additional search_query field."""

    search_query: dict

    @field_validator("search_query")
    def validate_search_query(cls, v, values, **kwargs):
        base_fields = set(ClassBase.__fields__.keys())
        for key in v.keys():
            if key not in base_fields:
                raise ValueError(
                    f"Key '{key}' in search_query is not a valid field of ClassBase"
                )
        return v

    def values_to_update(self):
        # Return the object without search_query and filter out None or empty lists
        class_data = self.dict()
        class_data.pop("search_query", None)

        return {k: v for k, v in class_data.items() if v is not None and v != []}


class EncodedQuery(BaseModel):
    query: str

    @field_validator("query")
    def validate_query(cls, v):
        if not v:
            raise ValueError("The encoded_query cannot be empty")
        return v

    def decode(self):
        try:
            # URL-decode the encoded string
            json_string = urllib.parse.unquote(self.query)

            # Convert the JSON string back to a dictionary
            query_params = json.loads(json_string)

            return query_params
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in the encoded query")

    def validate_query(cls, v):
        base_fields = set(EncodedQuery.__fields__.keys())
        for key in v.keys():
            if key not in base_fields:
                raise ValueError(
                    f"Key '{key}' in search_query is not a valid field of ClassBase"
                )
        return v

    class Config:
        extra = "forbid"


role_schema_map = {
    User.ADMIN: AdminSensitiveData,
    User.TEACHER: TeacherSensitiveData,
    User.STUDENT: StudentSensitiveData,
    User.RELATIVE: RelativeSensitiveData,
}

role_schema_update_map = {
    User.ADMIN: AdminUpdateData,
    User.TEACHER: TeacherUpdateData,
    User.STUDENT: StudentUpdateData,
    User.RELATIVE: RelativeUpdateData,
}


def check_keys_in_schema(schema: BaseModel, data: dict) -> bool:
    schema_keys = set(schema.__fields__.keys())
    for key in data.keys():
        if key not in schema_keys:
            return False
    return True


def check_not_null_values(data: dict) -> bool:
    for key in data.keys():
        if data[key] == None or data[key] == "":
            return False
    return True


def check_input_query(input_query: dict, schema: BaseModel) -> str:
    """Check input queries."""
    # Check keys correctness
    if not check_keys_in_schema(
        schema=schema,
        data=input_query,
    ):
        return "The provided keys do not match the Schema!"

    # Check non empty values
    if not check_not_null_values(data=input_query):
        return "Input dictionary can't contain null values"

    return ""


def check_admin(token: str) -> str:
    """Checks token belongs to admin and input_query correctness"""

    if not encryption.check_admin(token):
        return "Only Admins can create classes"

    return ""
