from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache


from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityCreate
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
}

ROOM_PATCH_EXAMPLES = {
    "1": {
        "summary": "Изменить только цену",
        "value": {"price": "149.99"},
    },
    "2": {
        "summary": "Изменить список удобств",
        "value": {"facilities_ids": [1, 2, 4]},
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
    db: DBDep,
    room_in: RoomCreateRequest = Body(openapi_examples=ROOM_CREATE_EXAMPLES),
):
    room_payload = room_in.model_dump(exclude={"facilities_ids"})
    room_data = RoomCreate(hotel_id=hotel_id, **room_payload)
    room = await db.rooms.create(room_data)

    if room_in.facilities_ids:
        rooms_facilities_data = [
            RoomFacilityCreate(room_id=room.id, facility_id=f_id)
            for f_id in room_in.facilities_ids
        ]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)

    await db.commit()
    return {"status": "OK", "created_room": room}


@router.get(
    "/{hotel_id}/rooms",
    summary="Список категорий номеров отеля",
    description="Возвращает все категории номеров, созданные для указанного отеля по hotel_id.",
    response_description="Список категорий номеров отеля.",
)
@cache(expire=30)
async def read_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(),
    date_to: date = Query(),
):
    return await db.rooms.read_filtered_by_time(
        hotel_id=hotel_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.get(
    "/{hotel_id}/rooms/{room_id}",
    summary="Просмотр категории номера",
    description="Возвращает категорию номера по room_id в рамках указанного отеля hotel_id.",
    response_description="Данные категории номера или null, если запись не найдена.",
)
@cache(expire=30)
async def read_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.read_one_or_none_with_rels(hotel_id=hotel_id, id=room_id)


@router.put(
    "/{hotel_id}/rooms/{room_id}",
    summary="Полная замена категории номера",
    description="Полностью обновляет данные категории номера по room_id для указанного hotel_id.",
    response_description="Подтверждение успешного полного обновления категории номера.",
)
async def replace_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
    room_in: RoomCreateRequest = Body(openapi_examples=ROOM_CREATE_EXAMPLES),
):
    room_payload = room_in.model_dump(exclude={"facilities_ids"})
    room_data = RoomCreate(hotel_id=hotel_id, **room_payload)
    await db.rooms.update(room_data, id=room_id, hotel_id=hotel_id)
    await db.rooms_facilities.set_room_facilities(
        room_id=room_id, facilities_ids=room_in.facilities_ids
    )
    await db.commit()
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
    db: DBDep,
    room_in: RoomFilterRequest = Body(openapi_examples=ROOM_PATCH_EXAMPLES),
):
    room_data_dict = room_in.model_dump(exclude_unset=True)
    facilities_ids = room_data_dict.pop("facilities_ids", None)
    room_data = RoomFilter(hotel_id=hotel_id, **room_data_dict)

    if room_data_dict:
        await db.rooms.update(room_data, id=room_id, hotel_id=hotel_id, is_patch=True)
    if facilities_ids is not None:
        await db.rooms_facilities.set_room_facilities(
            room_id=room_id,
            facilities_ids=facilities_ids,
        )

    await db.commit()
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}/rooms/{room_id}",
    summary="Удаление категории номера",
    description="Удаляет категорию номера по room_id в рамках указанного hotel_id.",
    response_description="Подтверждение успешного удаления категории номера.",
)
async def delete_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}
