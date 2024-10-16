# domain/user/command_handlers/register_user_handler.py
from domain.user.models.user import User
from domain.user.commands.register_user_command import RegisterUserCommand
from domain.user.events.user_registered_event import UserRegisteredEvent
from domain.user.exceptions.user_exception import UserException
from domain.user.ports.user_repository import UserRepository
import uuid


class RegisterUserHandler:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def handle(self, command: RegisterUserCommand):
        # Check for existing user
        existing_user = self.user_repository.find_by_id(command.username)
        if existing_user:
            raise UserException(f"User {command.username} already exists.")

        # Create a new user
        user_id = str(uuid.uuid4())
        new_user = User(user_id=user_id, username=command.username)

        # Save the user
        self.user_repository.save(new_user)

        # Emit User Registered Event
        return UserRegisteredEvent(user_id=user_id, username=command.username)
