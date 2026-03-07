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
    """ """

    room_id: int = Field(description="")
    facility_id: int = Field(description="")


class RoomFacility(RoomFacilityCreate):
    """ """

    id: int = Field(description="")