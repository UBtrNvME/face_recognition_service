# domain/user/events/face_encoding_added_event.py
from pydantic import BaseModel


class FaceEncodingAddedEvent(BaseModel):
    user_id: str
