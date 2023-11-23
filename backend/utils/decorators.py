from fastapi import HTTPException
from pymongo import errors as pymongo_errors
from functools import wraps


def handle_mongodb_exceptions(func):
    """
    Decorator to handle MongoDB exceptions for FastAPI route functions.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except pymongo_errors.PyMongoError as e:
            # Handle specific MongoDB exceptions as needed
            if isinstance(e, pymongo_errors.DuplicateKeyError):
                raise HTTPException(status_code=400, detail="Duplicate key error.")
            elif isinstance(e, pymongo_errors.OperationFailure):
                raise HTTPException(status_code=500, detail="Operation failure.")
            elif isinstance(e, pymongo_errors.ConfigurationError):
                raise HTTPException(status_code=500, detail="Configuration error.")
            elif isinstance(e, pymongo_errors.NetworkTimeout):
                raise HTTPException(status_code=408, detail="Network timeout.")
            # Add more specific exceptions as needed

            # General MongoDB error
            raise HTTPException(status_code=500, detail="A database error occurred.")
        except Exception as e:
            # If the exception was handled in the API routes raise it, otherwise raise the standard one
            if isinstance(e, HTTPException):
                raise e
            else:
                raise HTTPException(status_code=500, detail=str(e))

    return wrapper
