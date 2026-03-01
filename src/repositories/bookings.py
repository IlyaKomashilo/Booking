from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.schemas.bookings import Booking


class BookingRepository(BaseRepository):
    """Репозиторий для работы с бронированиями."""

    model = BookingsOrm
    schema = Booking
