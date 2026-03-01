from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingCreate, BookingCreateRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post(
    "/",
    summary="Создание бронирования",
    description=(
        "Создаёт бронирование для текущего пользователя. "
        "Проверяет существование номера и валидность диапазона дат."
    ),
    response_description="Статус операции и созданное бронирование.",
)
async def create_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_in: BookingCreateRequest,
):
    """Создаёт бронирование пользователя с бизнес-валидацией входных данных."""

    room = await db.rooms.read_one_or_none(id=booking_in.room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Номер не найден")
    if booking_in.date_to <= booking_in.date_from:
        raise HTTPException(
            status_code=400,
            detail="Дата выезда должна быть позже даты заезда",
        )

    booking_data = BookingCreate(
        user_id=user_id,
        price=room.price,
        **booking_in.model_dump(),
    )
    booking = await db.bookings.create(booking_data)
    await db.commit()
    return {"status": "OK", "created_booking": booking}
