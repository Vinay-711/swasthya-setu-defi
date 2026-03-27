import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.mark.asyncio
async def test_debug(client: AsyncClient):
    res = await client.post("/api/v1/auth/send-otp", json={"phone": "9876543210"})
    print("SEND OTP RESPONSE", res.status_code, res.json())
