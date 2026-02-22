from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    """Репозиторий для работы с категориями номеров."""

    model = RoomsOrm
    schema = Room
