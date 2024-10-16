from pydantic import BaseModel
from typing import Optional
from domain.face_recognition.types import FaceEncoding


class User(BaseModel):
    user_id: str
    username: str
    face_encoding: Optional[FaceEncoding] = None

    def add_face_encoding(self, encoding: FaceEncoding):
        self.face_encoding = encoding
