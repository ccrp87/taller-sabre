from datetime import datetime
from fastapi import Depends, Response
from fastapi.responses import JSONResponse
from api.schemas import GuestCreateSchema, ReservationCreateSchema, ReservationResponseSchema, RoomStatus
from models import StatusReservation
from repository.guest_repository import GuestRepository
from repository.reservation_repository import ReservationRepository
from repository.rooms_repository import RoomsRepository


class ReservationService():
    def __init__(self, reservation_repository:ReservationRepository=Depends(ReservationRepository),guest_repository:GuestRepository=Depends(GuestRepository),room_repository:RoomsRepository=Depends(RoomsRepository)):
        self.reservation_repository = reservation_repository
        self.guest_repository = guest_repository
        self.room_repository = room_repository
    
    # Create a new reservation
    # This method creates a new reservation, checking if the guest exists or needs to be created
    # It returns a ReservationResponseSchema with the reservation details
    def create_reservation(self, reservation:ReservationCreateSchema):
        try:
            
            room = self.room_repository.get_room_by_id(reservation.room_id)
            if not room:
                return JSONResponse(status_code=404, content={"message": "Room not found"})
            
            # Check if the guest exists, if not, create a new guest
            guest = self.guest_repository.find_guest_by_id(reservation.guest_id)
            if not guest:
                guest = self.guest_repository.create_guest(reservation.guest)
            # Create the reservation
            reservation.guest_id = guest.id
            reservation_data = self.reservation_repository.create_reservation(reservation=reservation)
            
            return ReservationResponseSchema(
                room_id=reservation_data.room_id,
                check_out=reservation_data.check_out,
                check_in=reservation_data.check_in,
                guest_id=guest.id,
                status=reservation_data.status,
                guest=GuestCreateSchema(
                    email=guest.email,
                    full_name=guest.full_name,
                    phone=guest.phone
                    ),
                id=reservation_data.id
            )
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": f"Error creating reservation {e} "})
        
    # List all reservations
    # This method retrieves all reservations and returns them as a list of ReservationResponseListSchema
    # It includes details about the room and guest associated with each reservation
    def list_all_reservation(self):
        try:
            return self.reservation_repository.list_all_reservations()
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": "Error listing reservations"})
        
    # Check-in a reservation
    # This method updates the status of a reservation to 'inhouse' and cancels any overlapping reservations
    # It returns the updated reservation data
    def reservation_checkin(self,id_reservation:int):
        try:
            reservation = self.reservation_repository.get_reservation_by_id(id_reservation)
            if not reservation:
                return JSONResponse(status_code=404, content={"message": "Reservation not found"})
            
            reservation.status = StatusReservation.inhouse
            print(self.reservation_repository.update_reservation(reservation))
            self.reservation_repository.cancel_all_overlaps(reservation.room_id, id_reservation)
            return reservation
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": "Error checking in reservation"})
        
    # Check-out a reservation
    # This method updates the status of a reservation to 'completed'
    # It returns the updated reservation data
    def reservation_checkout(self,id_reservation:int):
        try:
            reservation = self.reservation_repository.get_reservation_by_id(id_reservation)
            if not reservation:
                return JSONResponse(status_code=404,content={"message": "Reservation not found"})
            
            reservation.status = StatusReservation.completed
            self.reservation_repository.update_reservation(reservation)
            return reservation
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": "Error checking out reservation"})
        
    # Cancel a reservation
    # This method updates the status of a reservation to 'cancelled'
    # It returns the updated reservation data
    def cancel_reservation(self,id_reservation:int):
        try:
            reservation = self.reservation_repository.get_reservation_by_id(id_reservation)
            if not reservation:
                return JSONResponse(status_code=404, content={"message": "Reservation not found"})
            
            reservation.status = StatusReservation.cancelled
            self.reservation_repository.update_reservation(reservation)
            return reservation
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": "Error cancelling reservation"})
        
    # Update a reservation
    # This method updates the details of a reservation, including check-in and check-out dates and room ID
    # It returns the updated reservation data
    def update_reservation(self,reservation,id):
        try:
            reservation_data = self.reservation_repository.get_reservation_by_id(id)
            if not reservation:
                return JSONResponse(status_code=404 , content={"message": "Reservation not found"})
            
            room = self.room_repository.get_room_by_id(reservation.room_id)
            if not room:
                return JSONResponse(status_code=404, content={"message": "Room not found"})
            
            reservation_data.check_in = reservation.check_in
            reservation_data.check_out = reservation.check_out
            reservation_data.room_id = reservation.room_id
            return self.reservation_repository.update_reservation(reservation_data,id)
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": "Error updating reservation"})
        
    # Get reservation details by ID
    # This method retrieves a reservation by its ID and returns its details
    # It returns a ReservationCheckInSchema with the reservation information
    def reservation_detail(self,id):
        try:
            return self.reservation_repository.get_reservation_by_id(id)
        except Exception as e:
            return JSONResponse(status_code=500, content={"message": "Error retrieving reservation details"})
        
                