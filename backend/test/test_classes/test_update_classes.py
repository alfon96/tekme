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

        self.valid_search_query = {
            "name": "A",
            "grade": 1,
            "students_id": ["some-id"],
        }
        self.update_query = {
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
        }

        self.invalid_update_queries = [
            {
                "invalid_" + key: value if key == k else self.update_query[k]
                for k, value in self.update_query.items()
            }
            for key in self.update_query
        ]

    async def update(
        self,
        token: str = "",
        search_query: dict = None,
        json: dict = {},
        multi: bool = False,
        debug: bool = False,
    ):
        """Update Endpoint"""
        self.headers["Authorization"] = f"Bearer {token}"
        query = search_query if search_query else self.valid_search_query
        params = f"query={SharedTestData.encode_queries(query)}&multi={multi}"

        async with aiohttp.ClientSession() as session:
            response = await session.patch(
                self.url, headers=self.headers, params=params, json=json
            )
            if debug:
                SharedTestData.debug_print(
                    self.headers,
                    params,
                    json,
                    response.status,
                )
            return response.status, await response.json()

    async def test_fail_update_classes(self):
        """Update Classes - Fail"""

        # Only admins can update classes otherwise should return 401
        token = "Invalid Token"
        status, _ = await self.update(token=token, json=self.update_query)
        assert status == 401

        for role in custom_types.User:
            if role.value != custom_types.User.ADMIN:
                token = SharedTestData.tokens[role.value]
                status, _ = await self.update(
                    token=token, json=self.update_query, debug=False
                )
                assert status == 401

        # One field wrong must cause Unprocessasble entity 422
        token = SharedTestData.tokens[custom_types.User.ADMIN.value]
        for invalid_query in self.invalid_update_queries:
            status, _ = await self.update(token=token, json=invalid_query, debug=False)

            assert status == 422

        # One field wrong in the search_query must cause Unprocessasble entity 422
        token = SharedTestData.tokens[custom_types.User.ADMIN.value]
        for invalid_query in self.invalid_update_queries:
            invalid_search_query = {**self.update_query, "search_query": invalid_query}
            status, _ = await self.update(
                token=token, json=invalid_search_query, debug=False
            )
            assert status == 422

    async def test_pass_update_classes(self):
        """Update Classes - Pass"""

        "Single Update"
        token = SharedTestData.tokens[custom_types.User.ADMIN.value]

        status, _ = await self.update(
            token=token,
            json=self.update_query,
            debug=False,
        )
        assert status == 200

        "Multi Update"
        status, _ = await self.update(token=token, json=self.update_query, multi=True)
        assert status == 200
