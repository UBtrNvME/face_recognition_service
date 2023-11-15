from typing import List

from pydantic import BaseModel


class FaceBase(BaseModel):
    vector: List[float]


class Face(FaceBase):
    id: int = -1
    user_id: int = -1

    class Config:
        from_attributes = True


class ClosestFaceRequest(FaceBase):
    threshold: float


class ClosestFaceResponse(BaseModel):
    user_id: int
    face_id: int
    euclidean_distance: float
