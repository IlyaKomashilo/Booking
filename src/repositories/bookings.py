"""Репозиторий для работы с бронированиями."""

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    """Репозиторий для работы с бронированиями."""

    model = BookingsOrm
    mapper = BookingDataMapper
