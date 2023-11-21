import unittest
import asyncio
from decouple import config
import motor.motor_asyncio
import tracemalloc
from schemas import schemas

tracemalloc.start()


async def clean_db_before_tests():
    """Deletes all previous data in test db"""
    db_name = config("TEST_DB_NAME")
    mongo_url = config("MONGO_DB_TEST_URI")

    # Connessione al database
    client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
    db = client[db_name]

    collections = await db.list_collection_names()

    # Delete all collections in test db
    for collection_name in collections:
        db[collection_name].drop()


class SharedTestData:
    tokens: dict = {}
    roles_schemas: dict = {
        schemas.User.ADMIN.value: schemas.AdminBase,
        schemas.User.TEACHER.value: schemas.TeacherBase,
        schemas.User.STUDENT.value: schemas.StudentBase,
        schemas.User.RELATIVE.value: schemas.RelativeBase,
    }


if __name__ == "__main__":
    loader = unittest.TestLoader()

    # Preliminary deletion of previous tests data
    asyncio.run(clean_db_before_tests())

    # Load tests fot User's CRUD Operation
    user_create = loader.loadTestsFromName(
        "test.test_users.test_create_users.TestUserCreate"
    )
    user_read = loader.loadTestsFromName("test.test_users.test_read_users.TestUserRead")
    user_update = loader.loadTestsFromName(
        "test.test_users.test_update_users.TestUserUpdate"
    )
    user_delete = loader.loadTestsFromName(
        "test.test_users.test_delete_users.TestUserDelete"
    )

    users_crud = unittest.TestSuite([user_create, user_read, user_update, user_delete])

    user_create = loader.loadTestsFromName(
        "test.test_users.test_create_users.TestUserCreate"
    )
    classes_create = loader.loadTestsFromName(
        "test.test_classes.test_create_classes.TestClassesCreate"
    )

    classes_crud = unittest.TestSuite([user_create, classes_create])

    # # Run the combined suite
    runner = unittest.TextTestRunner()
    runner.run(users_crud)

    runner = unittest.TextTestRunner()
    runner.run(classes_crud)
