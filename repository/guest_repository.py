from fastapi import Depends
from sqlmodel import Session, select
from db import get_session
from models import Guest


class GuestRepository:
    def __init__(self, db_session: Session = Depends(get_session)):
        self.db_session = db_session
    
    # Retrieves a guest by their ID
    def find_guest_by_id(self,id:int):
        try:
            return self.db_session.exec(select(Guest).where(Guest.id==id)).first()
        except Exception as e:
            raise Exception(f"Error finding guest by id: {id}")
    
    # Creates a new guest
    def create_guest(self,guest):
        try:
            guest_data = Guest(**guest.dict())
            self.db_session.add(guest_data)
            self.db_session.commit()
            self.db_session.refresh(guest_data)
            return guest_data
        except Exception as e:
            raise Exception(f"Error creating guest.")