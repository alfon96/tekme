import motor.motor_asyncio
from decouple import config
from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Generator, AsyncGenerator


async def get_db(request: Request = None) -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    # Determines which database to use based on request
    if request and request.headers.get("X-Test-Env"):
        db_name = config("TEST_DB_NAME")
        mongo_url = config("MONGO_DB_TEST_URI")
    else:
        db_name = config("PROD_DB_NAME")
        mongo_url = config("MONGO_DB_PROD_URI")

    # Connessione al database
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    try:
        yield db
    finally:
        client.close()
