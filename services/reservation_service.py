from api.reservarion_schema import ReservationCreateSchema
from repository.reservation_repository import ReservationRepository


class ReservationService():
    def __init__(self, reservation_repository:ReservationRepository):
        self.reseration_repository = reservation_repository
        
    def create_reservation(self, reservation:ReservationCreateSchema):
        self.reseration_repository.create_reservation(reservation=reservation)