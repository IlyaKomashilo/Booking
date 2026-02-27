from pydantic import BaseModel, Field, condecimal
from datetime import date


class BookingCreateRequest(BaseModel):
    date_from: date = Field(description="")
    date_to: date = Field(description="")


class BookingCreate(BookingCreateRequest):
    room_id: str = Field(description="")
    user_id: str = Field(description="")
    price: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(description="")


class Booking(BookingCreate):
    id: int = Field(description="")