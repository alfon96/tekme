from pydantic import (
    BaseModel,
    ValidationError,
    create_model,
    EmailStr,
    validator,
    validator,
)
from typing import List, Optional, Union, Annotated
from datetime import datetime, date
from fastapi import HTTPException
from enum import Enum
from schemas.custom_types import (
    User,
    Data,
    UserRole,
    Password,
    NameSurname,
    Phone,
    Grade,
    Score,
)


class UserBase(BaseModel):
    id: Optional[str] = None
    name: NameSurname
    surname: NameSurname
    birthday: Union[datetime, date]
    details: List[str] = []
    profile_pic: Optional[str] = None
    email: EmailStr

    class Config:
        extra = "forbid"
        arbitrary_types_allowed = True


class UserSensitiveData(UserBase):
    password: Password
    phone: Phone


class UserUpdateData(UserBase):
    phone: Phone


class Admin(UserBase):
    pass


class Teacher(UserBase):
    subjects: List[str]

    @validator("subjects")
    def check_subjects_not_empty(cls, v):
        if not v or len(v) == v.count(""):
            raise ValueError("Teachers must have at least one subject")

        return v


class Student(UserBase):
    relatives_id: List[str] = []
    teachers_id: List[str] = []


class Relative(UserBase):
    children_id: List[str] = []


class AdminSensitiveData(Admin, UserSensitiveData):
    pass


class TeacherSensitiveData(Teacher, UserSensitiveData):
    pass


class StudentSensitiveData(Student, UserSensitiveData):
    pass


class RelativeSensitiveData(Relative, UserSensitiveData):
    pass


class Signin(BaseModel):
    email: EmailStr
    password: Password

    class Config:
        extra = "forbid"

    def get_email_query(self) -> dict:
        return {"email": self.email}


class UserFactory(BaseModel):
    """
    Represents a general user and acts as a factory for specific user types.
    """

    @staticmethod
    def create_user(
        role: str, user_data: dict
    ) -> Union[Admin, Teacher, Student, Relative]:
        role_to_class = {
            User.ADMIN.value: Admin,
            User.TEACHER.value: Teacher,
            User.STUDENT.value: Student,
            User.RELATIVE.value: Relative,
        }

        target_class = role_to_class.get(role)
        if not target_class:
            raise ValueError("Invalid role")

        # Get specific class keys
        target_fields = target_class.__fields__.keys()

        # Filter out invalid keys for the specific class
        filtered_data = {k: v for k, v in user_data.items() if k in target_fields}

        # Create the user object
        return target_class(**filtered_data)


# Score schema
class ScoreBase(BaseModel):
    """Schema representing a score."""

    id: Optional[str] = None
    classes: Score
    breaks: Score
    date: datetime
    details: Optional[list[str]] = []
    teacher_id: Optional[str] = None
    students_id: Union[str, List[str]]
    creation: datetime

    class Config:
        extra = "forbid"


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
    creation: datetime

    class Config:
        extra = "forbid"

    def get_class_info(self):
        return f"{self.grade}_{self.name}"


role_schema_map = {
    User.ADMIN: AdminSensitiveData,
    User.TEACHER: TeacherSensitiveData,
    User.STUDENT: StudentSensitiveData,
    User.RELATIVE: RelativeSensitiveData,
}

data_schema_map = {
    Data.CLASS: ClassBase,
    Data.SCORE: ScoreBase,
}

complete_schema_mapping = {**role_schema_map, **data_schema_map}

role_schema_update_map = {
    User.ADMIN: Admin,
    User.TEACHER: Teacher,
    User.STUDENT: Student,
    User.RELATIVE: Relative,
}


not_admin_users = {
    name: value for name, value in User.__members__.items() if value != User.ADMIN.value
}

NotAdminUsers = Enum("NotAdminUsers", not_admin_users)


def validate_query_over_schema(base_model: BaseModel, query: dict) -> BaseModel:
    # Extract keys from both query and model
    base_fields = set(base_model.__fields__)
    query_keys = set(query.keys())
    unique_fields = query_keys - base_fields

    # If the query has different keys -> status_code 422
    if unique_fields:
        raise HTTPException(
            status_code=422, detail=f"You can only use this keys {base_fields}"
        )

    query_mathing_fields = {
        field_name: (field.annotation, field.default)
        for field_name, field in base_model.__fields__.items()
        if field_name in query_keys
    }

    model = create_model("QuerySubModel", **query_mathing_fields)

    # Try parsing the query in the newly created model to get full query validation

    try:
        validated_query = model(**query)
        return validated_query.dict()
    except ValidationError as e:
        raise e

    # Create a new dynamic model


class ThingsFactory(BaseModel):
    """
    Represents a general non user class and acts as a factory for scores and classes types.
    """

    @staticmethod
    def create_thing(thing: str, data: dict) -> Union[ScoreBase, ClassBase]:
        thing_to_class = {
            Data.CLASS.value: ClassBase,
            Data.SCORE.value: ScoreBase,
        }

        target_class = thing_to_class.get(thing)
        if not target_class:
            raise ValueError(
                f"Invalid thing, it can only be one in '{[x.value for x in Data]}'"
            )

        # Get specific class keys
        target_fields = target_class.__fields__.keys()

        # Filter out invalid keys for the specific class
        filtered_data = {k: v for k, v in data.items() if k in target_fields}

        # Create the user object
        return target_class(**filtered_data)
