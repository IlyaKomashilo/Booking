from src.models.facilities import FacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility


class FacilitiesRepository(BaseRepository):
    """Репозиторий для работы с удобствами."""

    model = FacilitiesOrm
    schema = Facility
