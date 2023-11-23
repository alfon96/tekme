from datetime import datetime
from schemas import schemas
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData
from typing import Union
from utils.setup import Setup


class TestUserCreate(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.valid_user_data = {
            "name": "TestName",
            "surname": "TestSurname",
            "birthday": datetime.now().isoformat(),
            "email": "test@test.com",
            "password": "testPassword1!",
            "phone": "+393715485996",
            "profile_pic": "",
        }
        self.invalid_user_data = [
            {
                k if k != key else f"invalid_{k}": v
                for k, v in self.valid_user_data.items()
            }
            for key in self.valid_user_data
        ]

        self.details = ({"details": []},)
        self.subjects = ({"subjects": []},)
        self.headers = {"X-Test-Env": "true"}
        self.url = "http://backend:80/users/signup"

    async def create(self, json: dict, user_role: str):
        params = {"user_role": user_role}

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                self.url, headers=self.headers, json=json, params=params
            )
            return response.status, await response.json()

    async def test_fail_signup(self):
        """Create User - Fail"""

        # A not valid input user_role should return 401
        json = {
            "user_data": self.valid_user_data,
            "details": ["Some details"],
            "subjects": ["Some Subects"],
        }
        status, _ = await self.create(json=json, user_role="Invalid Role")
        assert status == 422

        # Any incorrect field in the user_data should return 422
        for invalid_user_data in self.invalid_user_data:
            json = {
                "user_data": invalid_user_data,
                "details": ["Some details"],
                "subjects": ["Some Subects"],
            }
            for role in schemas.User:
                status, _ = await self.create(
                    json=json,
                    user_role=role.value,
                )
                assert status == 422

        # Teachers without subjects field should return 422
        json = {
            "user_data": self.valid_user_data,
            "details": [],
            "subjects": [],
        }
        status, _ = await self.create(
            json=json,
            user_role=schemas.User.TEACHER.value,
        )
        assert status == 422

    async def test_pass_signup(self):
        """Create User - Pass"""

        # Check for all roles
        for role in schemas.User:
            subjects = ["Maths"] if role.value == schemas.User.TEACHER.value else []
            json = {
                "user_data": self.valid_user_data,
                "details": ["Some Details"],
                "subjects": subjects,
            }

            status, json = await self.create(
                json=json,
                user_role=role.value,
            )

            token = json.get("token")
            assert status == 200
            assert token is not None
            SharedTestData.tokens[role] = token

        async def asyncTearDown(self):
            # Any teardown code needed for the tests
            pass
