from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from decouple import config
from utils.setup import Setup
from fastapi import HTTPException, Request
from schemas import schemas, custom_types
from urllib.parse import parse_qs
from typing import Union
import json
import urllib.parse

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_jwt_token(user_id: str, user_role: str):
    """
    Create JWT token with user ID and role. Token expires in 7 days by default.
    """
    expires_delta: timedelta = timedelta(days=Setup.expiration_days_jwt)

    expire = datetime.utcnow() + expires_delta
    to_encode = {
        f"{Setup.expiration}": expire,
        f"{Setup.id}": user_id,
        f"{Setup.role}": user_role,
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def encrypt_password(password: str):
    """
    Encrypt a plain password using bcrypt.
    """
    return pwd_context.hash(password)


def check_password(plain_password: str, hashed_password: str):
    """
    Verify a plain password against the hashed version.
    """
    return pwd_context.verify(plain_password, hashed_password)


def check_token(token: str):
    """
    Check if the JWT token is valid.
    """
    try:
        _ = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return True
    except jwt.PyJWTError:
        return False


async def read_token_from_header(request: Request) -> dict:
    authorization: str = request.headers.get("Authorization")

    if authorization is None:
        raise HTTPException(status_code=422, detail="Missing 'Authorization' header")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid 'Authorization' header")

    token = authorization.split(" ")[1]

    if not check_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        # Decode the token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def read_token(token: str) -> dict:
    if not check_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        # Decode the token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def check_admin(token):
    token_payload: dict = read_token(token)
    if token_payload["role"] != custom_types.User.ADMIN.value:
        return False
    return True


def decode_query(query: str) -> dict:
    """
    Decodes a query string into a dictionary. If the query string is a URL-encoded JSON string,
    it decodes it as JSON; otherwise, it treats it as a standard query string.
    """
    # Split the query string into separate parameters
    params = query.split("&")
    decoded_result = {}

    for param in params:
        # URL-decode each parameter
        decoded_param = urllib.parse.unquote(param)

        # Check if the parameter is in JSON format
        try:
            # If it's JSON, load it and update the dictionary
            json_part = json.loads(decoded_param)
            if isinstance(json_part, dict):
                decoded_result.update(json_part)
        except json.JSONDecodeError:
            # If it's not JSON, process as a standard key-value pair
            key_value = decoded_param.split("=", 1)
            if len(key_value) == 2:
                key, value = key_value
                decoded_result[key] = value

    return decoded_result


def decode_and_validate_query(
    query: str, key_to_schema_map: Union[schemas.User, schemas.Data]
) -> dict:
    try:
        # decode Query
        decoded_query = decode_query(query)
        base_model = schemas.complete_schema_mapping[key_to_schema_map]

        return schemas.validate_query_over_schema(
            base_model=base_model,
            query=decoded_query,
        )

    except Exception as e:
        raise e
