from typing import List, Union

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.faces import models, schemas


def create_face_encoding(db: Session, user_id: int, face_encoding: List[float]):
    face_encoding = models.Face.create(user_id=user_id, vector=face_encoding)
    db.add(face_encoding)
    db.commit()
    db.refresh(face_encoding)
    return convert_to_schema(face_encoding)


def get_face_encoding_by_user_id(db: Session, user_id: int):
    return convert_to_schema(
        db.query(models.Face).filter(models.Face.user_id == user_id).first()
    )


def get_faces(db: Session, skip: int = 0, limit: int = 100):
    return convert_to_schema(db.query(models.Face).offset(skip).limit(limit).all())


def get_face_encoding(db: Session, face_id: int):
    return convert_to_schema(
        db.query(models.Face).filter(models.Face.id == face_id).first()
    )


def calculate_square_distance(face, unknown_face_encoding):
    return sum(
        (getattr(face, f"v{i}") - value) ** 2
        for i, value in enumerate(unknown_face_encoding)
    )


def get_closest_face_encoding(
    db: Session, unknown_face_encoding: List[float], threshold: float
):
    squared_distance = " + ".join(
        f"(v{i} - {value}) * (v{i} - {value})"
        for i, value in enumerate(unknown_face_encoding)
    )
    query = text(
        f"""SELECT id, user_id, {squared_distance} AS squared_distance
    FROM {models.Face.__tablename__}
    WHERE 
    {squared_distance} <= {threshold ** 2}
    ORDER BY squared_distance ASC LIMIT 1
    """
    )
    result = db.execute(query).fetchone()
    return result


# The rest of your code remains unchanged.


def convert_to_schema(faces: Union[models.Face, List[models.Face]]):
    return faces
    if not isinstance(faces, list):
        faces = [faces]
    result = [schemas.Face.from_orm(face) for face in faces]
    count = len(result)
    return result if count > 1 else result[0]
