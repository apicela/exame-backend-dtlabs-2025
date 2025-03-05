import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from app.services.auth_service import AuthService
from app.models import User
from werkzeug.security import generate_password_hash
import jwt
from datetime import datetime, timedelta
from app.utils import ErrorResponse

class TestAuthService:
    def test_register_user_success(self, mocker):
        mock_user = None
        mocker.patch("app.models.User.query.filter_by", return_value=MagicMock(first=lambda: mock_user))
        mock_db = mocker.patch("app.services.auth_service.db.session")
        
        response = AuthService.register_user("test@example.com", "password123")
        assert response == {"message": "User created successfully"}
        mock_db.add.assert_called()
        mock_db.commit.assert_called()

    def test_register_user_existing_email(self, mocker):
        mock_user = User(email="test@example.com", password=generate_password_hash("password123"))
        mocker.patch("app.models.User.query.filter_by", return_value=MagicMock(first=lambda: mock_user))
        
        with pytest.raises(ErrorResponse) as exc:
            AuthService.register_user("test@example.com", "password123")
        assert exc.value.status_code == 409
        assert str(exc.value) == "Email already registered"

    def test_login_success(self, mocker):
        password = "password123"
        hashed_password = generate_password_hash(password)
        mock_user = User(email="test@example.com", password=hashed_password, ulid="user-123")
        mocker.patch("app.models.User.query.filter_by", return_value=MagicMock(first=lambda: mock_user))
        mocker.patch("app.services.auth_service.check_password_hash", return_value=True)
        
        token = AuthService.login("test@example.com", password)
        decoded_token = jwt.decode(token, "secret", algorithms=["HS256"])
        assert decoded_token["ulid"] == "user-123"

    def test_login_invalid_credentials(self, mocker):
        mock_user = None
        mocker.patch("app.models.User.query.filter_by", return_value=MagicMock(first=lambda: mock_user))
        
        with pytest.raises(ErrorResponse) as exc:
            AuthService.login("wrong@example.com", "password123")
        assert exc.value.status_code == 401
        assert str(exc.value) == "That account doesn't exist. Please create a new account."

    def test_login_wrong_password(self, mocker):
        mock_user = User(email="test@example.com", password=generate_password_hash("password123"))
        mocker.patch("app.models.User.query.filter_by", return_value=MagicMock(first=lambda: mock_user))
        mocker.patch("app.services.auth_service.check_password_hash", return_value=False)
        
        with pytest.raises(ErrorResponse) as exc:
            AuthService.login("test@example.com", "wrongpassword")
        assert exc.value.status_code == 401
        assert str(exc.value) == "Credentials doesn't exist"