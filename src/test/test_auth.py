import pytest
from fastapi import status

@pytest.mark.anyio
async def test_user_registration_and_login_flow(client):
    user_payload = {
        "email": "user_il@example.com",
        "password": "sring",
        "role": "customer"
            }

    register_response = await client.post("/api/v1/auth/register",json=user_payload)
    assert register_response.status_code == status.HTTP_201_CREATED
    assert register_response.json()["email"] == user_payload["email"]
    assert "id" in register_response.json()

    duplicate_response = await client.post("/api/v1/auth/register",json=user_payload)
    assert duplicate_response.status_code == status.HTTP_400_BAD_REQUEST

    login_response = await client.post("/api/v1/auth/login",json=user_payload)
    assert login_response.status_code == status.HTTP_200_OK
    assert login_response.json()["token_type"] == "bearer"
    assert "access_token" in login_response.json()