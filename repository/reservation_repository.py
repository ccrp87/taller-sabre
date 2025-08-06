from fastapi import Depends
from sqlmodel import Session

from db import get_session
from models import Reservation


class ReservationRepository():
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        
    def create_reservation(self, reservation):
            self.session.add(Reservation(**reservation.dict()))
            self.session.commit()
            return self.session.refresh()