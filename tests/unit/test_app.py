import os
import pytest
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_cors import CORS
from flasgger import Swagger

from src.app import create_app
from src.infrastructure.database.models import db


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


class TestApp:
    def test_create_app_default_config(self):
        """Test app creation with default config"""
        app = create_app()
        assert isinstance(app, Flask)
        assert app.config['DEBUG'] is True  # default is development config
        assert 'users_db' in app.config['SQLALCHEMY_DATABASE_URI']

    def test_create_app_testing_config(self):
        """Test app creation with testing config"""
        app = create_app('testing')
        assert isinstance(app, Flask)
        assert app.config['TESTING'] is True
        assert 'users_test_db' in app.config['SQLALCHEMY_DATABASE_URI']

    def test_create_app_production_config(self):
        """Test app creation with production config"""
        os.environ['SECRET_KEY'] = 'test-secret'
        os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret'
        os.environ['DATABASE_URL'] = 'postgresql://test:test@testdb:5432/testdb'
        
        app = create_app('production')
        assert isinstance(app, Flask)
        assert app.config['DEBUG'] is False
        assert app.config['TESTING'] is False
        
        # Cleanup
        del os.environ['SECRET_KEY']
        del os.environ['JWT_SECRET_KEY']
        del os.environ['DATABASE_URL']

    def test_create_app_with_flask_env(self):
        """Test app creation using FLASK_ENV environment variable"""
        os.environ['FLASK_ENV'] = 'testing'
        app = create_app()
        assert app.config['TESTING'] is True
        del os.environ['FLASK_ENV']

    def test_extensions_initialization(self):
        """Test Flask extensions are properly initialized"""
        app = create_app('testing')
        
        # Test SQLAlchemy initialization
        assert hasattr(app, 'extensions')
        assert 'sqlalchemy' in app.extensions
        
        # Test JWT initialization
        assert 'flask-jwt-extended' in app.extensions
        assert isinstance(app.extensions['flask-jwt-extended'], JWTManager)
        
        # Test CORS initialization
        # CORS no se registra en app.extensions, pero podemos verificar que la app tiene los decoradores CORS
        assert app.before_request_funcs[None] is not None  # CORS registra funciones before_request
        
        # Test Swagger initialization
        assert hasattr(app, 'swag')  # Flasgger añade el atributo 'swag' a la app

    def test_blueprint_registration(self):
        """Test API blueprint is registered"""
        app = create_app('testing')
        rules = [str(rule) for rule in app.url_map.iter_rules()]
        
        # Check if API routes are registered with correct prefix
        assert any(rule.startswith('/api/v1/') for rule in rules)

    def test_json_ascii_config(self):
        """Test JSON ASCII configuration"""
        app = create_app('testing')
        assert app.json.ensure_ascii is False

    def test_jwt_config(self):
        """Test JWT configuration"""
        app = create_app('testing')
        assert app.config['JWT_TOKEN_LOCATION'] == ['headers']

    def test_health_check_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json == {'status': 'healthy'}

    def test_database_uri_config(self):
        """Test database URI configuration"""
        app = create_app('testing')
        assert 'postgresql://' in app.config['SQLALCHEMY_DATABASE_URI']
        assert 'users_test_db' in app.config['SQLALCHEMY_DATABASE_URI']