import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.services.auth_service import AuthService
from app.models import User
from werkzeug.security import generate_password_hash
import jwt
from datetime import datetime, timedelta

@pytest.fixture
def client():
    app = Flask(__name__)
    app.testing = True
    client = app.test_client()
    return client

class AuthControllerTest:
    def test_register_endpoint(self, client, mocker):
        mock_register = mocker.patch("app.services.auth_service.AuthService.register_user", return_value={"message": "User created successfully"})
        response = client.post("/auth/register", json={"email": "test@example.com", "password": "password123"})
        assert response.status_code == 201
        assert response.get_json() == {"message": "User created successfully"}
        mock_register.assert_called_once_with("test@example.com", "password123")

    def test_login_endpoint(self, client, mocker):
        mock_token = jwt.encode({"ulid": "user-123", "exp": datetime.utcnow() + timedelta(minutes=30)}, "secret", algorithm="HS256")
        mock_login = mocker.patch("app.services.auth_service.AuthService.login", return_value=mock_token)
        response = client.post("/auth/login", json={"email": "test@example.com", "password": "password123"})
        assert response.status_code == 200
        assert "token" in response.get_json()["message"]
        mock_login.assert_called_once_with("test@example.com", "password123")
