from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import src.users.crud as users_repo
from src.database import get_db
from src.users import schemas
from src.users.schemas import UserCreate

router = APIRouter()


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = users_repo.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users_repo.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/", response_model=schemas.User)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    user = users_repo.get_user_by_email(db, email=user_create.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users_repo.create_user(db=db, user=user_create)
