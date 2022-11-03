import httpx
import pytest


@pytest.mark.asyncio
async def test_sign_up(default_client: httpx.AsyncClient) -> None:
    payload = {
        "email": "test@test.com",
        "password": "stringtest"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    test_response = {
        "Message": "User Successfully Signed Up"
    }

    response = await default_client.post("/user/signup", json=payload,
                                         headers=headers)
    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_sign_in(default_client: httpx.AsyncClient) -> None:
    payload = {
        "username": "test@test.com",
        "password": "stringtest"
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = await default_client.post("/user/signin", data=payload,
                                         headers=headers)
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"
