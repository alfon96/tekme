import unittest
import asyncio
from decouple import config
import motor.motor_asyncio
import tracemalloc
from schemas import schemas, custom_types

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
        custom_types.User.ADMIN.value: schemas.AdminSensitiveData,
        custom_types.User.TEACHER.value: schemas.TeacherSensitiveData,
        custom_types.User.STUDENT.value: schemas.StudentSensitiveData,
        custom_types.User.RELATIVE.value: schemas.RelativeSensitiveData,
    }
    classes_id: str = ""

    debug_print = lambda x, y=None, z=None, t=None: (
        print(x),
        print(y),
        print(z),
        print(t),
    )


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

    users_crud = unittest.TestSuite(
        [
            user_create,
            user_read,
            user_update,
            user_delete,
        ]
    )

    user_create = loader.loadTestsFromName(
        "test.test_users.test_create_users.TestUserCreate"
    )
    # Create
    classes_create = loader.loadTestsFromName(
        "test.test_classes.test_create_classes.TestClassesCreate"
    )
    # Read
    classes_read = loader.loadTestsFromName(
        "test.test_classes.test_read_classes.TestClassesRead"
    )
    # Update
    classes_update = loader.loadTestsFromName(
        "test.test_classes.test_update_classes.TestClassesUpdate"
    )

    # Delete
    classes_delete = loader.loadTestsFromName(
        "test.test_classes.test_delete_classes.TestClassesDelete"
    )

    classes_crud = unittest.TestSuite(
        [
            user_create,
            classes_create,
            classes_read,
            classes_update,
            classes_delete,
        ]
    )

    # Run the combined suite
    runner = unittest.TextTestRunner()
    runner.run(users_crud)

    # runner = unittest.TextTestRunner()
    # runner.run(classes_crud)
