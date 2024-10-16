# domain/face_recognition/commands/search_similar_faces.py
from pydantic import BaseModel
from domain.user.models.user import FaceEncoding


class SearchSimilarFacesCommand(BaseModel):
    face_encoding: FaceEncoding
    similarity_threshold: float = 0.6
