from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Entidad de dominio para Usuario"""
    
    email: str
    password: str
    first_name: str
    last_name: str
    is_active: bool = True
    created_at: datetime = datetime.utcnow()
    updated_at: Optional[datetime] = None
    id: Optional[int] = None

    def update_password(self, new_password: str) -> None:
        """Actualiza la contraseña del usuario"""
        self.password = new_password
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Desactiva el usuario"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Activa el usuario"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def update_profile(self, first_name: str, last_name: str) -> None:
        """Actualiza el perfil del usuario"""
        self.first_name = first_name
        self.last_name = last_name
        self.updated_at = datetime.utcnow()