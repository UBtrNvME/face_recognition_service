# app/services/auth_service.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.config import settings
from app.services.user_repository import UserRepository
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password."""
        print(password)
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> Optional[dict]:
        """Decode and verify a JWT token."""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            return payload
        except JWTError:
            return None

    def authenticate_user(self, email_or_username: str, password: str) -> Optional[User]:
        """Authenticate a user by email/username and password."""
        user = self.repository.get_by_email_or_username(email_or_username)
        if not user:
            return None
        if not user.is_active:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from JWT token."""
        payload = self.decode_access_token(token)
        print(payload)
        if payload is None:
            return None
        user_id = payload.get("sub")
        if user_id is None:
            return None
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return None
        user = self.repository.get_by_id(user_id)
        if not user or not user.is_active:
            return None
        return user

