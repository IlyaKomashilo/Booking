from datetime import date

from pydantic import BaseModel, ConfigDict, Field, condecimal, model_validator


class BookingCreateRequest(BaseModel):
    """Тело запроса на создание бронирования."""

    model_config = ConfigDict(extra="forbid")

    room_id: int = Field(
        gt=0,
        description="Идентификатор категории номера (положительное целое число).",
    )
    date_from: date = Field(description="Дата заезда.")
    date_to: date = Field(description="Дата выезда (должна быть позже даты заезда).")

    @model_validator(mode="after")
    def validate_date_range(self) -> "BookingCreateRequest":
        """Проверяет, что дата выезда строго позже даты заезда."""

        if self.date_to <= self.date_from:
            raise ValueError("Дата выезда должна быть позже даты заезда")
        return self


class BookingCreate(BookingCreateRequest):
    """Внутренняя схема для создания бронирования в БД."""

    user_id: int = Field(
        description="Идентификатор пользователя, который создаёт бронь."
    )
    price: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(
        description="Стоимость одной ночи на момент бронирования."
    )


class Booking(BookingCreate):
    """Схема бронирования, возвращаемая в API."""

    id: int = Field(description="Уникальный идентификатор бронирования.")
