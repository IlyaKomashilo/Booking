"""add_facilities

Revision ID: 00f197b2e594
Revises: 3450726e7db7
Create Date: 2026-03-05 15:21:55.312595

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "00f197b2e594"
down_revision: Union[str, Sequence[str], None] = "3450726e7db7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "facilities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.CheckConstraint("btrim(title) <> ''", name="ck_facilities_title_not_empty"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title", name="uq_facilities_title"),
    )
    op.create_table(
        "rooms_facilities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("room_id", sa.BigInteger(), nullable=False),
        sa.Column("facility_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["facility_id"], ["facilities.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "room_id", "facility_id", name="uq_rooms_facilities_room_id_facility_id"
        ),
    )
    op.create_index(
        op.f("ix_rooms_facilities_facility_id"),
        "rooms_facilities",
        ["facility_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_rooms_facilities_room_id"),
        "rooms_facilities",
        ["room_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_rooms_facilities_room_id"), table_name="rooms_facilities")
    op.drop_index(
        op.f("ix_rooms_facilities_facility_id"), table_name="rooms_facilities"
    )
    op.drop_table("rooms_facilities")
    op.drop_table("facilities")
