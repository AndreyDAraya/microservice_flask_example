import os
from datetime import timedelta
import pytest
from src.config import Config, DevelopmentConfig, TestingConfig, ProductionConfig, config


@pytest.fixture
def env_vars():
    """Setup environment variables for testing"""
    os.environ['SECRET_KEY'] = 'test-secret-key'
    os.environ['JWT_SECRET_KEY'] = 'test-jwt-secret'
    os.environ['DATABASE_URL'] = 'postgresql://test:test@testdb:5432/testdb'
    yield
    # Cleanup
    del os.environ['SECRET_KEY']
    del os.environ['JWT_SECRET_KEY']
    del os.environ['DATABASE_URL']


class TestConfig:
    def test_base_config_defaults(self):
        """Test default values in base Config class"""
        config_obj = Config()
        
        assert config_obj.SECRET_KEY == 'dev-secret-key-123'
        assert config_obj.JWT_SECRET_KEY == 'jwt-secret-key-123'
        assert 'postgresql://admin:admin123@localhost:5432/users_db' in config_obj.SQLALCHEMY_DATABASE_URI
        assert config_obj.SQLALCHEMY_TRACK_MODIFICATIONS is False
        assert config_obj.JWT_ACCESS_TOKEN_EXPIRES == timedelta(hours=1)
        assert config_obj.JWT_HEADER_TYPE == 'Bearer'
        assert config_obj.JWT_TOKEN_LOCATION == ['headers']
        assert config_obj.JWT_HEADER_NAME == 'Authorization'

    def test_swagger_config(self):
        """Test Swagger configuration settings"""
        config_obj = Config()
        
        assert config_obj.SWAGGER['title'] == 'Users API'
        assert config_obj.SWAGGER['version'] == '1.0.0'
        assert config_obj.SWAGGER['specs_route'] == '/docs/'
        assert 'Bearer' in config_obj.SWAGGER['securityDefinitions']


class TestDevelopmentConfig:
    def test_development_config(self):
        """Test development environment specific settings"""
        dev_config = DevelopmentConfig()
        
        assert dev_config.DEBUG is True
        assert dev_config.SECRET_KEY == 'dev-secret-key-123'
        assert 'postgresql://admin:admin123@localhost:5432/users_db' in dev_config.SQLALCHEMY_DATABASE_URI


class TestTestingConfig:
    def test_testing_config(self):
        """Test testing environment specific settings"""
        test_config = TestingConfig()
        
        assert test_config.TESTING is True
        assert 'users_test_db' in test_config.SQLALCHEMY_DATABASE_URI
        assert test_config.SECRET_KEY == 'dev-secret-key-123'


class TestProductionConfig:
    def test_production_config_defaults(self):
        """Test production config with default values"""
        # Guardar valores originales
        original_secret = os.environ.get('SECRET_KEY')
        original_jwt = os.environ.get('JWT_SECRET_KEY')
        original_db = os.environ.get('DATABASE_URL')
        
        # Eliminar variables de entorno
        if 'SECRET_KEY' in os.environ:
            del os.environ['SECRET_KEY']
        if 'JWT_SECRET_KEY' in os.environ:
            del os.environ['JWT_SECRET_KEY']
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
        
        prod_config = ProductionConfig()
        
        assert prod_config.DEBUG is False
        assert prod_config.TESTING is False
        assert prod_config.SECRET_KEY == 'dev-secret-key-123'  # Hereda el valor por defecto
        assert prod_config.JWT_SECRET_KEY == 'jwt-secret-key-123'  # Hereda el valor por defecto
        assert 'postgresql://admin:admin123@localhost:5432/users_db' in prod_config.SQLALCHEMY_DATABASE_URI
        
        # Restaurar valores originales
        if original_secret:
            os.environ['SECRET_KEY'] = original_secret
        if original_jwt:
            os.environ['JWT_SECRET_KEY'] = original_jwt
        if original_db:
            os.environ['DATABASE_URL'] = original_db

    def test_production_config_with_env_vars(self, env_vars):
        """Test production config with environment variables set"""
        # Guardar valores originales
        original_secret = os.environ.get('SECRET_KEY')
        original_jwt = os.environ.get('JWT_SECRET_KEY')
        original_db = os.environ.get('DATABASE_URL')
        
        try:
            # Configurar variables de entorno
            os.environ['SECRET_KEY'] = 'prod-secret-key'
            os.environ['JWT_SECRET_KEY'] = 'prod-jwt-secret'
            os.environ['DATABASE_URL'] = 'postgresql://prod:prod@proddb:5432/proddb'
            
            # Recargar el módulo de configuración para que tome las nuevas variables de entorno
            import importlib
            import src.config
            importlib.reload(src.config)
            from src.config import ProductionConfig
            prod_config = ProductionConfig()
            
            assert prod_config.SECRET_KEY == 'prod-secret-key'
            assert prod_config.JWT_SECRET_KEY == 'prod-jwt-secret'
            assert prod_config.SQLALCHEMY_DATABASE_URI == 'postgresql://prod:prod@proddb:5432/proddb'
        finally:
            # Restaurar valores originales
            if original_secret:
                os.environ['SECRET_KEY'] = original_secret
            else:
                del os.environ['SECRET_KEY']
                
            if original_jwt:
                os.environ['JWT_SECRET_KEY'] = original_jwt
            else:
                del os.environ['JWT_SECRET_KEY']
                
            if original_db:
                os.environ['DATABASE_URL'] = original_db
            else:
                del os.environ['DATABASE_URL']


def test_config_dictionary():
    """Test the config dictionary contains all environments"""
    assert 'development' in config
    assert 'testing' in config
    assert 'production' in config
    assert 'default' in config
    assert config['default'] == DevelopmentConfig
    assert isinstance(config['development'](), DevelopmentConfig)
    assert isinstance(config['testing'](), TestingConfig)
    assert isinstance(config['production'](), ProductionConfig)