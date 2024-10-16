# domain/face_recognition/command_handlers/add_face_encoding_handler.py
from domain.face_recognition.commands.add_face_encoding import AddFaceEncodingCommand
from domain.face_recognition.ports.face_recognition_service import (
    FaceRecognitionService,
)
from domain.user.ports.user_repository import UserRepository
from domain.user.exceptions.user_exception import UserException


class AddFaceEncodingHandler:
    def __init__(
        self,
        user_repository: UserRepository,
        face_recognition_service: FaceRecognitionService,
    ):
        self.user_repository = user_repository
        self.face_recognition_service = face_recognition_service

    def handle(self, command: AddFaceEncodingCommand):
        # Ensure the user exists
        user = self.user_repository.find_by_id(command.user_id)
        if not user:
            raise UserException(f"User with ID {command.user_id} not found.")

        # Add face encoding
        user.add_face_encoding(command.face_encoding)
        self.user_repository.update(user)

        # Store encoding in vector DB
        self.face_recognition_service.add_face_encoding(
            command.user_id, command.face_encoding
        )

        # Emit face encoding added event
        return FaceEncodingAddedEvent(user_id=command.user_id)
