from pydantic import BaseModel, Field, condecimal


class RoomCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    price: condecimal(max_digits=10, decimal_places=2, ge=0)
    quantity: int = Field(..., ge=0)


class RoomCreate(RoomCreateRequest):
    hotel_id: int


class Room(RoomCreate):
    id: int

class RoomFilterRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    price: condecimal(max_digits=10, decimal_places=2, ge=0) | None = None
    quantity: int | None = Field(default=None, ge=0)

class RoomFilter(RoomFilterRequest):
    hotel_id: int | None = None