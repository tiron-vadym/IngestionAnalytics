from uuid import uuid4
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ingest_and_query_stats():
    batch = [
        {"event_id": str(uuid4()), "occurred_at": "2025-10-30T12:00:00",
         "user_id": 1, "event_type": "login", "properties": None},
        {"event_id": str(uuid4()), "occurred_at": "2025-10-30T13:00:00",
         "user_id": 2, "event_type": "purchase", "properties": None},
    ]

    response = client.post("/events", json=batch)
    assert response.status_code == 200
    assert response.json()["ingested"] == 2

    response = client.get("/dau", params={"from_": "2025-10-30", "to": "2025-10-30"})
    assert response.status_code == 200
    data = response.json()
    assert any(r["dau"] == 1 for r in data)
