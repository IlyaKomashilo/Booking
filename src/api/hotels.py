from fastapi import Body, APIRouter, Depends

from src.repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelFilter, HotelCreate
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.post(
    "",
    summary="Создание отеля",
    description="Создаёт отель и возвращает созданную сущность.",
)
async def create_hotel(
    hotel_in: HotelCreate = Body(
        openapi_examples={
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
    )
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).create(hotel_in)
        await session.commit()
        return {"status": "OK", "created_hotel": hotel}


@router.get(
    "",
    summary="Список отелей",
    description="Возвращает список отелей с фильтрацией по title/location (подстрока, без учёта регистра) и пагинацией.",
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
    "/{hotel_id}", summary="Просмотр отеля", description="Возвращает отель по его ID"
)
async def read_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).read_one_or_none(id=hotel_id)


@router.put(
    "/{hotel_id}",
    summary="Полное обновление отеля",
    description="Полностью заменяет изменяемые поля отеля по идентификатору.",
)
async def update_hotel_all_params(hotel_id: int, hotel_in: HotelCreate):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_in, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление отеля",
    description="Обновляет только переданные поля отеля по идентификатору.",
)
async def update_hotel_any_params(hotel_id: int, hotel_in: HotelFilter):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(hotel_in, is_patch=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.delete(
    "/{hotel_id}",
    summary="Удаление отеля",
    description="Удаляет отель по идентификатору.",
)
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}
