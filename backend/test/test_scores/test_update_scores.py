from datetime import datetime
from schemas import schemas, custom_types
import unittest
import aiohttp
from test.test_main import SharedTestData
import datetime


class TestScoresUpdate(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.headers = {
            "X-Test-Env": "true",
            "Content-Type": "application/json",
            "Authorization": "Bearer ",
        }
        self.url = "http://backend:80/scores/"

        self.valid_search_query = {
            "classes": 6,
            "breaks": 8,
            "students_id": "some-student-id",
        }
        self.valid_update_query = {
            "classes": 1,
            "breaks": 10,
            "details": [],
            "date": datetime.datetime.now().isoformat(),
            "teacher_id": "teachers-id",
            "students_id": ["some-id", "some-other-id"],
        }

        self.invalid_search_queries = [
            {
                "invalid_" + key: value if key == k else self.valid_search_query[k]
                for k, value in self.valid_search_query.items()
            }
            for key in self.valid_search_query
        ]

        self.invalid_update_queries = [
            {
                "invalid_" + key: value if key == k else self.valid_update_query[k]
                for k, value in self.valid_update_query.items()
            }
            for key in self.valid_update_query
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
        json = json if json else self.valid_update_query

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

    async def test_fail_update_scores(self):
        """Update Scores - Fail"""

        # Only Teachers can update scores otherwise should return 401
        token = "Invalid Token"
        status, _ = await self.update(token=token, json=self.valid_update_query)
        assert status == 401

        for role in custom_types.User:
            if role.value != custom_types.User.TEACHER:
                token = SharedTestData.tokens[role.value]
                status, _ = await self.update(
                    token=token, json=self.valid_update_query, debug=False
                )
                assert status == 401

        # One field wrong in search_query must cause Unprocessasble entity 422
        token = SharedTestData.tokens[custom_types.User.TEACHER.value]
        for invalid_query in self.invalid_search_queries:
            status, _ = await self.update(token=token, json=invalid_query, debug=False)

            assert status == 422

        # One field wrong in update_query must cause Unprocessasble entity 422
        token = SharedTestData.tokens[custom_types.User.TEACHER.value]
        for invalid_query in self.invalid_update_queries:
            status, _ = await self.update(
                token=token, search_query=invalid_query, debug=False
            )

            assert status == 422

    async def test_pass_update_scores(self):
        """Update Scores - Pass"""

        "Single Update"
        token = SharedTestData.tokens[custom_types.User.TEACHER.value]

        status, _ = await self.update(
            token=token,
            debug=False,
        )
        assert status == 200

        "Multi Update"
        status, _ = await self.update(
            token=token,
            multi=True,
            debug=False,
        )
        assert status == 200
