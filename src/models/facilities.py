from sqlalchemy import String, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database import Base


class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities"
    )

    __table_args__ = (
        CheckConstraint("btrim(title) <> ''", name="ck_facilities_title_not_empty"),
        UniqueConstraint("title", name="uq_facilities_title"),
    )



class RoomsFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"),nullable=False, index=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id", ondelete="CASCADE"),nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint(
            "room_id",
            "facility_id",
            name="uq_rooms_facilities_room_id_facility_id",
        ),
    )