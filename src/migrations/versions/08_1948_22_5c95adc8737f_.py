"""empty message

Revision ID: 5c95adc8737f
Revises: 43bdac23de69
Create Date: 2026-02-08 19:48:22.331582

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "5c95adc8737f"
down_revision: Union[str, Sequence[str], None] = "43bdac23de69"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "hash_password",
        existing_type=sa.VARCHAR(length=254),
        type_=sa.Text(),
        existing_nullable=False,
    )
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:

    op.drop_constraint(None, "users", type_="unique")
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.alter_column(
        "users",
        "hash_password",
        existing_type=sa.Text(),
        type_=sa.VARCHAR(length=254),
        existing_nullable=False,
    )

