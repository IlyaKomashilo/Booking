from sqlalchemy import String, BigInteger, CheckConstraint, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class UsersOrm(Base):
    __tablename__ = "users"

    __table_args__ = (
        UniqueConstraint("email", name="uq_users_email"),
        UniqueConstraint("nickname", name="uq_users_nickname"),
        CheckConstraint("email <> ''", name="ck_users_email_not_empty"),
        CheckConstraint("hash_password <> ''", name="ck_users_hash_password_not_empty"),
        CheckConstraint("(firstname IS NULL) OR (firstname <> '')", name="ck_users_firstname_not_empty"),
        CheckConstraint("(lastname IS NULL) OR (lastname <> '')", name="ck_users_lastname_not_empty"),
        CheckConstraint("(nickname IS NULL) OR (nickname <> '')", name="ck_users_nickname_not_empty"),
        Index("ix_users_email", "email"),
        Index("ix_users_nickname", "nickname"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False)
    hash_password: Mapped[str] = mapped_column(String(255), nullable=False)
    firstname: Mapped[str | None] = mapped_column(String(50), nullable=True)
    lastname: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nickname: Mapped[str | None] = mapped_column(String(32), nullable=True)
