from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from decouple import config
from utils.setup import Setup
from fastapi import HTTPException, Header


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


async def read_token(authorization: str = Header(...)) -> dict:
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Invalid or missing authorization header"
        )

    # Extract token from the authorization header
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
