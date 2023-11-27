from datetime import datetime
from schemas import schemas, custom_types
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData


class TestScoresRead(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.headers = {
            "X-Test-Env": "true",
            "Content-Type": "application/json",
            "Authorization": "Bearer ",
        }
        self.url = "http://backend:80/scores/"

        self.valid_query = {
            "classes": 6,
            "breaks": 8,
            "students_id": "some-student-id",
        }

        self.invalid_queries = [
            {
                "invalid_" + key: value if key == k else self.valid_query[k]
                for k, value in self.valid_query.items()
            }
            for key in self.valid_query
        ]

        self.valid_query_no_result = {
            "classes": 6,
            "breaks": 8,
            "students_id": "some-student-fake-id",
        }

    async def read(
        self,
        token: str = "",
        search_query: dict = None,
        multi: bool = False,
        debug: bool = False,
    ):
        """Read Endpoint"""
        query = search_query if search_query else self.valid_query
        params = f"query={SharedTestData.encode_queries(query)}&multi={multi}"

        self.headers["Authorization"] = f"Bearer {token}"
        async with aiohttp.ClientSession() as session:
            response = await session.get(self.url, headers=self.headers, params=params)
            if debug:
                SharedTestData.debug_print(token, params, query, response.status)
            return response.status, await response.json()

    async def test_fail_read_classes(self):
        """Read Classes - Fail"""

        # Only logged users can read classes otherwise the api should return 401
        token = "Invalid Token"
        status, _ = await self.read(token=token)
        assert status == 401

        # One field wrong must cause Unprocessasble entity 422
        for role in custom_types.User:
            token = SharedTestData.tokens[role.value]
            for invalid_query in self.invalid_queries:
                status, _ = await self.read(
                    token=token,
                    search_query=invalid_query,
                )
                assert status == 422

    async def test_pass_read_classes(self):
        """Read Classes - Pass"""

        for role in custom_types.User:
            token = SharedTestData.tokens[role.value]
            status, score_data = await self.read(
                token=token,
                debug=False,
            )
            assert score_data != None

            data_obj = schemas.ThingsFactory.create_thing(
                thing=schemas.Data.SCORE.value,
                data=score_data["results"],
            )
            assert data_obj != None

            assert status == 200

        token = SharedTestData.tokens[custom_types.User.TEACHER.value]
        status, score_data = await self.read(
            token=token,
            search_query=self.valid_query_no_result,
            debug=False,
        )
        assert status == 404
