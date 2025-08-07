
from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from services.reservation_service import ReservationService
from api.schemas import ReservationCheckInSchema, ReservationCreateSchema, ReservationResponseListSchema, ReservationResponseSchema, ReservationUpdateSchema


reservation_router = APIRouter(prefix="/api", tags=["Manage Reservations"])


@reservation_router.post("/reservation/",response_model=ReservationResponseSchema, description="Crea un huésped (si no existe) y una reserva con estado 'pending'.")
async def create_reservation( reservation:ReservationCreateSchema, reservation_service:ReservationService = Depends(ReservationService)):
    try:
        return reservation_service.create_reservation(reservation)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error creating reservation"})

@reservation_router.get("/reservations/",response_model=List[ReservationResponseListSchema], description="Lista todas las reservas con detalles de la habitación y el huésped asociado.")
async def get_reservation( reservation_service:ReservationService = Depends(ReservationService)):
    try:
        return reservation_service.list_all_reservation()
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error listing reservations"})

@reservation_router.put("/reservations/{id}/checkin",response_model=ReservationCheckInSchema,description="Actualiza el estado de una reserva a 'inhouse' y cancela cualquier reserva superpuesta.")
async def check_in_reservation(id:int, reservation_service:ReservationService = Depends(ReservationService)):
    try:
        return reservation_service.reservation_checkin(id)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error checking in reservation"})
    
@reservation_router.put("/reservations/{id}/checkout",response_model=ReservationCheckInSchema, description="Actualiza el estado de una reserva a 'completed' y libera la habitación asociada.")
async def check_out_reservation(id:int, reservation_service:ReservationService = Depends(ReservationService)):
    try:
        return reservation_service.reservation_checkout(id)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error checking out reservation"})

@reservation_router.put("/reservations/{id}/cancelled",response_model=ReservationCheckInSchema, description="Actualiza el estado de una reserva a 'cancelled' y libera la habitación asociada.")
async def cancel_reservation(id:int, reservation_service:ReservationService = Depends(ReservationService)):
    try:
        return reservation_service.cancel_reservation(id)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error cancelling reservation"})
    
@reservation_router.put("/reservations/{id}",response_model=ReservationCheckInSchema, description="Actualiza los detalles de una reserva existente, incluyendo las fechas de check-in y check-out, y el ID de la habitación.")
async def update_reservation(id:int,reservation:ReservationUpdateSchema, reservation_service:ReservationService = Depends(ReservationService)):
    try:
        return reservation_service.update_reservation(reservation,id)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error updating reservation"})
    
@reservation_router.get("/reservations/{id}",response_model=ReservationCheckInSchema, description="Obtiene los detalles de una reserva específica por su ID.")
async def reservation_detail(id:int, reservation_service:ReservationService = Depends(ReservationService)):
    try:
        return reservation_service.reservation_detail(id)
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Error retrieving reservation details"})