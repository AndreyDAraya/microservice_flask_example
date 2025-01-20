from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.entities.user import User


class UserRepository(ABC):
    """Puerto (interfaz) para el repositorio de usuarios"""

    @abstractmethod
    def save(self, user: User) -> User:
        """Guarda un usuario en el repositorio"""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su email"""
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        """Obtiene todos los usuarios"""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Actualiza un usuario existente"""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Elimina un usuario por su ID"""
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Verifica si existe un usuario con el email dado"""
        pass