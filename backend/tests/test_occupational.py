# pyre-ignore-all-errors
import pytest

@pytest.mark.asyncio
async def test_occupational_risk_profile_rule_based_high(client):
    register_payload = {
        "email": "risk.worker@example.com",
        "password": "Worker@123",
        "role": "migrant_worker",
        "name": "Risk Worker",
        "phone": "8888888888",
        "language": "en",
    }

    register_res = await client.post("/api/v1/auth/register", json=register_payload)
    assert register_res.status_code == 201
    body = register_res.json()
    token = body["access_token"]
    worker_id = body["user"]["id"]

    headers = {"Authorization": f"Bearer {token}"}
    risk_payload = {
        "worker_id": worker_id,
        "occupation": "stone_quarry",
        "years_in_job": 8,
        "tasks": ["drilling", "stone_cutting"],
        "ppe_usage": "rarely",
        "symptoms": ["persistent_cough"],
    }

    response = await client.post("/api/v1/occupational/risk-profile", json=risk_payload, headers=headers)
    assert response.status_code == 200

    risk = response.json()
    assert risk["silicosis"] >= 0.75
    assert risk["risk_level"] in {"HIGH", "MEDIUM"}
    assert len(risk["top_factors"]) == 3
