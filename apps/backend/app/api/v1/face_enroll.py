# app/api/v1/face_enroll.py
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.image_input import FileImageInput
from app.services.face_enroller import FaceEnroller
from app.schemas.face_enroll import FaceEnrollResponse

router = APIRouter()


@router.post("/enroll", response_model=FaceEnrollResponse)
async def enroll_face(
    user_id: int = Query(..., description="User ID to enroll"),
    file: UploadFile = File(..., description="Image file containing faces"),
    db: Session = Depends(get_db)
):
    """Enroll faces from uploaded image for a user."""
    from app.services.user_service import UserService
    
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    
    image_bytes = await file.read()
    image_input = FileImageInput(image_bytes)
    
    enroller = FaceEnroller(db)
    faces_enrolled = enroller.enroll_faces(user_id, image_input)
    
    return FaceEnrollResponse(
        user_id=user_id,
        faces_enrolled=faces_enrolled
    )

