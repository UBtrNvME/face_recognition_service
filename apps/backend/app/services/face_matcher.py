# app/services/face_matcher.py
from typing import List
from sqlalchemy.orm import Session
from app.services.image_input import ImageInput
from app.services.face_service import FaceService
from app.services.face_repository import FaceRepository
from app.schemas.face import FaceMatch


class FaceMatcher:
    def __init__(self, db: Session):
        self.face_service = FaceService()
        self.repository = FaceRepository(db)

    def match_faces(
        self,
        image_input: ImageInput,
        threshold: float = 0.6,
        limit: int = 10
    ) -> tuple[int, List[FaceMatch]]:
        """
        Extract faces from image and match against database.
        Returns (detected_faces_count, list of matches).
        """
        encodings = self.face_service.extract_encodings(image_input)
        detected_faces = len(encodings)
        
        all_matches = []
        for encoding in encodings:
            matches = self.repository.find_matches(encoding, threshold, limit)
            for user_id, distance in matches:
                all_matches.append(FaceMatch(user_id=user_id, distance=distance))
        
        return detected_faces, all_matches

