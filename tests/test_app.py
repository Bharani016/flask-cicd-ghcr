from unittest.mock import MagicMock, patch

from app.app import app


def get_client():
    app.config["TESTING"] = True
    return app.test_client()


def test_home():
    response = get_client().get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Flask app is running"


def test_health_ok():
    with patch("app.app.get_connection", return_value=MagicMock()):
        response = get_client().get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_health_database_down():
    with patch("app.app.get_connection", side_effect=Exception("boom")):
        response = get_client().get("/health")
    assert response.status_code == 503
    assert response.get_json()["database"] == "unavailable"
