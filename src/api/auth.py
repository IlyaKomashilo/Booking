from fastapi import APIRouter

from passlib.context import CryptContext

from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestCreate, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register",
             summary="Регистрирует пользователя",
             description="<h1>Регистрирует пользователя и хэширует его пароль</h1>",)
async def create_user(data_user: UserRequestCreate):
    hash_password = pwd_context.hash(data_user.password)
    new_data_user = UserCreate(email=data_user.email,
                               hash_password=hash_password,
                               nickname=data_user.nickname,
                               lastname=data_user.lastname,
                               firstname=data_user.firstname,)
    async with async_session_maker as session:
        user = await UsersRepository(session).create(new_data_user)
        await session.commit()

    return {"status": "OK", "data": user}