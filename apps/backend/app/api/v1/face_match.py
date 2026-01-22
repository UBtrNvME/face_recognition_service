# app/api/v1/face_match.py
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.image_input import FileImageInput
from app.services.face_matcher import FaceMatcher
from app.schemas.face import FaceUploadResponse

router = APIRouter()


@router.post("/match", response_model=FaceUploadResponse)
async def match_face(
    file: UploadFile = File(..., description="Image file to match"),
    threshold: float = Query(0.6, ge=0.0, le=1.0, description="Distance threshold for matching"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of matches per face"),
    db: Session = Depends(get_db)
):
    """Match faces from uploaded image against enrolled faces."""
    image_bytes = await file.read()
    image_input = FileImageInput(image_bytes)
    
    matcher = FaceMatcher(db)
    detected_faces, matches = matcher.match_faces(image_input, threshold, limit)
    
    return FaceUploadResponse(
        detected_faces=detected_faces,
        matches=matches
    )

