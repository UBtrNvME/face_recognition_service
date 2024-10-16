# domain/user/command_handlers/update_user_handler.py
from app.domain.user.events.face_encoding_added_event import FaceEncodingAddedEvent
from domain.user.commands.add_face_encoding_command import AddFaceEncodingCommand

from domain.user.exceptions.user_exception import UserException
from domain.user.ports.user_repository import UserRepository


class AddFaceEncodingHandler:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def handle(self, command: AddFaceEncodingCommand):
        user = self.user_repository.find_by_id(command.user_id)
        if not user:
            raise UserException(f"User with ID {command.user_id} not found.")

        # Update face encoding
        user.add_face_encoding(command.face_encoding)

        # Save the updated user
        self.user_repository.update(user)

        # Emit User Updated Event
        return FaceEncodingAddedEvent(user_id=command.user_id)
