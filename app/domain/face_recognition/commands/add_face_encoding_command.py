from pydantic import BaseModel
from domain.face_recognition.types import FaceEncoding


class AddFaceEncodingCommand(BaseModel):
    user_id: str
    face_encoding: FaceEncoding
