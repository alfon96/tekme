from datetime import datetime
from schemas import schemas
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData


class TestClassesCreate(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.headers = {
            "X-Test-Env": "true",
            "Content-Type": "application/json",
            "Authorization": "Bearer ",
        }
        self.url = "http://backend:80/classes/"
        self.params = {"password": "testPassword1!"}
        self.valid_classes_data = {
            "name": "A",
            "grade": 1,
            "students_id": ["some-id"],
            "teachers_id": ["some-id", "some-id", "some-id"],
            "details": ["Scientific Focus"],
            "type": ["Experimental"],
        }
        self.invalid_classes_data = [
            {**self.valid_classes_data, x: ""}
            for x in self.valid_classes_data.keys()
            if x != "profile_pic"
        ]

    async def create(self, token: str = "", class_data: dict = None):
        json = self.valid_classes_data if not class_data else class_data

        self.headers["Authorization"] = f"Bearer {token}"

        async with aiohttp.ClientSession() as session:
            return await session.post(self.url, headers=self.headers, json=json)

    async def test_fail_create_classes(self):
        """Create Classes - Fail"""

        # All token but the admin's with correct class data should return 401
        for role in schemas.User:
            token = SharedTestData.tokens[role.value]
            if role.value != schemas.User.ADMIN.value:
                response = await self.create(token=token)
                assert response.status == 401

        # One field wrong must cause Unprocessasble entity 422
        role = schemas.User.ADMIN.value
        token = SharedTestData.tokens[role]
        for invalid_class_data in self.invalid_classes_data:
            response = await self.create(
                token=token,
                class_data=invalid_class_data,
            )
            assert response.status == 422

    async def test_pass_create_classes(self):
        """Create Classes - Pass"""

        role = schemas.User.ADMIN.value
        token = SharedTestData.tokens[role]
        response = await self.create(
            token=token,
        )
        assert response.status == 200
