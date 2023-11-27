from datetime import datetime
from schemas import schemas, custom_types
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData


class TestScoresDelete(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.headers = {
            "X-Test-Env": "true",
            "Content-Type": "application/json",
            "Authorization": "Bearer ",
        }
        self.url = "http://backend:80/scores/"
        self.valid_search_query = {
            "classes": 1,
            "breaks": 10,
            "students_id": ["some-id", "some-other-id"],
        }

        self.invalid_search_queries = [
            {**self.valid_search_query, f"invalid_{x}": self.valid_search_query[x]}
            for x in self.valid_search_query.keys()
        ]

        self.valid_query_no_result = {
            "classes": 6,
            "breaks": 8,
            "students_id": "some-student-fake-id",
        }

    async def delete(
        self,
        token: str = "",
        deletion_query: dict = None,
        multi: bool = False,
        debug: bool = False,
    ):
        self.headers["Authorization"] = f"Bearer {token}"
        query = deletion_query if deletion_query else self.valid_search_query
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
                    query,
                    params,
                    response.status,
                )
            return response.status, await response.json()

    async def test_fail_delete_scores(self):
        """Delete Scores - Delete"""

        # Only teachers can delete scores otherwise the api should return 401
        for role in custom_types.User:
            token = SharedTestData.tokens[role.value]
            if role.value != custom_types.User.TEACHER.value:
                status, _ = await self.delete(token=token, debug=False)
                assert status == 401

        # One field wrong must cause Unprocessasble entity 422
        role = custom_types.User.TEACHER.value
        token = SharedTestData.tokens[role]
        for invalid_query in self.invalid_search_queries:
            status, _ = await self.delete(
                token=token,
                deletion_query=invalid_query,
            )
            assert status == 422

    async def test_pass_delete_scores(self):
        """Delete Scores - Pass"""
        # Single delete
        role = custom_types.User.TEACHER.value
        token = SharedTestData.tokens[role]
        status, _ = await self.delete(
            token=token,
        )
        assert status == 200
        # Multi delete
        role = custom_types.User.TEACHER.value
        token = SharedTestData.tokens[role]
        status, _ = await self.delete(
            token=token,
            multi=True,
        )
        assert status == 200
