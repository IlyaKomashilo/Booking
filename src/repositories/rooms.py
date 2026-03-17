"""Репозиторий для работы с категориями номеров."""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import RoomDataMapper, RoomDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    """Репозиторий для работы с категориями номеров."""

    model = RoomsOrm
    mapper = RoomDataMapper

    async def read_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)

        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.scalars().all()
        ]

    async def is_room_available(
        self, room_id: int, date_from: date, date_to: date
    ) -> bool:
        """Проверяет, доступна ли категория номера на заданный период."""

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        query = select(self.model.id).filter(
            self.model.id == room_id,
            self.model.id.in_(rooms_ids_to_get),
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def read_one_or_none_with_rels(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return RoomDataWithRelsMapper.map_to_domain_entity(model)
