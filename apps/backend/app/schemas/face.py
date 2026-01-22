# app/schemas/face.py
from pydantic import BaseModel


class FaceMatch(BaseModel):
    user_id: int
    distance: float


class FaceMatchResult(BaseModel):
    matches: list[FaceMatch]


class FaceUploadResponse(BaseModel):
    detected_faces: int
    matches: list[FaceMatch]

