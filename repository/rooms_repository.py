from datetime import datetime
from fastapi import Depends
from sqlmodel import Session, select

from db import get_session
from models import Reservation, Room, StatusReservation


class RoomsRepository:
    def __init__(self, db_session: Session = Depends(get_session)):
        self.db_session = db_session
        
    # Retrieves a room by its ID
    def get_room_by_id(self, room_id: int):
        try:
            return self.db_session.get(Room, room_id)
        except Exception as e:
            raise Exception(f"Error finding room by id.")
        
    # Lists all rooms
    def list_all_rooms(self):
        try:
            return self.db_session.exec(select(Room)).all()
        except Exception as e:
            raise Exception(f"Error listing rooms.")
        
    # Retrieves the status of a room
    def get_status_room(self,room_id):
        try:
            return self.db_session.exec(select(Reservation).where((Reservation.room_id == room_id) & (Reservation.status== StatusReservation.inhouse)&(Reservation.check_out >= datetime.now())&(Reservation.check_in <= datetime.now()))).all()
        except Exception as e:
            raise Exception(f"Error getting room status.")