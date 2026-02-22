from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomCreateRequest, RoomCreate, RoomFilter, RoomFilterRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.post(
    "/{hotel_id}/rooms",
    summary="Создать номер (категорию) в отеле",
    description="Создаёт категорию номера для конкретного отеля по `hotel_id`"
)
async def create_room(
    hotel_id: int,
    room_in: RoomCreateRequest = Body(
        openapi_examples={
            "standard": {
                "summary": "Standard (базовый вариант)",
                "value": {
                    "title": "Standard",
                    "description": "1 двуспальная кровать, душ, Wi-Fi, 18 м²",
                    "price": "129.99",
                    "quantity": 12,
                },
            },
            "deluxe": {
                "summary": "Deluxe (улучшенный)",
                "value": {
                    "title": "Deluxe",
                    "description": "Вид на город, ванна, кофе-машина, 28 м²",
                    "price": "189.50",
                    "quantity": 6,
                },
            },
            "family": {
                "summary": "Family (семейный)",
                "value": {
                    "title": "Family",
                    "description": "2 кровати + диван, мини-кухня, 35 м²",
                    "price": "219.00",
                    "quantity": 4,
                },
            },
            "suite": {
                "summary": "Suite (люкс)",
                "value": {
                    "title": "Suite",
                    "description": "Гостиная + спальня, 55 м², панорамный вид",
                    "price": "399.99",
                    "quantity": 2,
                },
            },
        }
    ),
):
    room_data = RoomCreate(hotel_id=hotel_id, **room_in.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).create(room_data)
        await session.commit()
    return {"status": "OK", "created_room": room}


@router.get(
    "/{hotel_id)/rooms",
    summary="",
    description=""
)
async def read_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).read_filtered(hotel_id=hotel_id)


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="",
    description=""
)
async def read_rooms(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).read_one_or_none(hotel_id=hotel_id, id=room_id)


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="",
    description=""
)
async def update_room_all_params(
        hotel_id: int,
        room_id: int,
        room_in: RoomCreateRequest
):
    room_data = RoomCreate(hotel_id=hotel_id, **room_in.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).update(room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="",
    description=""
)
async def update_room_any_params(
        hotel_id: int,
        room_id: int,
        room_in: RoomFilterRequest
):
    room_data = RoomFilter(hotel_id=hotel_id, **room_in.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).update(room_data, id=room_id, hotel_id=hotel_id, is_patch=True)
        await session.commit()
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="",
    description=""
)
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
        return {"status": "OK"}