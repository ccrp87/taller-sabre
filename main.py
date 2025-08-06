from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from sqlmodel import SQLModel
from api.reservarion_schema import ReservationCreateSchema, ReservationResponseSchema
from services.reservation_service import ReservationService
from db import engine


@asynccontextmanager
async def lifespan(app:FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/reservation",response_model=None)
async def create_reservation( ):
    #return reservation_service.create_reservation()
    print("")