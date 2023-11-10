from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from decouple import config
from utils.setup import Setup

JWT_SECRET = config("JWT_SECRET")
JWT_ALGORITHM = config("JWT_ALGORITHM")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_jwt_token(user_id: str, user_role: str):
    """
    Create JWT token with user ID and role. Token expires in 7 days by default.
    """
    expires_delta: timedelta = timedelta(days=Setup.expiration_days_jwt)

    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "user_id": user_id, "user_role": user_role}
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
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return True
    except jwt.PyJWTError:
        return False
