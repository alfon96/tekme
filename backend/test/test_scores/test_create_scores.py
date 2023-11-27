from datetime import datetime
from schemas import schemas, custom_types
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData
import json as json_
import urllib.parse
import datetime


class TestScoresCreate(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.headers = {
            "X-Test-Env": "true",
            "Content-Type": "application/json",
            "Authorization": "Bearer ",
        }
        self.url = "http://backend:80/scores/"
        self.valid_scores_data = {
            "classes": 6,
            "breaks": 8,
            "date": "2023-11-27T12:31:14.703Z",
            "details": [],
            "students_id": "some-student-id",
            "creation": datetime.datetime.now().isoformat(),
        }
        self.invalid_scores_data = [
            {**self.valid_scores_data, f"invalid_{x}": self.valid_scores_data[x]}
            for x in self.valid_scores_data.keys()
        ]

    async def create(
        self, token: str = "", score_data: dict = None, debug: bool = False
    ):
        json = score_data if score_data else self.valid_scores_data
        self.headers["Authorization"] = f"Bearer {token}"

        async with aiohttp.ClientSession() as session:
            response = await session.post(self.url, headers=self.headers, json=json)
            if debug:
                SharedTestData.debug_print(token, json, response.status)
            return response.status, await response.json()

    async def test_fail_create_scores(self):
        """Create Scores - Fail"""

        # All token but the teacher's with correct class data should return 401
        for role in custom_types.User:
            token = SharedTestData.tokens[role.value]
            if role.value != custom_types.User.TEACHER.value:
                status, _ = await self.create(token=token)
                assert status == 401

        # One field wrong must cause Unprocessasble entity 422
        role = custom_types.User.TEACHER.value
        token = SharedTestData.tokens[role]
        for invalid_score_data in self.invalid_scores_data:
            status, _ = await self.create(
                token=token,
                score_data=invalid_score_data,
            )
            assert status == 422

    async def test_pass_create_scores(self):
        """Create Scores - Pass"""

        token = SharedTestData.tokens[custom_types.User.TEACHER.value]

        for _ in range(5):
            # Create multiple instance just for next tests
            status, json = await self.create(
                token=token,
                debug=False,
            )
            id = json.get("id")

            assert id != None
            SharedTestData.scores_id = id
            assert status == 200
