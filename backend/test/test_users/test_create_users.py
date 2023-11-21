from datetime import datetime
from schemas import schemas
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData


class TestUserCreate(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.correct_user_data = {
            "name": "TestName",
            "surname": "TestSurname",
            "birthday": datetime.now().isoformat(),
            "email": "test@test.com",
            "password": "testPassword1!",
            "phone": "+393715485996",
            "profile_pic": "",
        }
        self.headers = {"X-Test-Env": "true"}
        self.url = "http://backend:80/users/signup"
        self.params = {"user_role": "invalid"}

    async def invalid_role(self):
        "A not valid input user_role should return 422"

        json = {"user_data": self.correct_user_data, "details": [], "subjects": []}

        async with aiohttp.ClientSession() as session:
            return await session.post(
                self.url, headers=self.headers, json=json, params=self.params
            )

    async def incorrect_user_data(self):
        "Any incorrect field in the user_data should return 422"
        incorrect_user_data = [
            {**self.correct_user_data, x: ""}
            for x in self.correct_user_data
            if x != "profile_pic"
        ]

        for json_data in incorrect_user_data:
            async with aiohttp.ClientSession() as session:
                yield await session.post(
                    self.url,
                    headers=self.headers,
                    json=json_data,
                    params=self.params,
                )

    async def user_signup(
        self,
        successful_teacher: bool = True,
        role: schemas.User = schemas.User.STUDENT.value,
    ):
        json = {"user_data": self.correct_user_data}
        if successful_teacher and role == schemas.User.TEACHER.value:
            json.update({"subjects": ["Maths"]})

        self.params["user_role"] = role

        async with aiohttp.ClientSession() as session:
            return await session.post(
                self.url, headers=self.headers, json=json, params=self.params
            )

    async def test_fail_signup(self):
        """Create User - Fail Signup."""

        # A not valid input user_role should return 401
        response = await self.invalid_role()
        assert response.status == 422

        # Any incorrect field in the user_data should return 422
        response = self.incorrect_user_data()
        async for response in self.incorrect_user_data():
            assert response.status == 422

        # Teachers without subjects field should return 422
        response = await self.user_signup(
            successful_teacher=False, role=schemas.User.TEACHER.value
        )
        async for response in self.incorrect_user_data():
            assert response.status == 422

    async def test_pass_signup(self):
        """Create User - Check that each type of user can signup and receive a token"""

        # Check for all roles
        for role in schemas.User:
            response = await self.user_signup(role=role.value)
            response_json = await response.json()
            token = response_json.get("token")
            assert response.status == 200
            assert token is not None
            SharedTestData.tokens[role] = token

        async def asyncTearDown(self):
            # Any teardown code needed for the tests
            pass
