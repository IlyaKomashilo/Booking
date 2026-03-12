from pydantic import BaseModel, Field


class FacilityCreate(BaseModel):
    """Схема для создания/обновления удобства."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Название удобства (например, Wi‑Fi, бассейн, парковка).",
        examples=["Wi-Fi"],
    )


class Facility(FacilityCreate):
    """Схема удобства, возвращаемая в API."""

    id: int = Field(description="Уникальный идентификатор удобства.")


class RoomFacilityCreate(BaseModel):
    """Связь категории номера и удобства для записи в таблицу many-to-many."""

    room_id: int = Field(gt=0, description="Идентификатор категории номера.")
    facility_id: int = Field(gt=0, description="Идентификатор удобства.")


class RoomFacility(RoomFacilityCreate):
    """Связь категории номера и удобства, возвращаемая из БД."""

    id: int = Field(description="Уникальный идентификатор связи номер-удобство.")
