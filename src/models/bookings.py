from datetime import date
from decimal import Decimal
from sqlalchemy import BigInteger, CheckConstraint, Date, ForeignKey, Index, Numeric
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class BookingsOrm(Base):
    """ORM-модель бронирований."""

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    room_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("rooms.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date_from: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    date_to: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    @hybrid_property
    def total_price(self) -> Decimal:
        return self.price * (self.date_to - self.date_from).days

    __table_args__ = (
        CheckConstraint("date_to > date_from", name="ck_bookings_date_range"),
        CheckConstraint("price >= 0", name="ck_bookings_price_non_negative"),
        Index("ix_bookings_room_dates", room_id, date_from, date_to),
    )
