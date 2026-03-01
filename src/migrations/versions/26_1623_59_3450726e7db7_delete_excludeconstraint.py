"""delete ExcludeConstraint

Revision ID: 3450726e7db7
Revises: 2ef9a40d2f87
Create Date: 2026-02-26 16:23:59.065532

"""

from typing import Sequence, Union

from alembic import op

revision: str = "3450726e7db7"
down_revision: Union[str, Sequence[str], None] = "2ef9a40d2f87"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE bookings
        DROP CONSTRAINT IF EXISTS excl_bookings_room_no_overlap
    """)


def downgrade() -> None:
    op.execute("""
        CREATE EXTENSION IF NOT EXISTS btree_gist
    """)
    op.execute("""
        ALTER TABLE bookings
        ADD CONSTRAINT excl_bookings_room_no_overlap
        EXCLUDE USING gist (
            room_id WITH =,
            daterange(date_from, date_to, '[)') WITH &&
        )
    """)
