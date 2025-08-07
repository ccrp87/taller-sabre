from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from services.rooms_services import RoomsService
from api.schemas import RoomStatus, RoomsSchema

room_router = APIRouter(prefix="/api", tags=["Manage Rooms"])

@room_router.get("/rooms/{room_id}/status",response_model=RoomStatus,description="Obtiene el estado actual de una habitación específica por su ID.")
async def rooms_status(room_id:int, room_service:RoomsService = Depends(RoomsService)):
    try:
        return room_service.room_status(room_id)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error retrieving room status"})
    
@room_router.get("/rooms", response_model=List[RoomsSchema], description="Lista todas las habitaciones disponibles con sus detalles.")
async def list_rooms(rooms_service: RoomsService = Depends(RoomsService)):
    try:
        return rooms_service.list_all_rooms()
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error listing rooms"})