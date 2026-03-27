import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status


@pytest_asyncio.fixture
async def asha_token(client: AsyncClient) -> dict:
    register_payload = {
        "email": "asha.docs@example.com",
        "password": "Worker@123",
        "role": "asha_worker",
        "name": "Asha Docs",
        "phone": "9876543221",
        "language": "hi",
    }
    res = await client.post("/api/v1/auth/register", json=register_payload)
    if res.status_code == 201:
        return {"token": res.json()["access_token"], "id": res.json()["user"]["id"]}
    login = await client.post("/api/v1/auth/login", json={"email": "asha.docs@example.com", "password": "Worker@123"})
    return {"token": login.json()["access_token"], "id": login.json()["user"]["id"]}


@pytest_asyncio.fixture
async def doctor_token(client: AsyncClient) -> dict:
    register_payload = {
        "email": "doctor.docs@example.com",
        "password": "Worker@123",
        "role": "doctor",
        "name": "Doctor Docs",
        "phone": "9876543222",
        "language": "en",
    }
    res = await client.post("/api/v1/auth/register", json=register_payload)
    if res.status_code == 201:
        return {"token": res.json()["access_token"], "id": res.json()["user"]["id"]}
    login = await client.post("/api/v1/auth/login", json={"email": "doctor.docs@example.com", "password": "Worker@123"})
    return {"token": login.json()["access_token"], "id": login.json()["user"]["id"]}


@pytest_asyncio.fixture
async def worker_token(client: AsyncClient) -> dict:
    register_payload = {
        "email": "worker.docs@example.com",
        "password": "Worker@123",
        "role": "migrant_worker",
        "name": "Worker Docs",
        "phone": "9876543223",
        "language": "hi",
    }
    res = await client.post("/api/v1/auth/register", json=register_payload)
    if res.status_code == 201:
        return {"token": res.json()["access_token"], "id": res.json()["user"]["id"]}
    login = await client.post("/api/v1/auth/login", json={"email": "worker.docs@example.com", "password": "Worker@123"})
    return {"token": login.json()["access_token"], "id": login.json()["user"]["id"]}


@pytest_asyncio.fixture
async def another_worker_token(client: AsyncClient) -> dict:
    register_payload = {
        "email": "another.docs@example.com",
        "password": "Worker@123",
        "role": "migrant_worker",
        "name": "Another Docs",
        "phone": "9876543224",
        "language": "hi",
    }
    res = await client.post("/api/v1/auth/register", json=register_payload)
    if res.status_code == 201:
        return {"token": res.json()["access_token"], "id": res.json()["user"]["id"]}
    login = await client.post("/api/v1/auth/login", json={"email": "another.docs@example.com", "password": "Worker@123"})
    return {"token": login.json()["access_token"], "id": login.json()["user"]["id"]}


@pytest.mark.asyncio
async def test_document_upload_ocr_stub(client: AsyncClient, asha_token: dict, worker_token: dict):
    # Prepare a dummy image file
    files = {"file": ("prescription.jpg", b"fake image content", "image/jpeg")}
    data = {"worker_id": worker_token["id"]}
    
    # Upload document as ASHA worker
    resp = await client.post(
        "/api/v1/documents/upload",
        files=files,
        data=data,
        headers={"Authorization": f"Bearer {asha_token['token']}"},
    )
    assert resp.status_code == status.HTTP_201_CREATED
    doc = resp.json()
    assert doc["worker_id"] == worker_token["id"]
    assert "MOCK_OCR_TEXT" in doc["parsed_json"]["raw_text"]
    assert "paracetamol" in str(doc["parsed_json"]["medicines"]).lower()
    
    return doc


@pytest.mark.asyncio
async def test_document_rbac(client: AsyncClient, worker_token: dict, another_worker_token: dict, doctor_token: dict):
    # Upload requires doctor or asha
    files = {"file": ("test.png", b"fake", "image/png")}
    data = {"worker_id": worker_token["id"]}
    
    resp = await client.post(
        "/api/v1/documents/upload",
        files=files,
        data=data,
        headers={"Authorization": f"Bearer {worker_token['token']}"},
    )
    assert resp.status_code == status.HTTP_403_FORBIDDEN  # Worker cannot upload
    
    # Upload via doctor to set up the document
    resp = await client.post(
        "/api/v1/documents/upload",
        files=files,
        data=data,
        headers={"Authorization": f"Bearer {doctor_token['token']}"},
    )
    assert resp.status_code == status.HTTP_201_CREATED
    doc_id = resp.json()["id"]
    
    # Another worker cannot view this worker's documents
    resp = await client.get(
        f"/api/v1/documents/worker/{worker_token['id']}", 
        headers={"Authorization": f"Bearer {another_worker_token['token']}"}
    )
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    
    resp = await client.get(
        f"/api/v1/documents/{doc_id}", 
        headers={"Authorization": f"Bearer {another_worker_token['token']}"}
    )
    assert resp.status_code == status.HTTP_403_FORBIDDEN
    
    # The owner worker CAN view their documents
    resp = await client.get(
        f"/api/v1/documents/worker/{worker_token['id']}", 
        headers={"Authorization": f"Bearer {worker_token['token']}"}
    )
    assert resp.status_code == status.HTTP_200_OK
    assert len(resp.json()) > 0
    
    resp = await client.get(
        f"/api/v1/documents/{doc_id}", 
        headers={"Authorization": f"Bearer {worker_token['token']}"}
    )
    assert resp.status_code == status.HTTP_200_OK
    
    # A doctor CAN view any documents
    resp = await client.get(
        f"/api/v1/documents/{doc_id}", 
        headers={"Authorization": f"Bearer {doctor_token['token']}"}
    )
    assert resp.status_code == status.HTTP_200_OK
