from datetime import datetime
from schemas import schemas, custom_types
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData


class TestUserUpdate(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.headers = {"X-Test-Env": "true"}
        self.url = "http://backend:80/users/"
        self.valid_update_single_query = {
            "name": "SingleUpdateTest_NewName",
        }
        self.valid_update_multi_query = {
            "surname": "MultiUpdateTest_NewSurname",
            "profile_pic": "http://multi.update.test.query.com",
        }

        self.update_query = {
            "name": "TestName",
            "surname": "TestSurname",
            "birthday": datetime.now().isoformat(),
            "email": "test@test.com",
            "phone": "+393715485996",
            "profile_pic": "",
        }
        self.invalid_update_queries = [
            {
                ("invalid_" + key if key == x else key): value
                for key, value in self.update_query.items()
            }
            for x in self.update_query
        ]

    async def update(self, json: dict = {}, token: str = None, debug: bool = False):
        """A not valid input user_role should return 422"""
        if token:
            self.headers.update({"Authorization": f"Bearer {token}"})

        async with aiohttp.ClientSession() as session:
            response = await session.patch(self.url, headers=self.headers, json=json)
            if debug:
                SharedTestData.debug_print(
                    self.headers,
                    json,
                    response.status,
                )
            return response.status, await response.json()

    async def test_fail_update_user(self):
        """Update User - Fail"""
        # Invalid Token
        status, _ = await self.update(
            token="Invalid Token", json=self.valid_update_single_query
        )
        assert status == 401

        # Invalid parameters, correct token but just one key wrong
        for role in custom_types.User:
            for invalid_update_query in self.invalid_update_queries:
                token = SharedTestData.tokens[role.value]

                status, _ = await self.update(
                    token=token,
                    json=invalid_update_query,
                    debug=False,
                )
                assert status == 422

    async def test_pass_update_user(self):
        """Update User - Pass"""

        for role in custom_types.User:
            token = SharedTestData.tokens[role]

            status, _ = await self.update(
                token=token,
                json=self.valid_update_single_query,
                debug=False,
            )

            assert status == 200

        # Multi Values Update
        for role in custom_types.User:
            status, _ = await self.update(
                token=SharedTestData.tokens[role],
                json=self.valid_update_multi_query,
                debug=False,
            )
            assert status == 200
