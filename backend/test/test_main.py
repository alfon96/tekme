import unittest
import asyncio
from decouple import config
import motor.motor_asyncio
import tracemalloc
from schemas import schemas, custom_types
import json
import urllib.parse

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
    scores_id: str = ""
    user_role_id = {}

    debug_print = lambda *args: [print(x) for x in args]

    def encode_queries(input_query: dict) -> str:
        # Serializza l'intero dizionario in una stringa JSON
        json_string = json.dumps(input_query)

        # Codifica la stringa JSON per l'utilizzo nell'URL
        encoded_query = urllib.parse.quote(json_string)

        return encoded_query


def create_test_suite(*args):
    loader = unittest.TestLoader()
    tests_list = [loader.loadTestsFromName(x) for x in args]
    test_suite = unittest.TestSuite(tests_list)
    return test_suite


def run_test_suite(test_suite):
    runner = unittest.TextTestRunner()
    runner.run(test_suite)


if __name__ == "__main__":
    # Preliminary deletion of previous tests data
    asyncio.run(clean_db_before_tests())

    # ------- Tests Configuration -------

    # USER - CRUD
    user_create = "test.test_users.test_create_users.TestUserCreate"
    user_read = "test.test_users.test_read_users.TestUserRead"
    user_update = "test.test_users.test_update_users.TestUserUpdate"
    user_delete = "test.test_users.test_delete_users.TestUserDelete"

    users_crud_suite = create_test_suite(
        user_create,
        user_read,
        user_update,
        user_delete,
    )

    # CLASSES - CRUD
    classes_create = "test.test_classes.test_create_classes.TestClassesCreate"
    classes_read = "test.test_classes.test_read_classes.TestClassesRead"
    classes_update = "test.test_classes.test_update_classes.TestClassesUpdate"
    classes_delete = "test.test_classes.test_delete_classes.TestClassesDelete"

    classes_crud_suite = create_test_suite(
        user_create,
        classes_create,
        classes_read,
        classes_update,
        classes_delete,
    )

    # SCORES - CRUD
    scores_create = "test.test_scores.test_create_scores.TestScoresCreate"
    scores_read = "test.test_scores.test_read_scores.TestScoresRead"
    scores_update = "test.test_scores.test_update_scores.TestScoresUpdate"
    scores_delete = "test.test_scores.test_delete_scores.TestScoresDelete"

    scores_crud_suite = create_test_suite(
        user_create,
        scores_create,
        scores_read,
        scores_update,
        scores_delete,
    )

    # ADMINS - UD
    admins_update = "test.test_admins.test_update_admins.TestAdminsUpdate"
    admins_delete = "test.test_admins.test_delete_admins.TestAdminsDelete"

    admins_crud_suite = create_test_suite(
        user_create,
        admins_update,
        admins_delete,
    )

    # ------- Start Tests -------
    # run_test_suite(users_crud_suite)
    # run_test_suite(classes_crud_suite)
    # run_test_suite(scores_crud_suite)
    run_test_suite(admins_crud_suite)
