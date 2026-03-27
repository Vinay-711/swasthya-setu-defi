# pyre-ignore-all-errors
import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status

@pytest_asyncio.fixture
async def asha_token(client: AsyncClient) -> dict:
    register_payload = {
        "email": "asha.health@example.com",
        "password": "Worker@123",
        "role": "asha_worker",
        "name": "Asha Worker",
        "phone": "9876543111",
        "language": "hi",
    }
    res = await client.post("/api/v1/auth/register", json=register_payload)
    if res.status_code == 201:
        return {"token": res.json()["access_token"], "id": res.json()["user"]["id"]}
    
    login = await client.post("/api/v1/auth/login", json={"email": register_payload["email"], "password": register_payload["password"]})
    return {"token": login.json()["access_token"], "id": login.json()["user"]["id"]}


@pytest_asyncio.fixture
async def doctor_token(client: AsyncClient) -> dict:
    register_payload = {
        "email": "doctor.health@example.com",
        "password": "Worker@123",
        "role": "doctor",
        "name": "Doctor Health",
        "phone": "9876543112",
        "language": "hi",
    }
    res = await client.post("/api/v1/auth/register", json=register_payload)
    if res.status_code == 201:
        return {"token": res.json()["access_token"], "id": res.json()["user"]["id"]}
    
    login = await client.post("/api/v1/auth/login", json={"email": register_payload["email"], "password": register_payload["password"]})
    return {"token": login.json()["access_token"], "id": login.json()["user"]["id"]}


@pytest_asyncio.fixture
async def patient_token(client: AsyncClient) -> dict:
    register_payload = {
        "email": "patient.health@example.com",
        "password": "Worker@123",
        "role": "migrant_worker",
        "name": "Patient Worker",
        "phone": "9876543113",
        "language": "hi",
    }
    res = await client.post("/api/v1/auth/register", json=register_payload)
    if res.status_code == 201:
        return {"token": res.json()["access_token"], "id": res.json()["user"]["id"]}
    
    login = await client.post("/api/v1/auth/login", json={"email": register_payload["email"], "password": register_payload["password"]})
    return {"token": login.json()["access_token"], "id": login.json()["user"]["id"]}


@pytest.mark.asyncio
async def test_create_health_record_asha(client: AsyncClient, asha_token: dict, patient_token: dict) -> None:
    # ASHA worker creates a symptom report for patient
    payload = {
        "worker_id": patient_token["id"],
        "record_type": "symptom_report",
        "data_json": {"symptoms": ["fever", "cough"], "severity": "mild"}
    }
    response = await client.post(
        "/api/v1/health-records/",
        json=payload,
        headers={"Authorization": f"Bearer {asha_token['token']}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["worker_id"] == patient_token["id"]
    assert data["record_type"] == "symptom_report"
    assert "fever" in data["data_json"]["symptoms"]


@pytest.mark.asyncio
async def test_create_health_record_unauthorized(client: AsyncClient, patient_token: dict) -> None:
    # Regular patient cannot create a record
    payload = {
        "worker_id": patient_token["id"],
        "record_type": "symptom_report",
        "data_json": {"symptoms": ["headache"]}
    }
    response = await client.post(
        "/api/v1/health-records/",
        json=payload,
        headers={"Authorization": f"Bearer {patient_token['token']}"}
    )
    # Should be 403 Forbidden because require_roles checks current_user.role
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.asyncio
async def test_list_records_pagination_doctor(client: AsyncClient, doctor_token: dict, asha_token: dict, patient_token: dict) -> None:
    # Create 3 records
    for i in range(3):
        await client.post(
            "/api/v1/health-records/",
            json={
                "worker_id": patient_token["id"],
                "record_type": "visit_record",
                "data_json": {"day": i}
            },
            headers={"Authorization": f"Bearer {asha_token['token']}"}
        )
    
    # Doctor lists records with pagination
    response = await client.get(
        f"/api/v1/health-records/worker/{patient_token['id']}?limit=2&skip=1",
        headers={"Authorization": f"Bearer {doctor_token['token']}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) <= 2
    assert data["total"] >= 3
    assert data["limit"] == 2
    assert data["skip"] == 1


@pytest.mark.asyncio
async def test_list_records_forbidden(client: AsyncClient, patient_token: dict, asha_token: dict) -> None:
    # ASHA worker tries to view records of patient (currently require DOCTOR, ADMIN or self)
    # Wait, in routes: if current_user.role not in [UserRole.DOCTOR, UserRole.ADMIN] and current_user.id != worker_id
    response = await client.get(
        f"/api/v1/health-records/worker/{patient_token['id']}",
        headers={"Authorization": f"Bearer {asha_token['token']}"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Patient tries to view their own - SHOULD BE OK
    response_self = await client.get(
        f"/api/v1/health-records/worker/{patient_token['id']}",
        headers={"Authorization": f"Bearer {patient_token['token']}"}
    )
    assert response_self.status_code == status.HTTP_200_OK
