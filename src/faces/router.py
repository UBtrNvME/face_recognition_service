from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.database import get_db
from src.faces import crud as faces_repo
from src.faces import schemas, services

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/{user_id}", response_model=schemas.Face)
def create_face_encoding(user_id: int, file: UploadFile = File(), db=Depends(get_db)):
    face_encoding = services.generate_face_encoding_from_image(file)
    if face_encoding is None:
        raise HTTPException(status_code=404, detail="No face encoding in image")
    return faces_repo.create_face_encoding(
        db, user_id=user_id, face_encoding=face_encoding.tolist()
    )


@router.post("/unknown/encode", response_model=schemas.Face)
def get_face_encoding_for_unknown(file: UploadFile = File()):
    face_encoding = services.generate_face_encoding_from_image(file)
    if face_encoding is None:
        raise HTTPException(status_code=404, detail="No face encoding in image")
    return schemas.Face(vector=face_encoding.tolist())


@router.get("/{face_id}", response_model=schemas.Face)
def read_face_encoding_by_id(face_id: int, db=Depends(get_db)):
    face_encoding = faces_repo.get_face_encoding(db, face_id=face_id)
    if face_encoding is None:
        raise HTTPException(status_code=404, detail="Face encoding not found")
    return face_encoding


@router.get("/user/{user_id}")
def read_face_encoding_by_user_id(user_id: int, db=Depends(get_db)):
    # Check authentication or authorization if needed
    # ...

    # Retrieve face encoding by user ID
    face_encoding = faces_repo.get_face_encoding_by_user_id(db, user_id)
    if face_encoding is None:
        raise HTTPException(status_code=404, detail="Face encoding not found")
    return face_encoding


@router.post("/unknown/closest", response_model=schemas.ClosestFaceResponse)
def read_closest_face_encoding(
    find_closest_face: schemas.ClosestFaceRequest,
    db=Depends(get_db),
):
    result = faces_repo.get_closest_face_encoding(
        db, find_closest_face.vector, find_closest_face.threshold
    )
    if result is None:
        raise HTTPException(status_code=404, detail="No matching face encoding found")
    face_id, user_id, square_distance = result
    return schemas.ClosestFaceResponse(
        face_id=face_id,
        user_id=user_id,
        euclidean_distance=square_distance**0.5,
    )


@router.get("/", response_model=list[schemas.Face])
def read_faces(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return faces_repo.get_faces(db, skip, limit)
