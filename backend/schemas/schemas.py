from pydantic import (
    BaseModel,
    ValidationError,
    create_model,
    EmailStr,
    validator,
)
from typing import List, Optional, Union, Type
from datetime import datetime, date
from fastapi import HTTPException
from schemas.custom_types import (
    User,
    Data,
    UserRole,
    Password,
    NameSurname,
    Phone,
    Grade,
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
    role: UserRole
    email: EmailStr
    password: Password

    class Config:
        extra = "forbid"


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

    id: Optional[str]
    classes: int
    breaks: int
    datetime: datetime
    details: Optional[list[str]] = []
    teacher_id: str
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


role_schema_map = {
    User.ADMIN: AdminSensitiveData,
    User.TEACHER: TeacherSensitiveData,
    User.STUDENT: StudentSensitiveData,
    User.RELATIVE: RelativeSensitiveData,
}

role_schema_update_map = {
    User.ADMIN: Admin,
    User.TEACHER: Teacher,
    User.STUDENT: Student,
    User.RELATIVE: Relative,
}


def find_unique_fields(base_class: BaseModel, sub_class: BaseModel) -> BaseModel:
    base_fields = set(base_class.__fields__)
    sub_class_fields = set(sub_class.__fields__)
    unique_fields = sub_class_fields - base_fields

    # Prepare fields for the new model
    try:
        fields = {
            field_name: (field.annotation, field.default)
            for field_name, field in sub_class.__fields__.items()
            if field_name in unique_fields
        }
        model = create_model("SubsetData", **fields)
        return model
    except Exception as e:
        raise e


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
