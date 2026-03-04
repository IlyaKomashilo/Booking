from datetime import date

from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room


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
        return await self.read_filtered(RoomsOrm.id.in_(rooms_ids_to_get))