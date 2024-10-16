from pydantic import BaseModel


class RegisterUserCommand(BaseModel):
    username: str
