# app/models/face_encoding.py
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class FaceEncoding(Base):
    __tablename__ = "face_encodings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    embedding: Mapped[Vector] = mapped_column(Vector(128), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="face_encodings")

    __table_args__ = (
        Index("idx_face_encodings_user_id", "user_id"),
    )

