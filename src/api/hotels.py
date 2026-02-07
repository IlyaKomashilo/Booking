from fastapi import Body, APIRouter, Depends

from repositories.hotels import HotelsRepository
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelFilter, HotelCreate
from src.database import async_session_maker

router = APIRouter(prefix='/hotels', tags=['Отели'])


@router.post('',
             summary='Добавление отеля',
             description='<h1>Добавляет отель с уникальным id и возвращает его</h1>'
             )
async def create_hotel(data_hotel: HotelCreate = Body(openapi_examples={
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
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).create(data_hotel)
        await session.commit()
        return {'status': 'OK', 'created_hotel': hotel}


@router.get('',
            summary='Просмотр отелей',
            description='<h1>Возвращает отели по query параметрам. Фильтрует методом "подстрок". + Пагинация </h1>'
            )
async def read_hotels(pagination: PaginationDep, data_hotel: HotelFilter = Depends()):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).read_all(
            location=data_hotel.location,
            title=data_hotel.title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.get('/{hotel_id}',
            summary='Просмотр отеля',
            description='<h1>Возвращает отель по его ID</h1>'
            )
async def read_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).read_one_or_none(id=hotel_id)


@router.put('/{hotel_id}',
            summary='Полное редактирование параметров отеля',
            description='<h1>Тут редактируются только все параметры</h1>'
            )
async def update_hotel_all_params(hotel_id: int, data_hotel: HotelCreate):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(data_hotel, id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.patch('/{hotel_id}',
              summary='Частичное редактирование любых параметров отеля',
              description='<h1>Тут редактируются любые параметры отеля</h1>'
              )
async def update_hotel_any_params(hotel_id: int, data_hotel: HotelFilter):
    async with async_session_maker() as session:
        await HotelsRepository(session).update(data_hotel, is_patch=True, id=hotel_id)
        await session.commit()
    return {'status': 'OK'}



@router.delete('/{hotel_id}',
               summary='Удаление отеля',
               description='<h1>Удаление отеля по его ID</h1>'
               )
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {'status': 'OK'}
