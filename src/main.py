from fastapi import FastAPI

from src.database import Base, engine
from src.users.router import router as user_router

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["users"])
