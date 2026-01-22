# app/schemas/face_enroll.py
from pydantic import BaseModel


class FaceEnrollResponse(BaseModel):
    user_id: int
    faces_enrolled: int

