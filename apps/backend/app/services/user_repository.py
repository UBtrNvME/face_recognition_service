# app/services/user_repository.py
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: dict) -> User:
        """Create a new user."""
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email_or_username(self, email_or_username: str) -> Optional[User]:
        """Get user by email or username."""
        return self.db.query(User).filter(
            or_(User.email == email_or_username, User.username == email_or_username)
        ).first()

    def update(self, user: User, update_data: dict) -> User:
        """Update user."""
        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        """Delete user."""
        self.db.delete(user)
        self.db.commit()

    def list_users(self, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
        """List users with pagination."""
        total = self.db.query(User).count()
        users = self.db.query(User).offset(skip).limit(limit).all()
        return users, total

