from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import (
    RoomCreate,
    RoomCreateRequest,
    RoomFilter,
    RoomFilterRequest,
)

router = APIRouter(prefix="/hotels", tags=["Номера"])

ROOM_CREATE_EXAMPLES = {
    "1": {
        "summary": "Standard",
        "value": {
            "title": "Standard",
            "description": "1 двуспальная кровать, душ, Wi-Fi, 18 м²",
            "price": "129.99",
            "quantity": 12,
        },
    },
    "2": {
        "summary": "Deluxe",
        "value": {
            "title": "Deluxe",
            "description": "Вид на город, ванна, кофе-машина, 28 м²",
            "price": "189.50",
            "quantity": 6,
        },
    },
    "3": {
        "summary": "Family",
        "value": {
            "title": "Family",
            "description": "2 кровати + диван, мини-кухня, 35 м²",
            "price": "219.00",
            "quantity": 4,
        },
    },
    "4": {
        "summary": "Suite",
        "value": {
            "title": "Suite",
            "description": "Гостиная + спальня, 55 м², панорамный вид",
            "price": "399.99",
            "quantity": 2,
        },
    },
    "5": {
        "summary": "Economy",
        "value": {
            "title": "Economy",
            "description": "Компактный номер, душ, 14 м²",
            "price": "89.00",
            "quantity": 20,
        },
    },
}

ROOM_PATCH_EXAMPLES = {
    "1": {
        "summary": "Изменить только цену",
        "value": {"price": "149.99"},
    },
    "2": {
        "summary": "Изменить только количество",
        "value": {"quantity": 10},
    },
    "3": {
        "summary": "Изменить название",
        "value": {"title": "Standard Plus"},
    },
    "4": {
        "summary": "Изменить описание",
        "value": {"description": "Обновлённое описание категории"},
    },
    "5": {
        "summary": "Изменить несколько полей",
        "value": {"title": "Family Comfort", "price": "249.00", "quantity": 3},
    },
}


@router.post(
    "/{hotel_id}/rooms",
    summary="Создание категории номера",
    description="Создаёт категорию номера для конкретного отеля по `hotel_id`.",
    response_description="Статус и данные созданной категории номера.",
)
async def create_room(
    hotel_id: int,
    room_in: RoomCreateRequest = Body(openapi_examples=ROOM_CREATE_EXAMPLES),
):
    room_data = RoomCreate(hotel_id=hotel_id, **room_in.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).create(room_data)
        await session.commit()
    return {"status": "OK", "created_room": room}


@router.get(
    "/{hotel_id}/rooms",
    summary="Список категорий номеров отеля",
    description="Возвращает все категории номеров, созданные для указанного отеля по hotel_id.",
    response_description="Список категорий номеров отеля.",
)
async def read_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).read_filtered(hotel_id=hotel_id)


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Просмотр категории номера",
    description="Возвращает категорию номера по room_id в рамках указанного отеля hotel_id.",
    response_description="Данные категории номера или null, если запись не найдена.",
)
async def read_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).read_one_or_none(
            hotel_id=hotel_id, id=room_id
        )


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полная замена категории номера",
    description="Полностью обновляет данные категории номера по room_id для указанного hotel_id.",
    response_description="Подтверждение успешного полного обновления категории номера.",
)
async def replace_room(
    hotel_id: int,
    room_id: int,
    room_in: RoomCreateRequest = Body(openapi_examples=ROOM_CREATE_EXAMPLES),
):
    room_data = RoomCreate(hotel_id=hotel_id, **room_in.model_dump())
    async with async_session_maker() as session:
        await RoomsRepository(session).update(room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}/rooms/{room_id}",
    summary="Частичное обновление категории номера",
    description="Обновляет только переданные поля категории номера по room_id для указанного hotel_id.",
    response_description="Подтверждение успешного частичного обновления категории номера.",
)
async def patch_room(
    hotel_id: int,
    room_id: int,
    room_in: RoomFilterRequest = Body(openapi_examples=ROOM_PATCH_EXAMPLES),
):
    room_data = RoomFilter(hotel_id=hotel_id, **room_in.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).update(
            room_data, id=room_id, hotel_id=hotel_id, is_patch=True
        )
        await session.commit()
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление категории номера",
    description="Удаляет категорию номера по room_id в рамках указанного hotel_id.",
    response_description="Подтверждение успешного удаления категории номера.",
)
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
        return {"status": "OK"}
