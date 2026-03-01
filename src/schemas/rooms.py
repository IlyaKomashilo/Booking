from pydantic import BaseModel, Field, condecimal


class RoomCreateRequest(BaseModel):
    title: str = Field(
        ..., min_length=1, max_length=100, description="Название категории номера."
    )
    description: str | None = Field(
        default=None, max_length=1000, description="Описание категории номера."
    )
    price: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(
        description="Стоимость за ночь в формате decimal."
    )
    quantity: int = Field(..., ge=0, description="Количество номеров данной категории.")


class RoomCreate(RoomCreateRequest):
    hotel_id: int = Field(
        description="Идентификатор отеля, к которому относится номер."
    )


class Room(RoomCreate):
    id: int = Field(description="Уникальный идентификатор категории номера.")


class RoomFilterRequest(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Новое название категории номера.",
    )
    description: str | None = Field(
        default=None,
        min_length=1,
        max_length=1000,
        description="Новое описание категории номера.",
    )
    price: condecimal(max_digits=10, decimal_places=2, ge=0) | None = Field(
        default=None,
        description="Новая стоимость за ночь.",
    )
    quantity: int | None = Field(
        default=None, ge=0, description="Новое количество номеров категории."
    )


class RoomFilter(RoomFilterRequest):
    hotel_id: int | None = Field(
        default=None,
        description="Идентификатор отеля для контекста обновления/фильтрации.",
    )
