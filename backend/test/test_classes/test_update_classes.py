from datetime import datetime
from schemas import schemas, custom_types
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData


class TestClassesUpdate(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.headers = {
            "X-Test-Env": "true",
            "Content-Type": "application/json",
            "Authorization": "Bearer ",
        }
        self.url = "http://backend:80/classes/"
        self.valid_search_queries = {"name": "A", "grade": 1}
        self.valid_query = {
            "name": "B",
            "grade": 2,
            "students_id": [
                "Some-students-id",
                "Some-students-id",
                "Some-students-id",
                "Some-students-id",
            ],
            "teachers_id": [
                "Some-teachers-id",
                "Some-teachers-id",
            ],
            "details": ["some details"],
            "type": ["Art Focus"],
            "search_query": self.valid_search_queries,
        }

        self.params = {"multi": False}
        self.invalid_queries = [
            {
                "invalid_" + key: value if key == k else self.valid_query[k]
                for k, value in self.valid_query.items()
            }
            for key in self.valid_query
        ]

    async def update(self, token: str = "", multi: bool = False, json: dict = {}):
        self.params["multi"] = f"{multi}"
        self.headers["Authorization"] = f"Bearer {token}"

        async with aiohttp.ClientSession() as session:
            response = await session.patch(
                self.url, headers=self.headers, params=self.params, json=json
            )
            return response.status, await response.json()

    async def test_fail_update_classes(self):
        """Update Classes - Fail"""

        # Only admins can update classes otherwise should return 401
        token = "Invalid Token"
        status, _ = await self.update(token=token, json=self.valid_query)
        assert status == 401

        for role in custom_types.User:
            if role.value != custom_types.User.ADMIN:
                token = SharedTestData.tokens[role.value]
                status, _ = await self.update(token=token, json=self.valid_query)
                assert status == 401

        # One field wrong must cause Unprocessasble entity 422
        token = SharedTestData.tokens[custom_types.User.ADMIN.value]
        for invalid_query in self.invalid_queries:
            status, _ = await self.update(
                token=token,
                json=invalid_query,
            )

            assert status == 422

        # One field wrong in the search_query must cause Unprocessasble entity 422
        token = SharedTestData.tokens[custom_types.User.ADMIN.value]
        for invalid_query in self.invalid_queries:
            invalid_search_query = {**self.valid_query, "search_query": invalid_query}
            status, _ = await self.update(
                token=token,
                json=invalid_search_query,
            )
            assert status == 422

    async def test_pass_update_classes(self):
        """Update Classes - Pass"""

        "Single Update"
        token = SharedTestData.tokens[custom_types.User.ADMIN.value]

        status, _ = await self.update(token=token, json=self.valid_query)
        assert status == 200

        "Multi Update"
        status, _ = await self.update(token=token, json=self.valid_query, multi=True)
        assert status == 200
