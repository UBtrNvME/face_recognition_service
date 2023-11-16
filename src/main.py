from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import Base, engine
from src.face_recognition.router import router as face_recognition_router
from src.faces.router import router as face_router
from src.users.router import router as user_router

Base.metadata.create_all(engine)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(face_router, prefix="/faces", tags=["faces"])
app.include_router(face_recognition_router, prefix="/face_recognition", tags=["faces"])
