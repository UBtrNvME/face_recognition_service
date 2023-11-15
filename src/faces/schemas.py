from typing import List

from pydantic import BaseModel


class FaceBase(BaseModel):
    user_id: int


class FaceCreate(FaceBase):
    image: str


class Face(FaceBase):
    id: int
    vector: List[str]

    class Config:
        orm_mode: True
