"""add users

Revision ID: 5a55eae384af
Revises: 3d3721ad4bdc
Create Date: 2026-02-08 14:41:59.238299

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5a55eae384af"
down_revision: Union[str, Sequence[str], None] = "3d3721ad4bdc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("hash_password", sa.String(length=256), nullable=False),
        sa.Column("firstname", sa.String(length=50), nullable=True),
        sa.Column("lastname", sa.String(length=50), nullable=True),
        sa.Column("nickname", sa.String(length=32), nullable=True),
        sa.CheckConstraint(
            "(firstname IS NULL) OR (firstname <> '')",
            name="ck_users_firstname_not_empty",
        ),
        sa.CheckConstraint(
            "(lastname IS NULL) OR (lastname <> '')", name="ck_users_lastname_not_empty"
        ),
        sa.CheckConstraint(
            "(nickname IS NULL) OR (nickname <> '')", name="ck_users_nickname_not_empty"
        ),
        sa.CheckConstraint("email <> ''", name="ck_users_email_not_empty"),
        sa.CheckConstraint(
            "hash_password <> ''", name="ck_users_hash_password_not_empty"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("nickname", name="uq_users_nickname"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    op.create_index("ix_users_nickname", "users", ["nickname"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_users_nickname", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
