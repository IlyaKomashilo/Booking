from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomWithRels


class RoomsRepository(BaseRepository):
    """Репозиторий для работы с категориями номеров."""

    model = RoomsOrm
    schema = Room

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
        return[RoomWithRels.model_validate(model, from_attributes=True) for model in result.scalars().all()]


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
        return RoomWithRels.model_validate(model, from_attributes=True)