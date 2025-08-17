from fastapi.params import Depends
from fastapi.responses import JSONResponse
from api.schemas import RoomStatus
from repository.rooms_repository import RoomsRepository


class RoomsService:
    def __init__(self, rooms_repository: RoomsRepository = Depends(RoomsRepository)):
        self.rooms_repository = rooms_repository

    # Retrieves a room by its ID
    def get_room_by_id(self, room_id: int):
        try:
            return self.rooms_repository.get_room_by_id(room_id)
        except Exception as e:
            raise Exception(f"Error retrieving room with ID {room_id}")
        
    # Lists all rooms
    def list_all_rooms(self):
        try:
            return self.rooms_repository.list_all_rooms()
        except Exception as e:
            raise Exception("Error retrieving all rooms")
        
    # Get room status
    # This method checks the status of a room by its ID
    # It returns a RoomStatus indicating whether the room is occupied or available
    def room_status(self,room_id:int):
        try:
            if len(self.rooms_repository.get_status_room(room_id))>0:
                return RoomStatus(status="Ocupada",room_id=room_id) 
            else:
                return RoomStatus(status="Disponible",room_id=room_id) 
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": "Error retrieving room status "})     