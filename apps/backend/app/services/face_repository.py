# app/services/face_repository.py
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, cast
from sqlalchemy.types import Float
from pgvector.sqlalchemy import Vector
import numpy as np
from app.models.face_encoding import FaceEncoding


class FaceRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_encodings(self, user_id: int, embeddings: List[np.ndarray]) -> int:
        """Save face encodings for a user. Returns number of encodings saved."""
        face_encodings = [
            FaceEncoding(
                user_id=user_id,
                embedding=embedding.tolist()  # Pass list directly, SQLAlchemy/pgvector will handle conversion
            )
            for embedding in embeddings
        ]
        self.db.add_all(face_encodings)
        self.db.commit()
        return len(face_encodings)

    def find_matches(
        self,
        embedding: np.ndarray,
        threshold: float = 0.6,
        limit: int = 10
    ) -> List[tuple[int, float]]:
        """
        Find matching face encodings using L2 distance in PostgreSQL.
        Returns list of (user_id, distance) tuples.
        """
        embedding_list = embedding.tolist()
        distance_expr = FaceEncoding.embedding.l2_distance(embedding_list)
        
        results = (
            self.db.query(
                FaceEncoding.user_id,
                cast(distance_expr, Float).label("distance")
            )
            .filter(cast(distance_expr, Float) <= threshold)
            .order_by(distance_expr)
            .limit(limit)
            .all()
        )
        
        return [(row.user_id, float(row.distance)) for row in results]

