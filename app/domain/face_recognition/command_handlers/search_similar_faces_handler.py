# domain/face_recognition/command_handlers/search_similar_faces_handler.py
from domain.face_recognition.commands.search_similar_faces import (
    SearchSimilarFacesCommand,
)
from domain.face_recognition.ports.face_recognition_service import (
    FaceRecognitionService,
)
from domain.face_recognition.events.similar_faces_found_event import (
    SimilarFacesFoundEvent,
)


class SearchSimilarFacesHandler:
    def __init__(self, face_recognition_service: FaceRecognitionService):
        self.face_recognition_service = face_recognition_service

    def handle(self, command: SearchSimilarFacesCommand):
        # Search for similar faces in the vector DB
        similar_faces = self.face_recognition_service.search_similar_faces(
            command.face_encoding, command.similarity_threshold
        )

        # Emit similar faces found event
        return SimilarFacesFoundEvent(similar_faces=similar_faces)
