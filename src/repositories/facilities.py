from sqlalchemy import delete, insert, select

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    """Репозиторий для работы с удобствами."""

    model = FacilitiesOrm
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    """Репозиторий для таблицы связей комнат и удобств."""

    model = RoomsFacilitiesOrm
    schema = RoomFacility

    async def set_room_facilities(
        self, room_id: int, facilities_ids: list[int]
    ) -> None:
        """Синхронизирует связи удобств для указанной категории номера."""

        read_current_facilities_ids_query = select(self.model.facility_id).filter_by(
            room_id=room_id
        )
        result = await self.session.execute(read_current_facilities_ids_query)
        current_facilities_ids = set(result.scalars().all())
        new_facilities_ids = set(facilities_ids)

        ids_to_delete = list(current_facilities_ids - new_facilities_ids)
        ids_to_insert = list(new_facilities_ids - current_facilities_ids)

        if ids_to_delete:
            delete_m2m_facilities_stmt = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.facility_id.in_(ids_to_delete),
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if ids_to_insert:
            insert_m2m_facilities_stmt = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert]
            )
            await self.session.execute(insert_m2m_facilities_stmt)
