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
):
    pass