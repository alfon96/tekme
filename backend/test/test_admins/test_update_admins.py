from datetime import datetime
from schemas import schemas, custom_types
import unittest
import aiohttp
from test.test_main import SharedTestData
import datetime


class TestAdminsUpdate(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.headers = {
            "X-Test-Env": "true",
            "Content-Type": "application/json",
            "Authorization": "Bearer ",
        }
        self.url = "http://backend:80/admins"

        self.valid_update_query = {
            "name": "TestAdminUpdateName",
            "surname": "TestAdminUpdateSurname",
            "phone": "+393711659555",
        }

        self.invalid_search_query = {
            "user_role": "Invalid Role",
            "multi": "True",
        }

        self.invalid_update_queries = [
            {
                "invalid_" + key: value if key == k else self.valid_update_query[k]
                for k, value in self.valid_update_query.items()
            }
            for key in self.valid_update_query
        ]

    def get_valid_search_query(
        self, role: str = schemas.User.TEACHER.value, multi: bool = False
    ):
        return {
            "user_role": role,
            "multi": str(multi),
        }

    async def update(
        self,
        token: str = "",
        search_query: dict = None,
        user_role: str = schemas.User.TEACHER.value,
        json: dict = {},
        multi: bool = False,
        debug: bool = False,
    ):
        """Update Endpoint"""

        self.headers["Authorization"] = f"Bearer {token}"
        user_id = SharedTestData.user_role_id[user_role]

        params = (
            search_query
            if search_query
            else self.get_valid_search_query(role=user_role, multi=multi)
        )

        json = json if json else self.valid_update_query

        async with aiohttp.ClientSession() as session:
            response = await session.patch(
                f"{self.url}/{user_id}", headers=self.headers, params=params, json=json
            )
            if debug:
                SharedTestData.debug_print(
                    self.headers, params, json, response.status, await response.json()
                )
            return response.status, await response.json()

    async def test_fail_update_admins(self):
        """Update Admin - Fail"""

        # Only Admins can update other users otherwise should return 401
        token = "Invalid Token"
        status, _ = await self.update(token=token, debug=False)
        assert status == 401

        for role in custom_types.User:
            if role.value != custom_types.User.ADMIN:
                token = SharedTestData.tokens[role.value]
                status, _ = await self.update(token=token, debug=False)
                assert status == 401

        # One field wrong in search_query must cause Unprocessasble entity 422
        token = SharedTestData.tokens[custom_types.User.ADMIN.value]
        status, _ = await self.update(
            token=token,
            search_query=self.invalid_search_query,
            debug=False,
        )

        assert status == 422

        # One field wrong in update_query must cause Unprocessasble entity 422
        token = SharedTestData.tokens[custom_types.User.ADMIN.value]
        for invalid_update_query in self.invalid_update_queries:
            status, _ = await self.update(
                token=token, json=invalid_update_query, debug=False
            )

            assert status == 422

    async def test_pass_update_admins(self):
        """Update Admin - Pass"""

        "Single Update"
        token = SharedTestData.tokens[custom_types.User.ADMIN.value]
        for role in schemas.User:
            if role.value != schemas.User.ADMIN.value:
                status, _ = await self.update(
                    token=token,
                    debug=False,
                    user_role=role.value,
                )
                assert status == 200

        # "Multi Update"
        # for role in schemas.User:
        #     if role.value != schemas.User.ADMIN.value:
        #         status, _ = await self.update(
        #             token=token, debug=False, user_role=role.value, multi=True
        #         )
        #         assert status == 200
