from datetime import datetime
from fastapi import Depends
from sqlmodel import Session, select, update

from api.schemas import ReservationResponseListSchema, StatusReservation
from db import get_session
from models import Guest, Reservation, Room


class ReservationRepository():
    def __init__(self, db_session: Session = Depends(get_session)):
        self.db_session = db_session
    
    # Create a new reservation
    def create_reservation(self, reservation):
        try:
            reservation_data = Reservation(**reservation.dict(exclude="guest"))
            reservation_data.status = StatusReservation.pending
            self.db_session.add(reservation_data)
            self.db_session.commit()
            self.db_session.refresh(reservation_data)
            return reservation_data
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error creating reservation.")
    
    # List all reservations with room and guest details
    def list_all_reservations(self):
       try:
            statement = (select(Reservation, Room,Guest)
            .join(Reservation, Room.id == Reservation.room_id)
            .join(Guest, Guest.id == Reservation.guest_id)
            )
            results = self.db_session.exec(statement).all()
            
            return [
                ReservationResponseListSchema(
                    reservation_id=reservation.id,
                    reservation_check_in=reservation.check_in,
                    reservation_check_out=reservation.check_out,
                    reservation_status=reservation.status,
                    room_id=room.id,
                    room_number=room.number,
                    guest_email=guest.email,
                    guest_full_name=guest.full_name,
                    guest_phone=guest.phone,
                    guest_id=guest.id
                )
                for reservation, room, guest in results
            
            ]
       except Exception as e:
           raise e
    
    # cancel all overlapping reservations
    # This method cancels all reservations that overlap with the given room and checkout date
    def cancel_all_overlaps(self,room_id,reservation_id:int):
        try:
            self.db_session.exec(update(Reservation).where((Reservation.id != reservation_id)&(Reservation.room_id == room_id) & (Reservation.status== StatusReservation.inhouse)).values(status=StatusReservation.cancelled))
            self.db_session.commit() 

        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error cancelling overlapping reservations for room {room_id}.")
        
    # find a reservation by ID
    def get_reservation_by_id(self,id:int)->Reservation:
        try:
            return self.db_session.get(Reservation, id)
        except Exception as e:
            raise Exception(f"Error finding reservation by id {id}")
    
    # Update a reservation
    def update_reservation(self,reservation,id=0):
        try:
            if id > 0:
                reservation.id = id        
            self.db_session.add(reservation)
            self.db_session.commit()
            self.db_session.refresh(reservation)
            return reservation
        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error updating reservation with id {id}")

        