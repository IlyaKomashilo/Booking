"""edit_rooms

Revision ID: 4f67fb4f80a7
Revises: 645252531c8a
Create Date: 2026-02-18 11:50:13.691580

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "4f67fb4f80a7"
down_revision: Union[str, Sequence[str], None] = "645252531c8a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(op.f("rooms_hotel_id_fkey"), "rooms", type_="foreignkey")

    op.alter_column(
        "rooms",
        "id",
        existing_type=sa.INTEGER(),
        type_=sa.BigInteger(),
        existing_nullable=False,
        postgresql_using="id::bigint",
    )

    op.alter_column(
        "rooms",
        "hotel_id",
        existing_type=sa.INTEGER(),
        type_=sa.BigInteger(),
        existing_nullable=False,
        postgresql_using="hotel_id::bigint",
    )

    op.alter_column(
        "rooms",
        "description",
        existing_type=sa.VARCHAR(),
        type_=sa.Text(),
        nullable=True,
    )

    op.alter_column(
        "rooms",
        "price",
        existing_type=sa.INTEGER(),
        type_=sa.Numeric(precision=10, scale=2),
        existing_nullable=False,
        postgresql_using="price::numeric(10,2)",
    )

    op.create_index(op.f("ix_rooms_hotel_id"), "rooms", ["hotel_id"], unique=False)
    op.create_unique_constraint("uq_rooms_hotel_title", "rooms", ["hotel_id", "title"])

    op.create_foreign_key(
        "fk_rooms_hotel_id_hotels",
        "rooms",
        "hotels",
        ["hotel_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("fk_rooms_hotel_id_hotels", "rooms", type_="foreignkey")

    op.drop_constraint("uq_rooms_hotel_title", "rooms", type_="unique")
    op.drop_index(op.f("ix_rooms_hotel_id"), table_name="rooms")

    op.alter_column(
        "rooms",
        "price",
        existing_type=sa.Numeric(precision=10, scale=2),
        type_=sa.INTEGER(),
        existing_nullable=False,
        postgresql_using="price::integer",
    )

    op.alter_column(
        "rooms",
        "description",
        existing_type=sa.Text(),
        type_=sa.VARCHAR(),
        nullable=False,
    )

    op.alter_column(
        "rooms",
        "hotel_id",
        existing_type=sa.BigInteger(),
        type_=sa.INTEGER(),
        existing_nullable=False,
        postgresql_using="hotel_id::integer",
    )

    op.alter_column(
        "rooms",
        "id",
        existing_type=sa.BigInteger(),
        type_=sa.INTEGER(),
        existing_nullable=False,
        postgresql_using="id::integer",
    )

    op.create_foreign_key(
        op.f("rooms_hotel_id_fkey"),
        "rooms",
        "hotels",
        ["hotel_id"],
        ["id"],
    )
