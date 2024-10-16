# domain/face_recognition/events/similar_faces_found_event.py
from pydantic import BaseModel
from typing import List


class SimilarFacesFoundEvent(BaseModel):
    similar_faces: List[str]  # List of user IDs that match the encoding
