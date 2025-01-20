import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token

from src.core.entities.user import User
from src.interfaces.rest.controllers import api
from src.application.use_cases.user_use_cases import CreateUserDTO, UpdateUserDTO

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    jwt = JWTManager(app)
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        return {"id": jwt_data["sub"]}
        
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user["id"] if isinstance(user, dict) else user
    
    app.register_blueprint(api)
    return app

@pytest.fixture
def auth_headers(app):
    with app.app_context():
        access_token = create_access_token(identity="1")
        return {'Authorization': f'Bearer {access_token}'}

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_user():
    return User(
        id=1,
        email="test@example.com",
        password="password123",
        first_name="Test",
        last_name="User",
        is_active=True,
        created_at=datetime.utcnow()
    )

class TestUserControllers:
    def test_create_user_success(self, client, sample_user):
        # Arrange
        with patch('src.interfaces.rest.controllers.user_use_cases') as mock_use_cases:
            mock_use_cases.create_user.return_value = sample_user
            user_data = {
                "email": "test@example.com",
                "password": "password123",
                "first_name": "Test",
                "last_name": "User"
            }

            # Act
            response = client.post('/users', json=user_data)
            data = response.get_json()

            # Assert
            assert response.status_code == 201
            assert data['email'] == sample_user.email
            assert data['first_name'] == sample_user.first_name
            assert data['last_name'] == sample_user.last_name
            mock_use_cases.create_user.assert_called_once()

    def test_create_user_invalid_data(self, client):
        # Arrange
        user_data = {
            "email": "test@example.com",
            # Falta password
            "first_name": "Test",
            "last_name": "User"
        }

        # Act
        response = client.post('/users', json=user_data)
        data = response.get_json()

        # Assert
        assert response.status_code == 400
        assert 'error' in data

    def test_get_users_success(self, client, sample_user, auth_headers):
        # Arrange
        with patch('src.interfaces.rest.controllers.user_use_cases') as mock_use_cases:
            mock_use_cases.get_all_users.return_value = [sample_user]

            # Act
            response = client.get('/users', headers=auth_headers)
            data = response.get_json()

            # Assert
            assert response.status_code == 200
            assert len(data) == 1
            assert data[0]['email'] == sample_user.email
            mock_use_cases.get_all_users.assert_called_once()

    def test_get_user_by_id_success(self, client, sample_user, auth_headers):
        # Arrange
        with patch('src.interfaces.rest.controllers.user_use_cases') as mock_use_cases:
            mock_use_cases.get_user.return_value = sample_user

            # Act
            response = client.get('/users/1', headers=auth_headers)
            data = response.get_json()

            # Assert
            assert response.status_code == 200
            assert data['email'] == sample_user.email
            mock_use_cases.get_user.assert_called_once_with(1)

    def test_get_user_not_found(self, client, auth_headers):
        # Arrange
        with patch('src.interfaces.rest.controllers.user_use_cases') as mock_use_cases:
            mock_use_cases.get_user.side_effect = ValueError("Usuario no encontrado")

            # Act
            response = client.get('/users/999', headers=auth_headers)
            data = response.get_json()

            # Assert
            assert response.status_code == 404
            assert 'error' in data
            assert data['error'] == 'Usuario no encontrado'

    def test_update_user_success(self, client, sample_user, auth_headers):
        # Arrange
        with patch('src.interfaces.rest.controllers.user_use_cases') as mock_use_cases:
            mock_use_cases.update_user.return_value = sample_user
            update_data = {
                "first_name": "Updated",
                "last_name": "Name"
            }

            # Act
            response = client.put('/users/1', json=update_data, headers=auth_headers)
            data = response.get_json()

            # Assert
            assert response.status_code == 200
            assert data['email'] == sample_user.email
            mock_use_cases.update_user.assert_called_once()

    def test_delete_user_success(self, client, auth_headers):
        # Arrange
        with patch('src.interfaces.rest.controllers.user_use_cases') as mock_use_cases:
            mock_use_cases.delete_user.return_value = True

            # Act
            response = client.delete('/users/1', headers=auth_headers)

            # Assert
            assert response.status_code == 204
            mock_use_cases.delete_user.assert_called_once_with(1)

    def test_login_success(self, client, sample_user):
        # Arrange
        with patch('src.interfaces.rest.controllers.user_repository') as mock_repository, \
             patch('src.interfaces.rest.controllers.create_access_token') as mock_create_token:
            mock_repository.get_by_email.return_value = sample_user
            mock_create_token.return_value = "test-token"
            login_data = {
                "email": "test@example.com",
                "password": "password123"
            }

            # Act
            response = client.post('/auth/login', json=login_data)
            data = response.get_json()

            # Assert
            assert response.status_code == 200
            assert 'access_token' in data
            assert data['access_token'] == 'test-token'
            mock_repository.get_by_email.assert_called_once_with(login_data['email'])

    def test_login_invalid_credentials(self, client):
        # Arrange
        with patch('src.interfaces.rest.controllers.user_repository') as mock_repository:
            mock_repository.get_by_email.return_value = None
            login_data = {
                "email": "wrong@example.com",
                "password": "wrongpass"
            }

            # Act
            response = client.post('/auth/login', json=login_data)
            data = response.get_json()

            # Assert
            assert response.status_code == 401
            assert 'error' in data
            assert data['error'] == 'Credenciales inválidas'