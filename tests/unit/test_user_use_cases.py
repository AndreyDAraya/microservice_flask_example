import pytest
from datetime import datetime
from unittest.mock import Mock

from src.core.entities.user import User
from src.application.use_cases.user_use_cases import UserUseCases, CreateUserDTO, UpdateUserDTO


@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def user_use_cases(mock_repository):
    return UserUseCases(mock_repository)

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

class TestUserUseCases:
    def test_create_user_success(self, user_use_cases, mock_repository, sample_user):
        # Arrange
        mock_repository.exists_by_email.return_value = False
        mock_repository.save.return_value = sample_user
        user_dto = CreateUserDTO(
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

        # Act
        result = user_use_cases.create_user(user_dto)

        # Assert
        assert result == sample_user
        mock_repository.exists_by_email.assert_called_once_with(user_dto.email)
        mock_repository.save.assert_called_once()

    def test_create_user_duplicate_email(self, user_use_cases, mock_repository):
        # Arrange
        mock_repository.exists_by_email.return_value = True
        user_dto = CreateUserDTO(
            email="existing@example.com",
            password="password123",
            first_name="Test",
            last_name="User"
        )

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            user_use_cases.create_user(user_dto)
        assert "Ya existe un usuario" in str(exc_info.value)
        mock_repository.save.assert_not_called()

    def test_get_user_success(self, user_use_cases, mock_repository, sample_user):
        # Arrange
        mock_repository.get_by_id.return_value = sample_user

        # Act
        result = user_use_cases.get_user(1)

        # Assert
        assert result == sample_user
        mock_repository.get_by_id.assert_called_once_with(1)

    def test_get_user_not_found(self, user_use_cases, mock_repository):
        # Arrange
        mock_repository.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            user_use_cases.get_user(999)
        assert "No existe un usuario" in str(exc_info.value)

    def test_update_user_success(self, user_use_cases, mock_repository, sample_user):
        # Arrange
        mock_repository.get_by_id.return_value = sample_user
        mock_repository.update.return_value = sample_user
        update_dto = UpdateUserDTO(
            first_name="Updated",
            last_name="Name"
        )

        # Act
        result = user_use_cases.update_user(1, update_dto)

        # Assert
        assert result == sample_user
        mock_repository.get_by_id.assert_called_once_with(1)
        mock_repository.update.assert_called_once()

    def test_delete_user_success(self, user_use_cases, mock_repository, sample_user):
        # Arrange
        mock_repository.get_by_id.return_value = sample_user
        mock_repository.delete.return_value = True

        # Act
        result = user_use_cases.delete_user(1)

        # Assert
        assert result is True
        mock_repository.get_by_id.assert_called_once_with(1)
        mock_repository.delete.assert_called_once_with(1)

    def test_toggle_user_status(self, user_use_cases, mock_repository, sample_user):
        # Arrange
        mock_repository.get_by_id.return_value = sample_user
        mock_repository.update.return_value = sample_user

        # Act
        result = user_use_cases.toggle_user_status(1, False)

        # Assert
        assert result == sample_user
        assert not result.is_active
        mock_repository.get_by_id.assert_called_once_with(1)
        mock_repository.update.assert_called_once()