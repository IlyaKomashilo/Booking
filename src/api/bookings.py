from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingCreate, BookingCreateRequest

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post(
    "",
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
        raise HTTPException(
            status_code=404, detail="Номер не найден",
        )
    if booking_in.date_to <= booking_in.date_from:
        raise HTTPException(
            status_code=400, detail="Дата выезда должна быть позже даты заезда",
        )

    booking_data = BookingCreate(
        user_id=user_id,
        price=room.price,
        **booking_in.model_dump(),
    )
    booking = await db.bookings.create(booking_data)
    await db.commit()
    return {"status": "OK", "created_booking": booking}


@router.get(
    "",
    summary="Получение списка всех бронирований для администрирования",
    description="Возвращает список всех бронирований",
    response_description="Список всех бронирований",
)
async def read_bookings(
    db: DBDep,
):
    """Возвращает список всех бронирований."""

    return await db.bookings.read_all()


@router.get(
    "/me",
    summary="Получение списка всех бронирований текущего пользователя",
    description="Инициализирует пользователя и возвращает список его бронирований",
    response_description="Список бронирований текущего пользователя",
)
async def read_user_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    """Возвращает список всех бронирований."""

    return await db.bookings.read_filtered(user_id=user_id)