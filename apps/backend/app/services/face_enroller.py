# app/services/face_enroller.py
from sqlalchemy.orm import Session
from app.services.image_input import ImageInput
from app.services.face_service import FaceService
from app.services.face_repository import FaceRepository


class FaceEnroller:
    def __init__(self, db: Session):
        self.face_service = FaceService()
        self.repository = FaceRepository(db)

    def enroll_faces(self, user_id: int, image_input: ImageInput) -> int:
        """
        Extract faces from image and save encodings for user.
        Returns number of faces enrolled.
        """
        encodings = self.face_service.extract_encodings(image_input)
        faces_enrolled = self.repository.save_encodings(user_id, encodings)
        return faces_enrolled

