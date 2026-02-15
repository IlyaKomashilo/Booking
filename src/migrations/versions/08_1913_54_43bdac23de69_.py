"""empty message

Revision ID: 43bdac23de69
Revises: 5a55eae384af
Create Date: 2026-02-08 19:13:54.004172

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "43bdac23de69"
down_revision: Union[str, Sequence[str], None] = "5a55eae384af"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "hash_password",
        existing_type=sa.VARCHAR(length=256),
        type_=sa.String(length=254),
        existing_nullable=False,
    )
    op.drop_index(op.f("ix_users_nickname"), table_name="users")
    op.drop_constraint(op.f("uq_users_email"), "users", type_="unique")
    op.drop_constraint(op.f("uq_users_nickname"), "users", type_="unique")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.drop_column("users", "firstname")
    op.drop_column("users", "lastname")
    op.drop_column("users", "nickname")
    # ### end Alembic commands ###


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "nickname", sa.VARCHAR(length=32), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "lastname", sa.VARCHAR(length=50), autoincrement=False, nullable=True
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "firstname", sa.VARCHAR(length=50), autoincrement=False, nullable=True
        ),
    )
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
    op.create_unique_constraint(
        op.f("uq_users_nickname"),
        "users",
        ["nickname"],
        postgresql_nulls_not_distinct=False,
    )
    op.create_unique_constraint(
        op.f("uq_users_email"), "users", ["email"], postgresql_nulls_not_distinct=False
    )
    op.create_index(op.f("ix_users_nickname"), "users", ["nickname"], unique=False)
    op.alter_column(
        "users",
        "hash_password",
        existing_type=sa.String(length=254),
        type_=sa.VARCHAR(length=256),
        existing_nullable=False,
    )
