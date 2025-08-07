from datetime import datetime
from enum import Enum
from pydantic import BaseModel, EmailStr


class GuestCreateSchema(BaseModel):
    full_name:str
    email:EmailStr
    phone:str
    
    class Config:
        from_attributes = True

class GuestResponseSchema(GuestCreateSchema):
    id:int
    
class StatusReservation(str, Enum):
    pending = "pending"
    inhouse = "inhouse"
    completed = "completed"
    cancelled = "cancelled"
  
class ReservationCreateSchema(BaseModel):
    guest_id :int
    guest: GuestCreateSchema
    room_id :int
    check_in :datetime
    check_out :datetime
    status :StatusReservation
    
    class Config:
        from_attributes = True
        
class ReservationUpdateSchema(BaseModel):
    room_id :int
    check_in :datetime
    check_out :datetime
    
    class Config:
        from_attributes = True
        
        
class ReservationCheckInSchema(BaseModel):
    guest_id :int
    room_id :int
    check_in :datetime
    check_out :datetime
    status :StatusReservation
    
    class Config:
        from_attributes = True
        

class ReservationResponseSchema(ReservationCreateSchema):
    id:int
    
class ReservationResponseListSchema(BaseModel):
    reservation_id:int
    reservation_check_in :datetime
    reservation_check_out :datetime
    reservation_status :StatusReservation
    guest_id:int
    guest_full_name:str
    guest_email:str
    guest_phone:str
    room_id:int
    room_number:str
    
class RoomStatus(BaseModel):
    status:str
    room_id:int
    
class GeneralStatusResponse(BaseModel):
    message:str
    
class RoomsSchema(BaseModel):
    id:int
    number:str