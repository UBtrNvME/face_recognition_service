# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.schemas.auth import RegisterRequest, Token
from app.schemas.user import UserResponse
from app.models.user import User

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    user_service = UserService(db)
    try:
        from app.schemas.user import UserCreate
        user_create = UserCreate(
            email=register_data.email,
            username=register_data.username,
            password=register_data.password,
            full_name=register_data.full_name
        )
        user = user_service.create_user(user_create)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login and get access token.
    Uses FastAPI's standard OAuth2PasswordRequestForm.
    Username field accepts either email or username.
    """
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_service.create_access_token(data={"sub": str(user.id)})
    print(access_token)
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information."""
    return current_user

