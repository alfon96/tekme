from datetime import datetime
from schemas import schemas
import pytest
from test_main import make_http_request
from utils.encryption import read_token


@pytest.mark.asyncio
async def succesful_signup(response):
    """Helper method to check for user creation response"""
    assert response.status_code == 200
    assert response.json().get("token") is not None
    assert response.json().get("message") == "User created successfully"


@pytest.mark.asyncio
async def succesful_signin(response):
    """Helper method to check for user creation response"""
    assert response.status_code == 200
    assert response.json().get("token") is not None


""" Testing CRUD Operations for Users"""


# Create an account


@pytest.mark.asyncio
async def test_fail_signup():
    """Create User - Pass Signup."""
    correct_user_data = {
        "name": "TestName",
        "surname": "TestSurname",
        "birthday": datetime.now().isoformat(),
        "email": "test@test.com",
        "password": "testPassword1!",
        "phone": "+393715485996",
        "profile_pic": "",
    }

    # Teacher with no subject can't signup
    url = "/users/signup"
    params = {"user_role": f"{schemas.User.TEACHER.value}"}
    headers = {"X-Test-Env": "true"}
    json = {"user_data": correct_user_data, "details": [], "subjects": []}

    response = await make_http_request(
        method="POST", url=url, headers=headers, json=json, params=params
    )
    assert response.status_code == 422

    # One field missing must fail, except for image_pic which is Optional
    incorrect_user_data = [
        {**correct_user_data, x: ""}
        for x in correct_user_data.keys()
        if x != "profile_pic"
    ]

    for json in incorrect_user_data:
        response = await make_http_request(
            method="POST", url=url, headers=headers, json=json, params=params
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_pass_signup():
    """Create User - Check that each type of user can signup and receive a token"""

    correct_user_data = {
        "name": "TestName",
        "surname": "TestSurname",
        "birthday": datetime.now().isoformat(),
        "email": "test@test.com",
        "password": "testPassword1!",
        "phone": "+393715485996",
        "profile_pic": "",
    }

    # Check for teachers
    params = {"user_role": f"{schemas.User.TEACHER.value}"}
    url = "/users/signup"
    headers = {"X-Test-Env": "true"}
    json = {"user_data": correct_user_data, "details": [], "subjects": ["Maths"]}

    response = await make_http_request(
        method="POST", url=url, headers=headers, json=json, params=params
    )

    await succesful_signup(response)

    # Check for students with or without details it pass
    json = {"user_data": correct_user_data, "details": ["Loves Art"], "subjects": []}
    params = {"user_role": f"{schemas.User.STUDENT.value}"}

    response = await make_http_request(
        method="POST", url=url, headers=headers, json=json, params=params
    )

    await succesful_signup(response)

    # Without details
    json = {"user_data": correct_user_data, "details": [], "subjects": []}
    params = {"user_role": f"{schemas.User.STUDENT.value}"}

    response = await make_http_request(
        method="POST", url=url, headers=headers, json=json, params=params
    )

    await succesful_signup(response)

    # Check for relatives
    params = {"user_role": f"{schemas.User.RELATIVE.value}"}
    response = await make_http_request(
        method="POST", url=url, headers=headers, json=json, params=params
    )

    await succesful_signup(response)


@pytest.mark.asyncio
async def test_pass_signin():
    """Pass Authentication."""

    json = {"email": "test@test.com", "password": "testPassword1!", "role": "teachers"}
    url = "/users/signin"
    headers = {"X-Test-Env": "true"}

    response = await make_http_request(
        method="POST", url=url, headers=headers, json=json
    )

    await succesful_signin(response)
    return response.json().get("token")


@pytest.mark.asyncio
async def test_fail_read_user():
    """Read User"""
    # Fails because the token is invalid
    url = "/users/"
    headers = {"Authorization": "Bearer invalid_token", "X-Test-Env": "true"}

    response = await make_http_request(method="GET", url=url, headers=headers)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_pass_read_user():
    """Read User"""
    token = await test_pass_signin()
    url = "/users/"
    payload = await read_token(token)
    headers = {"X-Test-Env": "true", "Authorization": f"Bearer {token}"}

    response = await make_http_request(method="GET", url=url, headers=headers)
    assert response.status_code == 200

    # Parse the response data
    user_data = response.json()

    user_role = payload["role"]
    # Check if the data matches one of the expected schema types
    if user_role == schemas.User.TEACHER.value:
        schemas.TeacherBase(**user_data)  # Validates data against the schema
    elif user_role == schemas.User.STUDENT.value:
        schemas.StudentBase(**user_data)
    elif user_role == schemas.User.RELATIVE.value:
        schemas.RelativeBase(**user_data)
    else:
        pytest.fail("User role not recognized in response data")
