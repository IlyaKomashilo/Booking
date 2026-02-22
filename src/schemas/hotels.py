from pydantic import BaseModel, Field


class HotelCreate(BaseModel):
    title: str = Field(description="Название отеля.")
    location: str = Field(description="Адрес или город расположения отеля.")


class Hotel(HotelCreate):
    id: int = Field(description="Уникальный идентификатор отеля.")


class HotelFilter(BaseModel):
    title: str | None = Field(
        default=None,
        description="Фильтр по названию отеля (подстрока, без учёта регистра).",
    )
    location: str | None = Field(
        default=None,
        description="Фильтр по локации отеля (подстрока, без учёта регистра).",
    )
