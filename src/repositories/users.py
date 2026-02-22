from pydantic import EmailStr
from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User, UserWithHashPassword


class UsersRepository(BaseRepository):
    """Репозиторий для работы с пользователями."""

    model = UsersOrm
    schema = User

    async def read_user_with_hash_password(self, email: EmailStr):
        """Возвращает пользователя вместе с хэшем пароля по email."""
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return UserWithHashPassword.model_validate(model, from_attributes=True)
