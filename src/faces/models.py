from sqlalchemy import Column, Float, ForeignKey, Integer

from src.database import Base

VECTOR_SIZE = 128


class Face(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    @property
    def vector(self):
        return [getattr(self, f"v{i}") for i in range(VECTOR_SIZE)]

    @vector.setter
    def vector(self, vector_data):
        for i, value in enumerate(vector_data):
            setattr(self, f"v{i}", value)


for i in range(VECTOR_SIZE):
    setattr(Face, f"v{i}", Column(Float, nullable=False))
