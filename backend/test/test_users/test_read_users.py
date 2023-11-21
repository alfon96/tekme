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
            return await session.get(self.url, headers=self.headers)

    async def test_fail_read_user(self):
        """Read User - Fail"""
        # No token
        response = await self.read(token=None)
        assert response.status == 401

        # Invalid token
        response = await self.read(token="Invalid Token")
        assert response.status == 401

    async def test_pass_read_user(self):
        # Valid token
        for role in schemas.User:
            token = SharedTestData.tokens[role.value]
            response = await self.read(token)
            content = await response.json()

            schema_class = SharedTestData.roles_schemas[role.value]
            schema_instance = schema_class(**content["user"])

            assert response.status == 200
            assert isinstance(schema_instance, schema_class)
