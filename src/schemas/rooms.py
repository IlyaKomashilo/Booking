from pydantic import BaseModel, Field, condecimal


class RoomCreateRequest(BaseModel):
    """Схема запроса для создания категории номера."""

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
    facilities_ids: list[int] = Field(
        default_factory=list,
        description="Идентификаторы удобств, которые нужно привязать к категории.",
    )


class RoomCreate(BaseModel):
    """Внутренняя схема создания категории номера в БД."""

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
    hotel_id: int = Field(
        description="Идентификатор отеля, к которому относится номер."
    )


class Room(RoomCreate):
    """Схема категории номера, возвращаемая в API."""

    id: int = Field(description="Уникальный идентификатор категории номера.")


class RoomFilterRequest(BaseModel):
    """Схема частичного обновления категории номера."""

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
    facilities_ids: list[int] | None = Field(
        default=None,
        description="Новый список идентификаторов удобств. При передаче заменяет текущие связи.",
    )


class RoomFilter(RoomFilterRequest):
    """Внутренняя схема фильтра/патча с контекстом отеля."""

    hotel_id: int | None = Field(
        default=None,
        description="Идентификатор отеля для контекста обновления/фильтрации.",
    )
