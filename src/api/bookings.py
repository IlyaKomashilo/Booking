from datetime import date

from fastapi import APIRouter




router = APIRouter(prefix="/bookings", tags=["бронирования"])


@router.post(
    "/",
    summary="",
    description="",
    response_description="",
)
async def create_booking(
        room_id: int,
        date_from: date,
        date_to: date,
):
    pass