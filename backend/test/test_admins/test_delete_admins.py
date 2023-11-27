from datetime import datetime
from schemas import schemas, custom_types
import unittest
import aiohttp
from datetime import datetime
from test.test_main import SharedTestData


class TestAdminsDelete(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Prepare some static data"""
        self.headers = {
            "X-Test-Env": "true",
            "Content-Type": "application/json",
            "Authorization": "Bearer ",
        }
        self.url = "http://backend:80/admins"
        self.valid_search_query = {
            "name": "TestAdminUpdateName",
            "surname": "TestAdminUpdateSurname",
            "details": ["Some Details"],
        }

        self.invalid_search_queries = [
            {**self.valid_search_query, f"invalid_{x}": self.valid_search_query[x]}
            for x in self.valid_search_query.keys()
        ]

        self.valid_query_no_result = {
            "name": "NameNotIndB",
        }

    def get_valid_search_query(
        self, role: str = schemas.User.TEACHER.value, multi: bool = False
    ):
        return {
            "user_role": role,
            "multi": str(multi),
        }

    async def delete(
        self,
        token: str = "",
        search_query: dict = None,
        multi: bool = False,
        debug: bool = False,
        user_role: str = schemas.User.TEACHER.value,
    ):
        self.headers["Authorization"] = f"Bearer {token}"

        user_id = SharedTestData.user_role_id[user_role]
        params = (
            search_query
            if search_query
            else self.get_valid_search_query(role=user_role, multi=multi)
        )

        async with aiohttp.ClientSession() as session:
            response = await session.delete(
                f"{self.url}/{user_id}",
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

    async def test_fail_delete_admins(self):
        """Delete Admins - Fail"""

        # Only admins can delete scores otherwise the api should return 401
        for role in custom_types.User:
            token = SharedTestData.tokens[role.value]
            if role.value != custom_types.User.ADMIN.value:
                status, _ = await self.delete(token=token, debug=False)
                assert status == 401

        # One field wrong must cause Unprocessasble entity 422
        role = custom_types.User.ADMIN.value
        token = SharedTestData.tokens[role]
        for invalid_query in self.invalid_search_queries:
            status, _ = await self.delete(
                token=token,
                search_query=invalid_query,
            )
            assert status == 422

    async def test_pass_delete_scores(self):
        """Delete Admins - Pass"""
        # Single delete
        role = custom_types.User.ADMIN.value
        token = SharedTestData.tokens[role]
        status, _ = await self.delete(
            token=token,
        )
        assert status == 200
        # # Multi delete
        # role = custom_types.User.ADMIN.value
        # token = SharedTestData.tokens[role]
        # status, _ = await self.delete(
        #     token=token,
        #     multi=True,
        # )
        # assert status == 200
