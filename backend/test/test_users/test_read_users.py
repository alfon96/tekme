from datetime import datetime
from schemas import schemas
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData


class TestUserRead(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.headers = {"X-Test-Env": "true", "Content-Type": "application/json"}
        self.url = "http://backend:80/users/"

    async def read(self, token: str = None):
        "A not valid input user_role should return 422"
        if token:
            self.headers.update({"Authorization": f"Bearer {token}"})

        async with aiohttp.ClientSession() as session:
            response = await session.get(self.url, headers=self.headers)
            return response.status, await response.json()

    async def test_fail_read_user(self):
        """Read User - Fail"""
        # No token
        status, _ = await self.read(token=None)
        assert status == 401

        # Invalid token
        status, _ = await self.read(token="Invalid Token")
        assert status == 401

    async def test_pass_read_user(self):
        # Valid token
        for role in schemas.User:
            token = SharedTestData.tokens[role.value]
            status, _ = await self.read(token)

            assert status == 200
