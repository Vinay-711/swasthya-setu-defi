# pyre-ignore-all-errors
import pytest
# pyre-ignore[21]
import pytest_asyncio
# pyre-ignore[21]
from httpx import AsyncClient
# pyre-ignore[21]
from fastapi import status
from unittest.mock import patch


@pytest_asyncio.fixture
async def otp_user(client: AsyncClient) -> None:
    register_payload = {
        "email": "otp.worker@example.com",
        "password": "Worker@123",
        "role": "migrant_worker",
        "name": "OTP Worker",
        "phone": "9876543210",
        "language": "hi",
    }
    res = await client.post("/api/v1/auth/register", json=register_payload)
    assert res.status_code in (201, 409)


@pytest.mark.asyncio
async def test_send_otp_success(client: AsyncClient, otp_user: None) -> None:
    # We will patch the redis creation to bypass actual redis calls for tests
    with patch("app.services.otp_service.otp_service.create_otp") as mock_create:
        mock_create.return_value = "123456"
        
        response = await client.post(
            "/api/v1/auth/send-otp",
            json={"phone": "9876543210"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "OTP sent successfully"
        assert data["DEBUG_OTP"] == "123456"
        mock_create.assert_called_once_with("9876543210")


@pytest.mark.asyncio
async def test_send_otp_user_not_found(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/send-otp",
        json={"phone": "0000000000"}  # does not exist
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


@pytest.mark.asyncio
async def test_verify_otp_success(client: AsyncClient, otp_user: None) -> None:
    with patch("app.services.otp_service.otp_service.verify_otp") as mock_verify:
        mock_verify.return_value = True
        
        response = await client.post(
            "/api/v1/auth/verify-otp",
            json={
                "phone": "9876543210",
                "otp": "123456"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["user"]["role"] == "migrant_worker"
        mock_verify.assert_called_once_with("9876543210", "123456")


@pytest.mark.asyncio
async def test_verify_otp_invalid(client: AsyncClient, otp_user: None) -> None:
    with patch("app.services.otp_service.otp_service.verify_otp") as mock_verify:
        mock_verify.return_value = False
        
        response = await client.post(
            "/api/v1/auth/verify-otp",
            json={
                "phone": "9876543210",
                "otp": "999999"  # invalid
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"] == "Invalid or expired OTP"
