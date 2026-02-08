"""v

Revision ID: 645252531c8a
Revises: 5c95adc8737f
Create Date: 2026-02-08 20:01:09.599823

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "645252531c8a"
down_revision: Union[str, Sequence[str], None] = "5c95adc8737f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(op.f("users_email_key"), "users", type_="unique")
    op.create_index(
        "uq_users_email_ci", "users", [sa.literal_column("lower(email)")], unique=True
    )
    op.execute("UPDATE users SET email = lower(email) WHERE email <> lower(email);")
    op.create_check_constraint("ck_users_email_is_lower", "users", "email = lower(email)")

def downgrade() -> None:
    op.drop_index("uq_users_email_ci", table_name="users")
    op.create_unique_constraint(
        op.f("users_email_key"), "users", ["email"], postgresql_nulls_not_distinct=False
    )

