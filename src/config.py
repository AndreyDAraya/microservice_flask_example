import os
from datetime import timedelta


class Config:
    """Base application configuration
    
    This class defines the core configuration settings for the Flask application,
    including database connections, JWT authentication, and Swagger documentation.
    All environment-specific configurations inherit from this base class.
    """
    
    # Flask core settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # SQLAlchemy database configuration
    # Default connection uses PostgreSQL with UTF-8 encoding
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'postgresql://admin:admin123@localhost:5432/users_db?client_encoding=utf8'
    )
    # Disable SQLAlchemy event system for better performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Authentication settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key')
    # Tokens expire after 1 hour
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    # Use Bearer token authentication scheme
    JWT_HEADER_TYPE = 'Bearer'
    # Only accept tokens in request headers
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    
    # Swagger/OpenAPI documentation configuration
    SWAGGER = {
        'title': 'Users API',
        'uiversion': 3,
        'version': '1.0.0',
        'description': 'RESTful API for user management',
        'specs_route': '/docs/',
        'swagger': '2.0',
        'securityDefinitions': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'Copy and paste the complete access_token value including the Bearer word from the login endpoint. Example: Bearer eyJhbGciOiJIUzI1...'
            }
        },
        'security': [
            {'JWT': []}
        ]
    }


class DevelopmentConfig(Config):
    """Development environment configuration
    
    Enables debug mode for detailed error messages and automatic reloading.
    Uses default database and secret keys for easy local development.
    """
    DEBUG = True


class TestingConfig(Config):
    """Testing environment configuration
    
    Enables testing mode and uses a separate test database to isolate test data.
    Inherits all other settings from base Config.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://admin:admin123@localhost:5432/users_test_db?client_encoding=utf8'


class ProductionConfig(Config):
    """Production environment configuration
    
    Disables all debug/testing features for security.
    Requires all sensitive settings to be provided via environment variables:
    - SECRET_KEY: Flask secret key for sessions and CSRF
    - JWT_SECRET_KEY: Key for signing JWT tokens
    - DATABASE_URL: Production database connection string
    """
    DEBUG = False
    TESTING = False
    # These values must be set through environment variables in production
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


# Configuration dictionary for easy environment switching
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}