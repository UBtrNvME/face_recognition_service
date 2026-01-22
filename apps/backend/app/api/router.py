# app/api/router.py
from fastapi import APIRouter
from app.api.v1 import face_enroll, face_match, users, auth

api_router = APIRouter()

api_router.include_router(
    auth.router,
    prefix="/v1/auth",
    tags=["auth"]
)

api_router.include_router(
    users.router,
    prefix="/v1/users",
    tags=["users"]
)

api_router.include_router(
    face_enroll.router,
    prefix="/v1/face",
    tags=["face"]
)

api_router.include_router(
    face_match.router,
    prefix="/v1/face",
    tags=["face"]
)
