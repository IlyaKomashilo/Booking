from pydantic import BaseModel, Field


class FacilityAdd(BaseModel):
    """Схема для создания/обновления удобства."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Название удобства (например, Wi‑Fi, бассейн, парковка).",
        examples=["Wi-Fi"],
    )


class Facility(FacilityAdd):
    """Схема удобства, возвращаемая в API."""

    id: int = Field(description="Уникальный идентификатор удобства.")
