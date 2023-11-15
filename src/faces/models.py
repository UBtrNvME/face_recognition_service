from typing import List

from sqlalchemy import Column, Float, ForeignKey, Index, Integer, func
from sqlalchemy.ext.hybrid import hybrid_property

from src.database import Base

VECTOR_SIZE = 128


class Face(Base):
    __tablename__ = "faces"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    @hybrid_property
    def vector(self) -> List[float]:
        return [getattr(self, f"v{i}") for i in range(VECTOR_SIZE)]

    @vector.expression
    def vector(cls):
        print(func.json_array([getattr(cls, f"v{i}") for i in range(VECTOR_SIZE)]))
        return func.json_array([getattr(cls, f"v{i}") for i in range(VECTOR_SIZE)])

    @vector.setter
    def vector(self, value: List[float]):
        for i, v in enumerate(value):
            setattr(self, f"v{i}", v)

    @classmethod
    def create(cls, user_id, vector: List[float]):
        data = {f"v{i}": value for i, value in enumerate(vector)}
        return cls(user_id=user_id, **data)


for i in range(VECTOR_SIZE):
    setattr(Face, f"v{i}", Column(Float, nullable=False))

vector_components = Face.__table__.c
Index(
    "ix_vector_components",
    *(getattr(vector_components, f"v{i}") for i in range(VECTOR_SIZE)),
)
