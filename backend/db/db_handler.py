import pymongo
from decouple import config
from enum import Enum


def get_db() -> pymongo.database.Database:
    # Replace these values with your MongoDB connection details
    username = config("USERNAME_MONGO_DB")
    password = config("PASSWORD_MONGO_DB")
    db_name = config("DB_NAME")
    mongo_url = f"mongodb+srv://{username}:{password}@cluster0.cmttqde.mongodb.net/?retryWrites=true&w=majority"

    # Initialize the MongoClient
    client = pymongo.MongoClient(mongo_url)

    # Access the database
    db = client.get_database(db_name)

    try:
        yield db
    except Exception as e:
        print(str(e))
    finally:
        db.client.close()