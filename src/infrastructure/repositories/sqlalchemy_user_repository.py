from typing import List, Optional

from src.core.entities.user import User
from src.core.ports.user_repository import UserRepository
from src.infrastructure.database.models import UserModel, db


class SQLAlchemyUserRepository(UserRepository):
    """Implementación SQLAlchemy del repositorio de usuarios"""

    def __init__(self, session=None):
        """Inicializa el repositorio con una sesión de base de datos opcional"""
        self.session = session or db.session

    def _to_entity(self, model: UserModel) -> User:
        """Convierte un modelo SQLAlchemy a una entidad de dominio"""
        return User(
            id=model.id,
            email=model.email,
            password=model.password,
            first_name=model.first_name,
            last_name=model.last_name,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: User) -> UserModel:
        """Convierte una entidad de dominio a un modelo SQLAlchemy"""
        return UserModel(
            id=entity.id,
            email=entity.email,
            password=entity.password,
            first_name=entity.first_name,
            last_name=entity.last_name,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def save(self, user: User) -> User:
        user_model = self._to_model(user)
        self.session.add(user_model)
        self.session.commit()
        return self._to_entity(user_model)

    def get_by_id(self, user_id: int) -> Optional[User]:
        user_model = UserModel.query.get(user_id)
        return self._to_entity(user_model) if user_model else None

    def get_by_email(self, email: str) -> Optional[User]:
        user_model = UserModel.query.filter_by(email=email).first()
        return self._to_entity(user_model) if user_model else None

    def get_all(self) -> List[User]:
        return [self._to_entity(user) for user in UserModel.query.all()]

    def update(self, user: User) -> User:
        user_model = UserModel.query.get(user.id)
        if user_model:
            user_model.email = user.email
            user_model.password = user.password
            user_model.first_name = user.first_name
            user_model.last_name = user.last_name
            user_model.is_active = user.is_active
            user_model.updated_at = user.updated_at
            self.session.commit()
            return self._to_entity(user_model)
        return None

    def delete(self, user_id: int) -> bool:
        user_model = UserModel.query.get(user_id)
        if user_model:
            self.session.delete(user_model)
            self.session.commit()
            return True
        return False

    def exists_by_email(self, email: str) -> bool:
        return self.session.query(UserModel.query.filter_by(email=email).exists()).scalar()