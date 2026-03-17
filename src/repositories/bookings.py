from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.schemas.bookings import Booking


class BookingsRepository(BaseRepository):
    """Репозиторий для работы с бронированиями."""

    model = BookingsOrm
    schema = BookingDataMapper
