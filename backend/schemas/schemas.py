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
    validate_value_over_field,
)
from urllib.parse import parse_qs


def decode_and_validate_query(encoded_query: str, schema: Type[BaseModel]) -> dict:
    parsed_query = parse_qs(encoded_query)
    data = {k: v[0] if len(v) == 1 else v for k, v in parsed_query.items()}

    return validate_query_over_schema(schema, data)


from pydantic import parse_obj_as
from typing import Any, get_args, get_type_hints


def validate_query_over_schema(data: dict[str, any], schema: Type[BaseModel]):
    field_types = get_type_hints(schema)

    keys_to_validate = set(data.keys())
    reference_keys = set(field_types.keys())
    extra_keys = keys_to_validate - reference_keys

    if extra_keys:
        raise HTTPException(
            status_code=422, detail=f"Invalid Keys, you can only use {reference_keys}"
        )

    for field_name, field_type in field_types.items():
        existing_field = data.get(field_name, None)
        if existing_field:
            try:
                validate_value_over_field(
                    value=existing_field, type_in_schema=field_type
                )
            except Exception as e:
                raise e
    return data


class UserBase(BaseModel):
    id: Optional[str] = None
    name: NameSurname
    surname: NameSurname
    birthday: date | datetime
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
    details: List[str] = []
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
