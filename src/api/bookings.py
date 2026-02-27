from datetime import date

from fastapi import APIRouter
from pydantic import condecimal

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingCreateRequest, BookingCreate

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post(
    "/",
    summary="",
    description="",
    response_description="",
)
async def create_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_in: BookingCreateRequest,
):
    room = await db.rooms.read_one_or_none(id=booking_in.room_id)
    booking_data = BookingCreate(
        user_id=user_id,
        price=room.price,
        **booking_in.model_dump()
    )
    booking = await db.bookings.create(booking_data)
    await db.commit()
    return {"status": "OK", "created_booking": booking}