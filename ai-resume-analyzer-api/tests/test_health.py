def test_health_check_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["environment"] in ["development", "test"]


def test_database_health_check_returns_ok(client):
    response = client.get("/db-health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["database"] == "connected"
