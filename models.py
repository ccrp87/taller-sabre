from datetime import datetime
from sqlmodel import Field, SQLModel


class Guest(SQLModel, table=True):
    id:int = Field(primary_key=True, nullable=False)
    full_name:str = Field(nullable=False)
    email:str = Field(nullable=False)
    phone:str = Field(nullable= False)
    
    
class Room(SQLModel, table=True):
    id:int = Field(primary_key=True)
    number:str = Field(nullable=False)
    
class Reservation(SQLModel, table= True):
    id:int = Field(primary_key=True)
    guest_id :int = Field(foreign_key="guest.id") 
    room_id :int = Field(foreign_key="room.id") 
    check_in:datetime = Field(default=None)
    check_out :datetime = Field(default=None)
    status : str = Field(default=None) 

