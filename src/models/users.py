from sqlalchemy import String, CheckConstraint, Text, BigInteger, Index, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    hash_password: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        CheckConstraint("email <> ''", name="ck_users_email_not_empty"),
        CheckConstraint("email = lower(email)", name="ck_users_email_is_lower"),
        CheckConstraint("hash_password <> ''", name="ck_users_hash_not_empty"),
        Index("uq_users_email_ci", func.lower(email), unique=True),
    )
