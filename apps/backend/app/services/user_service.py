# app/services/user_service.py
from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.services.user_repository import UserRepository
from app.services.auth_service import AuthService


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
        self.auth_service = AuthService(db)

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user with validation and password hashing."""
        if self.repository.get_by_email(user_data.email):
            raise ValueError(f"User with email {user_data.email} already exists")
        if self.repository.get_by_username(user_data.username):
            raise ValueError(f"User with username {user_data.username} already exists")

        user_dict = user_data.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.auth_service.get_password_hash(password)
        user_dict["is_active"] = True

        return self.repository.create(user_dict)

    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.repository.get_by_id(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.repository.get_by_email(email)

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.repository.get_by_username(username)

    def update_user(self, user_id: int, update_data: UserUpdate) -> Optional[User]:
        """Update user with validation."""
        user = self.repository.get_by_id(user_id)
        if not user:
            return None

        update_dict = update_data.model_dump(exclude_unset=True)

        if "email" in update_dict and update_dict["email"]:
            existing = self.repository.get_by_email(update_dict["email"])
            if existing and existing.id != user_id:
                raise ValueError(f"User with email {update_dict['email']} already exists")

        if "username" in update_dict and update_dict["username"]:
            existing = self.repository.get_by_username(update_dict["username"])
            if existing and existing.id != user_id:
                raise ValueError(f"User with username {update_dict['username']} already exists")

        return self.repository.update(user, update_dict)

    def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        user = self.repository.get_by_id(user_id)
        if not user:
            return False
        self.repository.delete(user)
        return True

    def list_users(self, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
        """List users with pagination."""
        return self.repository.list_users(skip, limit)

