from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from api.reservation_router import reservation_router
from api.room_router import room_router
from db import engine


@asynccontextmanager
async def lifespan(app:FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan, title="Hotel Reservation API", version="1.0.0")

origins = [
    "https://brave-wave-0ff2b8a0f.1.azurestaticapps.net",
    "https://myapp.3itc.co",
    "https://myapp2.3itc.co",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(reservation_router)
app.include_router(room_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Hotel Reservation API3"}


