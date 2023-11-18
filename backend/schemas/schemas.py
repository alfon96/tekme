from pydantic import BaseModel, Field, EmailStr, validator
from bson import ObjectId
from typing import List, Optional
from datetime import datetime
import phonenumbers
import re
from decouple import config
from enum import Enum


class Data(Enum):
    CLASS = "classes"
    SCORE = "scores"


class User(str, Enum):
    STUDENT = "students"
    TEACHER = "teachers"
    RELATIVE = "relatives"


collection_mapping = {
    User.STUDENT: config("STUDENTS_COLLECTION"),
    User.TEACHER: config("TEACHERS_COLLECTION"),
    User.RELATIVE: config("RELATIVES_COLLECTION"),
    Data.CLASS: config("CLASSES_COLLECTION"),
    Data.SCORE: config("SCORES_COLLECTION"),
}


def check_keys_in_schema(schema: BaseModel, data: dict) -> bool:
    schema_keys = set(schema.__fields__.keys())
    for key in data.keys():
        if key not in schema_keys:
            return False
    return True


class PyObjectId(ObjectId):
    """Custom field type for handling MongoDB ObjectId in Pydantic models."""

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values, **kwargs):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


def validate_phone_number(number: str) -> str:
    """Validates that a phone number is internationally formatted and valid."""
    try:
        phone_number = phonenumbers.parse(number, None)

        if not (
            phonenumbers.is_possible_number(phone_number)
            and phonenumbers.is_valid_number(phone_number)
        ):
            raise ValueError("Invalid phone number: not a valid number.")

        return number

    except phonenumbers.NumberParseException:
        raise ValueError("Invalid phone number: unable to parse.")


def validate_password(password: str):
    uppercase_regex = r"[A-Z]"
    lowercase_regex = r"[a-z]"
    special_symbol_regex = r"[!@#$%^&*()_+{}\[\]:;<>,.?~]"
    digit_regex = r"[0-9]"

    # Check if password contains at least one uppercase letter
    if not (
        re.search(uppercase_regex, password)
        and re.search(lowercase_regex, password)
        and re.search(special_symbol_regex, password)
        and re.search(digit_regex, password)
    ):
        raise ValueError(
            "Password must contain at least one uppercase and lowercase letters, one special character, and one number!"
        )

    return password


# user_role validator
def validate_user_role(role: str):
    """Validates that the role is one of the allowed options."""
    if role not in [user.value for user in User]:
        raise ValueError('Role must be one of "Student", "Teacher", or "Relative".')
    return role


# empty string validator
def validate_non_empty_string(input: str):
    if input == "":
        raise ValueError("This field cannot be empty")
    return input


# SignInModel
class Signin(BaseModel):
    """Represents a basic schema for whatever user to signin."""

    role: str
    email: EmailStr
    password: str

    @validator("role", pre=True)
    def validate_user_role(cls, role):
        return validate_user_role(role)

    @validator("password", pre=True)
    def validate_password(cls, password):
        return validate_password(password)


# SignUpModel
class Signup(BaseModel):
    """Represents a basic schema for whatever user to signup."""

    name: str
    surname: str
    birthday: datetime
    email: EmailStr
    password: str
    phone: str
    profile_pic: Optional[str] = None
    role: str

    @validator("name", pre=True)
    def validate_name(cls, name):
        return validate_non_empty_string(name)

    @validator("surname", pre=True)
    def validate_name(cls, surname):
        return validate_non_empty_string(surname)

    @validator("password", pre=True)
    def validate_password(cls, password):
        return validate_password(password)

    @validator("role", pre=True)
    def validate_user_role(cls, role):
        return validate_user_role(role)

    @validator("phone", pre=True)
    def validate_phone_number(cls, phone):
        return validate_phone_number(phone)


# Teacher schema
class TeacherBase(BaseModel):
    """Represents a basic schema for a teacher."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    surname: str
    birthday: datetime
    subjects: list[str]
    profile_pic: Optional[str] = None


class TeacherSensitiveData(TeacherBase):
    """Schema for teacher sign-in, inheriting from TeacherBase."""

    email: EmailStr
    password: str
    phone: str

    _validate_phone = validator("phone", allow_reuse=True)(validate_phone_number)


# Student schema
class StudentBase(BaseModel):
    """Represents a basic schema for a student."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    surname: str
    birthday: datetime
    details: list[str]
    relatives_id: list[PyObjectId]
    teachers_id: list[PyObjectId]
    profile_pic: Optional[str] = None


class StudentSensitiveData(StudentBase):
    """Schema for student sign-in, inheriting from StudentBase."""

    email: EmailStr
    password: str
    phone: str

    _validate_phone = validator("phone", allow_reuse=True)(validate_phone_number)


# Relative schema
class RelativeBase(BaseModel):
    """Represents a basic schema for a relative."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    surname: str
    birthday: datetime
    children_id: list[PyObjectId]
    profile_pic: Optional[str] = None


class RelativeSensitiveData(RelativeBase):
    """Schema for relative sign-in, inheriting from RelativeBase."""

    email: EmailStr
    password: str
    phone: str

    _validate_phone = validator("phone", allow_reuse=True)(validate_phone_number)


# Score schema
class ScoreBase(BaseModel):
    """Schema representing a score."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    classes: int
    breaks: int
    date: datetime
    details: list[str]
    teachers_id: PyObjectId


# Class schema
class ClassBase(BaseModel):
    """Schema representing a class."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    grade: int
    students_id: list[PyObjectId]
    teachers_id: list[PyObjectId]
    details: list[str]
    type: list[str]

    @validator("grade", pre=True)
    def validate_grade(cls, v):
        """Ensures grade is within an acceptable range."""
        if not 1 <= v <= 12:
            raise ValueError("Grade must be between 1 and 12")
        return v

    @validator("name", pre=True)
    def validate_name(cls, v):
        """Validates that the class name starts with a capital letter and contains only alphabetic characters."""
        # ... existing logic ...
        if not re.match(r"^[A-Z][a-zA-Z]*$", v):
            raise ValueError(
                "Name must start with a capital letter and contain only alphabetic characters"
            )
        return v
