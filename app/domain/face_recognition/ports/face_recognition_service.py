# domain/face_recognition/ports/face_recognition_service.py
from abc import ABC, abstractmethod
from typing import List
from domain.user.models.user import FaceEncoding


class FaceRecognitionService(ABC):
    @abstractmethod
    def add_face_encoding(self, user_id: str, face_encoding: FaceEncoding):
        pass

    @abstractmethod
    def search_similar_faces(
        self, face_encoding: FaceEncoding, similarity_threshold: float
    ) -> List[str]:
        pass
