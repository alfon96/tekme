from pydantic import BaseModel, Field, EmailStr, field_validator
from bson import ObjectId
from typing import List, Optional, Union
from datetime import datetime
import phonenumbers
import re
from decouple import config
from enum import Enum


class Data(Enum):
    CLASS = config("CLASSES_COLLECTION")
    SCORE = config("SCORES_COLLECTION")


class User(str, Enum):
    ADMIN = config("ADMIN_COLLECTION")
    STUDENT = config("STUDENTS_COLLECTION")
    TEACHER = config("TEACHERS_COLLECTION")
    RELATIVE = config("RELATIVES_COLLECTION")


def check_keys_in_schema(schema: BaseModel, data: dict) -> bool:
    schema_keys = set(schema.__fields__.keys())
    for key in data.keys():
        if key not in schema_keys:
            return False
    return True


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

    @field_validator("role")
    def validate_user_role(cls, role):
        return validate_user_role(role)

    @field_validator("password")
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

    @field_validator("name")
    def validate_name(cls, name):
        return validate_non_empty_string(name)

    @field_validator("surname")
    def validate_name(cls, surname):
        return validate_non_empty_string(surname)

    @field_validator("password")
    def validate_password(cls, password):
        return validate_password(password)

    @field_validator("phone")
    def validate_phone_number(cls, phone):
        return validate_phone_number(phone)


# Admin schema
class AdminBase(BaseModel):
    """Represents a basic schema for a student."""

    id: Union[str, None] = Field(default_factory=str, alias="_id")
    name: str
    surname: str
    birthday: datetime
    profile_pic: Optional[str] = None


class AdminSensitiveData(AdminBase):
    """Schema for student sign-in, inheriting from StudentBase."""

    email: EmailStr
    password: str
    phone: str

    @field_validator("phone")
    def validate_phone_number(cls, phone):
        return validate_phone_number(phone)


class AdminUpdateData(AdminBase):
    """Schema for student sign-in, inheriting from StudentBase."""

    email: EmailStr
    phone: str

    @field_validator("phone")
    def validate_phone_number(cls, phone):
        return validate_phone_number(phone)


# Teacher schema
class TeacherBase(BaseModel):
    """Represents a basic schema for a teacher."""

    id: Union[str, None] = Field(default_factory=str, alias="_id")
    name: str
    surname: str
    birthday: datetime
    profile_pic: Optional[str] = None
    subjects: list[str]


class TeacherSensitiveData(TeacherBase):
    """Schema for teacher sign-in, inheriting from TeacherBase."""

    email: EmailStr
    password: str
    phone: str

    @field_validator("phone")
    def validate_phone_number(cls, phone):
        return validate_phone_number(phone)


class TeacherUpdateData(AdminBase):
    """Schema for student sign-in, inheriting from StudentBase."""

    email: EmailStr
    phone: str

    @field_validator("phone")
    def validate_phone_number(cls, phone):
        return validate_phone_number(phone)


# Student schema
class StudentBase(BaseModel):
    """Represents a basic schema for a student."""

    id: Union[str, None] = Field(default_factory=str, alias="_id")
    name: str
    surname: str
    birthday: datetime
    details: list[str] = []
    relatives_id: list[str] = []
    teachers_id: list[str] = []
    profile_pic: Optional[str] = None


class StudentSensitiveData(StudentBase):
    """Schema for student sign-in, inheriting from StudentBase."""

    email: EmailStr
    password: str
    phone: str

    @field_validator("phone")
    def validate_phone_number(cls, phone):
        return validate_phone_number(phone)


class StudentUpdateData(AdminBase):
    """Schema for student sign-in, inheriting from StudentBase."""

    email: EmailStr
    phone: str

    @field_validator("phone")
    def validate_phone_number(cls, phone):
        return validate_phone_number(phone)


# Relative schema
class RelativeBase(BaseModel):
    """Represents a basic schema for a relative."""

    id: str = Field(default_factory=str, alias="_id")
    name: str
    surname: str
    birthday: datetime
    children_id: list[str] = []
    profile_pic: Optional[str] = None


class RelativeSensitiveData(RelativeBase):
    """Schema for relative sign-in, inheriting from RelativeBase."""

    email: EmailStr
    password: str
    phone: str

    @field_validator("phone")
    def validate_phone_number(cls, phone):
        return validate_phone_number(phone)


class RelativeUpdateData(AdminBase):
    """Schema for student sign-in, inheriting from StudentBase."""

    email: EmailStr
    phone: str

    @field_validator("phone")
    def validate_phone_number(cls, phone):
        return validate_phone_number(phone)


# Score schema
class ScoreBase(BaseModel):
    """Schema representing a score."""

    id: Union[str, None] = Field(default_factory=str, alias="_id")
    classes: int
    breaks: int
    date: datetime
    details: Optional[list[str]] = []
    teachers_id: str


# Class schema
class ClassBase(BaseModel):
    """Schema representing a class."""

    id: Union[str, None] = Field(default_factory=str, alias="_id")
    name: str
    grade: int
    students_id: Optional[list[str]] = []
    teachers_id: Optional[list[str]] = []
    details: Optional[list[str]] = []
    type: Optional[list[str]] = []

    @field_validator("grade")
    def validate_grade(cls, v):
        """Ensures grade is within an acceptable range."""
        if not 1 <= v <= 12:
            raise ValueError("Grade must be between 1 and 12")
        return v

    @field_validator("name")
    def validate_name(cls, v):
        """Validates that the class name starts with a capital letter and contains only alphabetic characters."""
        if not re.match(r"^[A-Z][a-zA-Z]*$", v):
            raise ValueError(
                "Name must start with a capital letter and contain only alphabetic characters"
            )
        return v


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
