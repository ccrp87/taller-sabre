from datetime import datetime
from pydantic import BaseModel


class Guest(BaseModel):
    id:int
    full_name:str
    email:str
    phone:str
    
    class Config:
        from_attributes = True
        
class ReservationCreateSchema(BaseModel):
    guest:Guest
    room_id :int
    check_in :datetime
    check_out :datetime
    status :str
    
    class Config:
        from_attributes = True
        
class ReservationResponseSchema(ReservationCreateSchema):
    id:int