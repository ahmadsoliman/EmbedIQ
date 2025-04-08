from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient):
    """
    Test the health check endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "embediq-api"}


def test_root_endpoint(client: TestClient):
    """
    Test the root endpoint that provides API information.
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "version" in data
    assert "documentation" in data
