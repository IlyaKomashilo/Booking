from fastapi import APIRouter, Body, Depends

from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelCreate, HotelFilter

router = APIRouter(prefix="/hotels", tags=["Отели"])

HOTEL_EXAMPLES = {
    "1": {
        "summary": "Atlantis The Palm (Dubai)",
        "value": {
            "title": "Atlantis The Palm",
            "location": "Crescent Rd, The Palm Jumeirah, Dubai, United Arab Emirates",
        },
    },
    "2": {
        "summary": "Burj Al Arab Jumeirah (Dubai)",
        "value": {
            "title": "Burj Al Arab Jumeirah",
            "location": "Jumeirah St, Umm Suqeim 3, Dubai, United Arab Emirates",
        },
    },
    "3": {
        "summary": "The Ritz-Carlton, Moscow (Moscow)",
        "value": {
            "title": "The Ritz-Carlton, Moscow",
            "location": "Tverskaya St, 3, Moscow, Russia",
        },
    },
    "4": {
        "summary": "Hotel Arts Barcelona (Barcelona)",
        "value": {
            "title": "Hotel Arts Barcelona",
            "location": "Carrer de la Marina, 19-21, 08005 Barcelona, Spain",
        },
    },
    "5": {
        "summary": "The Savoy (London)",
        "value": {
            "title": "The Savoy",
            "location": "Strand, London WC2R 0EZ, United Kingdom",
        },
    },
}

HOTEL_PATCH_EXAMPLES = {
    "1": {
        "summary": "Обновить только название",
        "value": {"title": "Atlantis The Palm Resort"},
    },
    "2": {
        "summary": "Обновить только локацию",
        "value": {"location": "Palm Jumeirah, Dubai, UAE"},
    },
    "3": {
        "summary": "Обновить оба поля",
        "value": {
            "title": "The Ritz-Carlton Moscow",
            "location": "Tverskaya Street, Moscow, Russia",
        },
    },
    "4": {
        "summary": "Новый городской отель",
        "value": {"title": "City Lights Hotel", "location": "Berlin, Germany"},
    },
    "5": {
        "summary": "Новый курортный объект",
        "value": {"title": "Laguna Bay Resort", "location": "Phuket, Thailand"},
    },
}


@router.post(
    "",
    summary="Создание отеля",
    description="Создаёт отель и возвращает созданную сущность.",
    response_description="Статус и данные созданного отеля.",
)
async def create_hotel(hotel_in: HotelCreate = Body(openapi_examples=HOTEL_EXAMPLES)):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).create(hotel_in)
        await session.commit()
        return {"status": "OK", "created_hotel": hotel}


@router.get(
    "",
    summary="Список отелей",
    description="Возвращает список отелей с фильтрацией по title/location (подстрока, без учёта регистра) и пагинацией.",
    response_description="Список отелей, удовлетворяющих фильтрам.",
)
async def read_hotels(pagination: PaginationDep, hotel_in: HotelFilter = Depends()):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).list_hotels(
            location=hotel_in.location,
            title=hotel_in.title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )


@router.get(
    "/{hotel_id}",
    summary="Просмотр отеля",
    description="Возвращает отель по его идентификатору hotel_id.",
    response_description="Данные отеля или null, если отель не найден.",
)
async def read_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).read_one_or_none(id=hotel_id)


@router.put(
    "/{hotel_id}",
    summary="Полная замена отеля",
    description="Полностью заменяет изменяемые поля отеля по идентификатору.",
    response_description="Подтверждение успешного полного обновления.",
)
async def replace_hotel(
    hotel_id: int, hotel_in: HotelCreate = Body(openapi_examples=HOTEL_EXAMPLES)
):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_in, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление отеля",
    description="Обновляет только переданные поля отеля по идентификатору.",
    response_description="Подтверждение успешного частичного обновления.",
)
async def patch_hotel(
    hotel_id: int, hotel_in: HotelFilter = Body(openapi_examples=HOTEL_PATCH_EXAMPLES)
):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_in, is_patch=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля",
    description="Удаляет отель по идентификатору.",
    response_description="Подтверждение успешного удаления отеля.",
)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}
