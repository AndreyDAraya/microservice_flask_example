from dataclasses import dataclass
from typing import List, Optional

from src.core.entities.user import User
from src.core.ports.user_repository import UserRepository


@dataclass
class CreateUserDTO:
    email: str
    password: str
    first_name: str
    last_name: str


@dataclass
class UpdateUserDTO:
    first_name: str
    last_name: str


class UserUseCases:
    """Casos de uso para la gestión de usuarios"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user_dto: CreateUserDTO) -> User:
        """Crea un nuevo usuario"""
        if self.user_repository.exists_by_email(user_dto.email):
            raise ValueError(f"Ya existe un usuario con el email {user_dto.email}")

        user = User(
            email=user_dto.email,
            password=user_dto.password,  # En una implementación real, aquí se haría el hash del password
            first_name=user_dto.first_name,
            last_name=user_dto.last_name
        )
        
        return self.user_repository.save(user)

    def get_user(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"No existe un usuario con el ID {user_id}")
        return user

    def get_all_users(self) -> List[User]:
        """Obtiene todos los usuarios"""
        return self.user_repository.get_all()

    def update_user(self, user_id: int, user_dto: UpdateUserDTO) -> User:
        """Actualiza un usuario existente"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"No existe un usuario con el ID {user_id}")

        user.update_profile(
            first_name=user_dto.first_name,
            last_name=user_dto.last_name
        )
        
        return self.user_repository.update(user)

    def delete_user(self, user_id: int) -> bool:
        """Elimina un usuario"""
        if not self.user_repository.get_by_id(user_id):
            raise ValueError(f"No existe un usuario con el ID {user_id}")
        
        return self.user_repository.delete(user_id)

    def change_password(self, user_id: int, new_password: str) -> User:
        """Cambia la contraseña de un usuario"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"No existe un usuario con el ID {user_id}")

        user.update_password(new_password)  # En una implementación real, aquí se haría el hash del password
        return self.user_repository.update(user)

    def toggle_user_status(self, user_id: int, activate: bool) -> User:
        """Activa o desactiva un usuario"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"No existe un usuario con el ID {user_id}")

        if activate:
            user.activate()
        else:
            user.deactivate()

        return self.user_repository.update(user)