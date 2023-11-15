from fastapi import FastAPI

from src.database import Base, engine
from src.faces.router import router as face_router
from src.users.router import router as user_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(face_router, prefix="/faces", tags=["faces"])
