import motor.motor_asyncio
from decouple import config


async def get_db():
    username = config("USERNAME_MONGO_DB")
    password = config("PASSWORD_MONGO_DB")
    db_name = config("DB_NAME")
    mongo_url = f"mongodb+srv://{username}:{password}@cluster0.cmttqde.mongodb.net/?retryWrites=true&w=majority"

    # Initialize the AsyncIOMotorClient
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)

    # Access the database
    db = client[db_name]

    try:
        yield db
    finally:
        # Close the connection (optional, as motor handles connection pooling)
        client.close()
