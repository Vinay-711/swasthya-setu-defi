import pytest


@pytest.mark.asyncio
async def test_mock_health(client):
    response = await client.get("/api/v1/health?mock=true")
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "mock"


@pytest.mark.asyncio
async def test_mock_occupational_profile(client):
    response = await client.get("/api/v1/occupational/risk-profile?mock=true")
    assert response.status_code == 200
    body = response.json()
    assert body["risk_level"] == "HIGH"
    assert body["silicosis"] == 0.87


@pytest.mark.asyncio
async def test_mock_voice_transcribe(client):
    response = await client.post("/api/v1/voice/transcribe?mock=true")
    assert response.status_code == 200
    body = response.json()
    assert "mujhe seene mein dard" in body["text"]


@pytest.mark.asyncio
async def test_mock_document_scan(client):
    response = await client.post("/api/v1/documents/scan?mock=true")
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "processed"
    assert body["parsed_json"]["medicines"]
