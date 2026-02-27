"""add bookings

Revision ID: 2ef9a40d2f87
Revises: 4f67fb4f80a7
Create Date: 2026-02-25 11:21:33.242999

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "2ef9a40d2f87"
down_revision: Union[str, Sequence[str], None] = "4f67fb4f80a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")
    op.create_table(
        "bookings",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("room_id", sa.BigInteger(), nullable=False),
        sa.Column("date_from", sa.Date(), nullable=False),
        sa.Column("date_to", sa.Date(), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        postgresql.ExcludeConstraint(
            (sa.column("room_id"), "="),
            (sa.text("daterange(date_from, date_to, '[)')"), "&&"),
            using="gist",
            name="excl_bookings_room_no_overlap",
        ),
        sa.CheckConstraint("date_to > date_from", name="ck_bookings_date_range"),
        sa.CheckConstraint("price >= 0", name="ck_bookings_price_non_negative"),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_bookings_date_from"), "bookings", ["date_from"], unique=False
    )
    op.create_index(op.f("ix_bookings_date_to"), "bookings", ["date_to"], unique=False)
    op.create_index(
        "ix_bookings_room_dates",
        "bookings",
        ["room_id", "date_from", "date_to"],
        unique=False,
    )
    op.create_index(op.f("ix_bookings_room_id"), "bookings", ["room_id"], unique=False)
    op.create_index(op.f("ix_bookings_user_id"), "bookings", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_bookings_user_id"), table_name="bookings")
    op.drop_index(op.f("ix_bookings_room_id"), table_name="bookings")
    op.drop_index("ix_bookings_room_dates", table_name="bookings")
    op.drop_index(op.f("ix_bookings_date_to"), table_name="bookings")
    op.drop_index(op.f("ix_bookings_date_from"), table_name="bookings")
    op.drop_table("bookings")
