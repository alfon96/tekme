from datetime import datetime
from schemas import schemas, custom_types
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData


class TestClassesDelete(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.headers = {
            "X-Test-Env": "true",
            "Content-Type": "application/json",
            "Authorization": "Bearer ",
        }
        self.url = "http://backend:80/classes/"
        self.valid_query = {
            "name": "B",
            "grade": 2,
            "students_id": ["Some-students-id"],
        }
        self.valid_query_id: str = SharedTestData
        self.invalid_queries = [
            {**self.valid_query, f"invalid_{x}": self.valid_query[x]}
            for x in self.valid_query.keys()
        ]

    async def delete(
        self,
        token: str = "",
        deletion_query: dict = None,
        multi: bool = False,
        debug: bool = False,
    ):
        self.headers["Authorization"] = f"Bearer {token}"
        query = deletion_query if deletion_query else self.valid_query
        params = f"query={SharedTestData.encode_queries(query)}&multi={multi}"

        async with aiohttp.ClientSession() as session:
            response = await session.delete(
                self.url,
                headers=self.headers,
                params=params,
            )
            if debug:
                SharedTestData.debug_print(
                    self.headers,
                    params,
                    response.status,
                )
            return response.status, await response.json()

    async def test_fail_delete_classes(self):
        """Create Classes - Delete"""

        # Only admins can delete classes otherwise the api should return 401
        for role in custom_types.User:
            token = SharedTestData.tokens[role.value]
            if role.value != custom_types.User.ADMIN.value:
                status, _ = await self.delete(token=token)
                assert status == 401

        # One field wrong must cause Unprocessasble entity 422
        role = custom_types.User.ADMIN.value
        token = SharedTestData.tokens[role]
        for invalid_query in self.invalid_queries:
            status, _ = await self.delete(
                token=token,
                deletion_query=invalid_query,
            )
            assert status == 422

    async def test_pass_delete_classes(self):
        """Create Classes - Pass"""
        # Single delete
        role = custom_types.User.ADMIN.value
        token = SharedTestData.tokens[role]
        status, _ = await self.delete(
            token=token,
        )
        assert status == 200
        # Multi delete
        role = custom_types.User.ADMIN.value
        token = SharedTestData.tokens[role]
        status, _ = await self.delete(
            token=token,
            multi=True,
        )
        assert status == 200
