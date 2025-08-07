from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import SQLModel
from api.reservation_router import reservation_router
from api.room_router import room_router
from db import engine


@asynccontextmanager
async def lifespan(app:FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan, title="Hotel Reservation API", version="1.0.0")
app.include_router(reservation_router)
app.include_router(room_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Hotel Reservation API"}


