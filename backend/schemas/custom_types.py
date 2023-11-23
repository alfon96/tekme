from pydantic import BaseModel, constr
import phonenumbers
import re
from enum import Enum
from decouple import config
from pydantic import constr
from pydantic import PlainSerializer
from pydantic.functional_validators import PlainValidator
from pydantic import WithJsonSchema
from pydantic_core import PydanticCustomError
from typing_extensions import Annotated
from fastapi import HTTPException


class Data(Enum):
    CLASS = config("CLASSES_COLLECTION")
    SCORE = config("SCORES_COLLECTION")


class User(str, Enum):
    ADMIN = config("ADMIN_COLLECTION")
    STUDENT = config("STUDENTS_COLLECTION")
    TEACHER = config("TEACHERS_COLLECTION")
    RELATIVE = config("RELATIVES_COLLECTION")


def validate_name_surname(v: str) -> str:
    if len(v) > 200:
        raise ValueError("The string must not be more than 200 characters")
    return v


def validate_password(v):
    uppercase_regex = r"[A-Z]"
    lowercase_regex = r"[a-z]"
    special_symbol_regex = r"[!@#$%^&*()_+{}\[\]:;<>,.?~]"
    digit_regex = r"[0-9]"

    # Check if v contains at least one uppercase letter
    if not (
        re.search(uppercase_regex, v)
        and re.search(lowercase_regex, v)
        and re.search(special_symbol_regex, v)
        and re.search(digit_regex, v)
    ):
        raise ValueError(
            "v must contain at least one uppercase and lowercase letters, one special character, and one number!"
        )

    return v


def validate_phone(v: str) -> str:
    try:
        phone_number = phonenumbers.parse(v, None)
        if not (
            phonenumbers.is_possible_number(phone_number)
            and phonenumbers.is_valid_number(phone_number)
        ):
            raise ValueError("Invalid phone number: not a valid number.")
        return v
    except phonenumbers.NumberParseException:
        raise ValueError("Invalid phone number: unable to parse.")


def validate_user_role(v: str) -> str:
    if v not in [user.value for user in User]:
        raise HTTPException(status_code=422, detail="Invalid user Role")
    print("Inside the Validation")
    return v


def validate_query(v: str) -> dict:
    if not isinstance(v, dict):
        raise TypeError("Value must be a dictionary")

    schema = v.get("expected_schema")
    if schema:
        base_fields = set(schema.__fields__.keys())
        for key in v.keys():
            if key not in base_fields:
                raise ValueError(
                    f"Key '{key}' is not a valid field of {schema.__name__}"
                )

    return v


def validate_grade(v: int) -> int:
    if not 1 <= v <= 12:
        raise ValueError("Grade must be between 1 and 12")
    return v


NameSurname = Annotated[
    str,
    PlainSerializer(lambda v: v.isoformat(), return_type=str),
    PlainValidator(validate_name_surname),
    WithJsonSchema({"type": "string", "constraint": "max 250 characters"}),
]

Phone = Annotated[
    str,
    PlainSerializer(lambda v: v.isoformat(), return_type=str),
    PlainValidator(validate_phone),
    WithJsonSchema({"type": "string", "example": "+393711584965"}),
]

Password = Annotated[
    str,
    PlainSerializer(lambda v: v.isoformat(), return_type=str),
    PlainValidator(validate_password),
    WithJsonSchema(
        {
            "type": "string",
            "constraint": "must contain at least one uppercase, lowercase, number and special character",
        }
    ),
]

UserRole = Annotated[
    str,
    PlainSerializer(lambda v: v.isoformat(), return_type=str),
    PlainValidator(validate_user_role),
    WithJsonSchema({"type": "string", f"constraint": "must be inside of {User} class"}),
]

Query = Annotated[
    str,
    PlainSerializer(lambda v: v.isoformat(), return_type=str),
    PlainValidator(validate_query),
    WithJsonSchema({"type": "dict", "constraint": "we will see"}),
]

Grade = Annotated[
    str,
    PlainSerializer(lambda v: v.isoformat(), return_type=str),
    PlainValidator(validate_grade),
    WithJsonSchema({"type": "int", "constraint": "in between 1 and 12"}),
]
