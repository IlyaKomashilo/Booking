from pydantic import BaseModel, Field, condecimal
from datetime import date


class BookingCreateRequest(BaseModel):
    room_id: int = Field(description="")
    date_from: date = Field(description="")
    date_to: date = Field(description="")


class BookingCreate(BookingCreateRequest):
    user_id: int = Field(description="")
    price: condecimal(max_digits=10, decimal_places=2, ge=0) = Field(description="")


class Booking(BookingCreate):
    id: int = Field(description="")