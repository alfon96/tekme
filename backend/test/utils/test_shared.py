# from schemas import schemas
# import pytest
# import httpx
# from main import app
# from test.test_config import TEST_ORDER

# pytestmark = pytest.mark.anyio

# class TestPreliminaryOperations(unittest.IsolatedAsyncioTestCase):


# @pytest.mark.asyncio
# async def successful_signup(response):
#     """Helper method to check for user creation response"""
#     assert response.status_code == 200
#     assert response.json().get("token") is not None
#     assert response.json().get("message") == "User created successfully"


# @pytest.mark.asyncio
# async def successful_signin(response):
#     """Helper method to check for user creation response"""
#     assert response.status_code == 200
#     assert response.json().get("token") is not None


# @pytest.mark.asyncio
# async def pass_signin(role: str = schemas.User.TEACHER.value):
#     """Pass Authentication."""

#     json = {"email": "test@test.com", "password": "testPassword1!", "role": role}
#     url = "/users/signin"
#     headers = {"X-Test-Env": "true"}

#     response = await make_http_request(
#         method="POST", url=url, headers=headers, json=json
#     )

#     await successful_signin(response)
#     return response.json().get("token")
