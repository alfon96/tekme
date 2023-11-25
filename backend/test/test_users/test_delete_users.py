from datetime import datetime
from schemas import schemas, custom_types
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData


class TestUserDelete(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.headers = {"X-Test-Env": "true", "Content-Type": "application/json"}
        self.url = "http://backend:80/users/"
        self.params = {"password": "testPassword1!"}

    async def delete(
        self, token: str = None, password: str = None, debug: bool = False
    ):
        "A not valid input user_role should return 422"
        if token:
            self.headers.update({"Authorization": f"Bearer {token}"})
        params = self.params if not password else {"password": password}

        async with aiohttp.ClientSession() as session:
            response = await session.delete(
                self.url, headers=self.headers, params=params
            )
            if debug:
                SharedTestData.debug_print(
                    self.headers,
                    params,
                    response.status,
                )
            return response.status, await response.json()

    async def test_fail_delete_user(self):
        """Delete User - Fail"""
        # No token
        status, _ = await self.delete(token=None)
        assert status == 401

        # Invalid token
        status, _ = await self.delete(token="Invalid Token")
        assert status == 401

        # Invalid password
        for role in custom_types.User:
            token: str = SharedTestData.tokens[role.value]
            status, _ = await self.delete(token=token, password="Password1!Invalid")
            assert status == 401

    async def test_pass_delete_user(self):
        """Delete User - Pass"""
        # Valid token & Valid Passwords
        for role in custom_types.User:
            token = SharedTestData.tokens[role.value]
            SharedTestData.tokens[role] = {}
            status, _ = await self.delete(token, debug=False)
            assert status == 200
