from abc import ABC, abstractmethod
from domain.user.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User):
        pass

    @abstractmethod
    def find_by_id(self, user_id: str) -> User:
        pass

    @abstractmethod
    def update(self, user: User):
        pass
