import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    register_payload = {
        "email": "worker1@example.com",
        "password": "Worker@123",
        "role": "migrant_worker",
        "name": "Worker One",
        "phone": "9999999999",
        "language": "hi",
    }

    register_res = await client.post("/api/v1/auth/register", json=register_payload)
    assert register_res.status_code == 201
    token = register_res.json()["access_token"]
    assert token

    login_res = await client.post(
        "/api/v1/auth/login",
        json={"email": register_payload["email"], "password": register_payload["password"]},
    )
    assert login_res.status_code == 200
    assert login_res.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_admin_only_route_rejects_doctor(client):
    # Register a doctor
    doctor_payload = {
        "email": "doctor1@example.com",
        "password": "Doctor@123",
        "role": "doctor",
        "name": "Doctor One",
        "phone": "8888888888",
    }
    res = await client.post("/api/v1/auth/register", json=doctor_payload)
    assert res.status_code == 201
    doctor_token = res.json()["access_token"]

    # Attempt to access admin-only route
    admin_res = await client.get(
        "/api/v1/auth/admin-only",
        headers={"Authorization": f"Bearer {doctor_token}"}
    )
    assert admin_res.status_code == 403

    # Register an admin
    admin_payload = {
        "email": "admin1@example.com",
        "password": "Admin@123",
        "role": "admin",
        "name": "Admin One",
        "phone": "7777777777",
    }
    res2 = await client.post("/api/v1/auth/register", json=admin_payload)
    assert res2.status_code == 201
    admin_token = res2.json()["access_token"]

    # Attempt to access admin-only route
    admin_res2 = await client.get(
        "/api/v1/auth/admin-only",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert admin_res2.status_code == 200
