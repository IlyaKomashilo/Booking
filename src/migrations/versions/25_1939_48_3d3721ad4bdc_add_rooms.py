"""add rooms

Revision ID: 3d3721ad4bdc
Revises: 29b39cc53fdb
Create Date: 2026-01-25 19:39:48.548460

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "3d3721ad4bdc"
down_revision: Union[str, Sequence[str], None] = "29b39cc53fdb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms")
