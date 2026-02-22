from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    BigInteger, Integer, String, Text, ForeignKey,
    CheckConstraint, UniqueConstraint, Numeric
)

from src.database import Base


class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    hotel_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("hotels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")


    __table_args__ = (
        UniqueConstraint("hotel_id", "title", name="uq_rooms_hotel_title"),
        CheckConstraint("title <> ''", name="ck_rooms_title_not_empty"),
        CheckConstraint("price >= 0", name="ck_rooms_price_non_negative"),
        CheckConstraint("quantity >= 0", name="ck_rooms_quantity_non_negative"),
    )