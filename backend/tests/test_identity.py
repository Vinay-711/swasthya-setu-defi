# pyre-ignore-all-errors
import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status

@pytest_asyncio.fixture
async def worker_identity(client: AsyncClient) -> dict:
    register_payload = {
        "email": "identity.worker@example.com",
        "password": "Worker@123",
        "role": "migrant_worker",
        "name": "Identity Worker",
        "phone": "9876543211",
        "language": "hi",
    }
    res = await client.post("/api/v1/auth/register", json=register_payload)
    assert res.status_code in (201, 409)
    
    if res.status_code == 201:
        token = res.json()["access_token"]
        user_id = res.json()["user"]["id"]
    else:
        login_res = await client.post(
            "/api/v1/auth/login",
            json={"email": register_payload["email"], "password": register_payload["password"]},
        )
        token = login_res.json()["access_token"]
        user_id = login_res.json()["user"]["id"]
    
    # Create identity
    identity_res = await client.post(
        "/api/v1/identity/create",
        json={"user_id": user_id},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert identity_res.status_code in (200, 201)
    
    return {
        "token": token,
        "swasthya_id": identity_res.json()["swasthya_id"],
        "user_id": user_id
    }


@pytest.mark.asyncio
async def test_link_abha_success(client: AsyncClient, worker_identity: dict) -> None:
    response = await client.post(
        f"/api/v1/identity/{worker_identity['swasthya_id']}/link-abha",
        json={"abha_number": "12345678901234"},
        headers={"Authorization": f"Bearer {worker_identity['token']}"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["abha_number"] == "12345678901234"


@pytest.mark.asyncio
async def test_link_abha_invalid_format(client: AsyncClient, worker_identity: dict) -> None:
    response = await client.post(
        f"/api/v1/identity/{worker_identity['swasthya_id']}/link-abha",
        json={"abha_number": "invalid-abha"},
        headers={"Authorization": f"Bearer {worker_identity['token']}"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_link_abha_unauthorized(client: AsyncClient, worker_identity: dict) -> None:
    response = await client.post(
        f"/api/v1/identity/{worker_identity['swasthya_id']}/link-abha",
        json={"abha_number": "12345678901234"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
