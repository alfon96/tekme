from datetime import datetime
from schemas import schemas
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData


class TestClassesRead(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.headers = {
            "X-Test-Env": "true",
            "Content-Type": "application/json",
            "Authorization": "Bearer ",
        }
        self.url = "http://backend:80/classes/"
        self.valid_query = {
            "name": "A",
            "grade": 1,
        }
        self.invalid_queries = [
            {
                "invalid_" + key: value if key == k else self.valid_query[k]
                for k, value in self.valid_query.items()
            }
            for key in self.valid_query
        ]

    async def read(self, token: str = "", search_query: dict = None):
        params = self.valid_query if not search_query else search_query

        self.headers["Authorization"] = f"Bearer {token}"
        async with aiohttp.ClientSession() as session:
            response = await session.get(self.url, headers=self.headers, params=params)
            return response.status, await response.json()

    async def test_fail_read_classes(self):
        """Read Classes - Fail"""

        # Only logged users can read classes otherwise the api should return 401
        token = "Invalid Token"
        status, _ = await self.read(token=token)
        assert status == 401

        # One field wrong must cause Unprocessasble entity 422
        for role in schemas.User:
            token = SharedTestData.tokens[role.value]
            for invalid_query in self.invalid_queries:
                status, _ = await self.read(
                    token=token,
                    search_query=invalid_query,
                )
                assert status == 422

    async def test_pass_read_classes(self):
        """Read Classes - Pass"""

        for role in schemas.User:
            token = SharedTestData.tokens[role.value]
            status, _ = await self.read(
                token=token,
            )
            assert status == 200
