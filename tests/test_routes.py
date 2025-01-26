import pytest
from flask import Flask

from app.exceptions import InvalidSignatureException
from app.routes import bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_stream_invalid_signature(client, mocker):
    mocker.patch("app.auth.validate_signature", side_effect=InvalidSignatureException)
    response = client.post("/stream", data=b"test body")
    assert response.status_code == 401
    assert response.json == {"error": "Invalid signature"}
