import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from flask import Flask

from src.core.entities.user import User
from src.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from src.infrastructure.database.models import UserModel, db
@pytest.fixture
def app():
    """Create test Flask app"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


@pytest.fixture
def db_session(app):
    """Create database session"""
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()


@pytest.fixture
def repository(db_session):
    """Instancia del repositorio con sesión de prueba"""
    return SQLAlchemyUserRepository(db_session)
    """Instancia del repositorio con sesión mockeada"""
    return SQLAlchemyUserRepository(db_session)


@pytest.fixture
def sample_user():
    """Usuario de ejemplo para pruebas"""
    return User(
        id=1,
        email="test@example.com",
        password="hashed_password",
        first_name="Test",
        last_name="User",
        is_active=True,
        created_at=datetime.utcnow()
    )


@pytest.fixture
def sample_user_model(sample_user):
    """Modelo de usuario de ejemplo para pruebas"""
    return UserModel(
        id=sample_user.id,
        email=sample_user.email,
        password=sample_user.password,
        first_name=sample_user.first_name,
        last_name=sample_user.last_name,
        is_active=sample_user.is_active,
        created_at=sample_user.created_at
    )


class TestSQLAlchemyUserRepository:
    def test_save_new_user(self, repository, db_session, sample_user, app):
        """Test guardar nuevo usuario"""
        with app.app_context():
            # Ejecutar
            result = repository.save(sample_user)
            
            # Verificar
            assert isinstance(result, User)
            assert result.email == sample_user.email
            assert result.id is not None

    def test_get_by_id_existing_user(self, repository, db_session, sample_user, app):
        """Test obtener usuario existente por ID"""
        with app.app_context():
            # Primero guardamos un usuario
            saved_user = repository.save(sample_user)
            
            # Ejecutar
            result = repository.get_by_id(saved_user.id)
            
            # Verificar
            assert isinstance(result, User)
            assert result.id == saved_user.id
            assert result.email == saved_user.email

    def test_get_by_id_non_existing_user(self, repository, app):
        """Test obtener usuario no existente por ID"""
        with app.app_context():
            # Ejecutar
            result = repository.get_by_id(999)
            
            # Verificar
            assert result is None

    def test_exists_by_email_true(self, repository, sample_user, app):
        """Test verificar si existe email (caso positivo)"""
        with app.app_context():
            # Primero guardamos un usuario
            repository.save(sample_user)
            
            # Ejecutar
            result = repository.exists_by_email(sample_user.email)
            
            # Verificar
            assert result is True

    def test_exists_by_email_false(self, repository, app):
        """Test verificar si existe email (caso negativo)"""
        with app.app_context():
            # Ejecutar
            result = repository.exists_by_email("non-existing@example.com")
            
            # Verificar
            assert result is False

    def test_update_existing_user(self, repository, sample_user, app):
        """Test actualizar usuario existente"""
        with app.app_context():
            # Primero guardamos un usuario
            saved_user = repository.save(sample_user)
            
            # Modificar usuario
            saved_user.first_name = "Updated"
            
            # Ejecutar
            result = repository.update(saved_user)
            
            # Verificar
            assert isinstance(result, User)
            assert result.first_name == "Updated"
            
            # Verificar que el cambio persiste
            updated_user = repository.get_by_id(saved_user.id)
            assert updated_user.first_name == "Updated"

    def test_update_non_existing_user(self, repository, sample_user, app):
        """Test actualizar usuario no existente"""
        with app.app_context():
            # Asignar un ID que no existe
            sample_user.id = 999
            
            # Ejecutar
            result = repository.update(sample_user)
            
            # Verificar
            assert result is None

    def test_delete_existing_user(self, repository, sample_user, app):
        """Test eliminar usuario existente"""
        with app.app_context():
            # Primero guardamos un usuario
            saved_user = repository.save(sample_user)
            
            # Ejecutar
            result = repository.delete(saved_user.id)
            
            # Verificar
            assert result is True
            assert repository.get_by_id(saved_user.id) is None

    def test_delete_non_existing_user(self, repository, app):
        """Test eliminar usuario no existente"""
        with app.app_context():
            # Ejecutar
            result = repository.delete(999)
            
            # Verificar
            assert result is False