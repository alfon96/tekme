from datetime import datetime
from schemas import schemas
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

    async def delete(self, token: str = None, password: str = None):
        "A not valid input user_role should return 422"
        if token:
            self.headers.update({"Authorization": f"Bearer {token}"})
        params = self.params if not password else {"password": password}

        async with aiohttp.ClientSession() as session:
            return await session.delete(self.url, headers=self.headers, params=params)

    async def test_fail_delete_user(self):
        """Delete User - Fail"""
        # No token
        response = await self.delete(token=None)
        assert response.status == 401

        # Invalid token
        response = await self.delete(token="Invalid Token")
        assert response.status == 401

        # Invalid password
        for role in schemas.User:
            token: str = SharedTestData.tokens[role.value]
            response = await self.delete(token=token, password="Password1!Invalid")
            assert response.status == 401

    async def test_pass_delete_user(self):
        """Delete User - Pass"""
        # Valid token & Valid Passwords
        for role in schemas.User:
            token = SharedTestData.tokens[role.value]
            SharedTestData.tokens[role] = {}
            response = await self.delete(token)
            assert response.status == 200
