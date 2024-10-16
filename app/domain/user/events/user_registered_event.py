# domain/user/events/user_registered_event.py
from pydantic import BaseModel


class UserRegisteredEvent(BaseModel):
    user_id: str
    username: str
