from pydantic import BaseModel, Field


class HotelCreate(BaseModel):
    title: str
    location: str


class Hotel(HotelCreate):
    id: int


class HotelFilter(BaseModel):
    title: str | None = Field(default=None, description="Название отеля")
    location: str | None = Field(default=None, description="Адрес отеля")
