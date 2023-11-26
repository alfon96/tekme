from datetime import datetime
from schemas import schemas, custom_types
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData
import json as json_
import urllib.parse
import datetime


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
            "creation": datetime.datetime.now().isoformat(),
        }
        self.invalid_classes_data = [
            {**self.valid_classes_data, f"invalid_{x}": self.valid_classes_data[x]}
            for x in self.valid_classes_data.keys()
        ]

    async def create(
        self, token: str = "", class_data: dict = None, debug: bool = False
    ):
        json = self.valid_classes_data if not class_data else class_data

        self.headers["Authorization"] = f"Bearer {token}"

        async with aiohttp.ClientSession() as session:
            response = await session.post(self.url, headers=self.headers, json=json)
            if debug:
                SharedTestData.debug_print(token, json, response.status)
            return response.status, await response.json()

    def generate_encoded_query_string(query_params):
        # Convert the dictionary to a JSON string
        json_string = json_.dumps(query_params)

        # URL-encode the JSON string
        encoded_string = urllib.parse.quote(json_string)

        return encoded_string

    async def test_fail_create_classes(self):
        """Create Classes - Fail"""

        # All token but the admin's with correct class data should return 401
        for role in custom_types.User:
            token = SharedTestData.tokens[role.value]
            if role.value != custom_types.User.ADMIN.value:
                status, _ = await self.create(token=token)
                assert status == 401

        # One field wrong must cause Unprocessasble entity 422
        role = custom_types.User.ADMIN.value
        token = SharedTestData.tokens[role]
        for invalid_class_data in self.invalid_classes_data:
            status, _ = await self.create(
                token=token,
                class_data=invalid_class_data,
            )
            assert status == 422

    async def test_pass_create_classes(self):
        """Create Classes - Pass"""
        # Create one class
        token = SharedTestData.tokens[custom_types.User.ADMIN.value]

        status, json = await self.create(
            token=token,
            debug=False,
        )
        id = json.get("id")

        assert id != None
        SharedTestData.classes_id = id
        assert status == 200

        # Create N classes
        token = SharedTestData.tokens[custom_types.User.ADMIN.value]
        class_data = [self.valid_classes_data for x in range(5)]
        status, json = await self.create(
            token=token,
            class_data=class_data,
            debug=False,
        )
        ids = [item.get("id") for item in json]

        assert len(ids) > 0
        SharedTestData.classes_id = id
        assert status == 200
