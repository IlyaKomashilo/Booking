from fastapi import APIRouter, Body

from passlib.context import CryptContext

from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestCreate, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register",
             summary="Регистрирует пользователя",
             description="<h1>Регистрирует пользователя и хэширует его пароль</h1>",)
async def create_user(data_user: UserRequestCreate = Body(openapi_examples={
    "1": {
        "summary": "User_1",
        "value": {
            "email": "atlantis.user1@example.com",
            "password": "M3rmaid!82",
        },
    },
    "2": {
        "summary": "User_2",
        "value": {
            "email": "burj.user2@example.com",
            "password": "Dune#47Sky",
        },
    },
    "3": {
        "summary": "User_3",
        "value": {
            "email": "ritz.user3@example.com",
            "password": "C0ffee@19",
        },
    },
    "4": {
        "summary": "User_4",
        "value": {
            "email": "arts.user4@example.com",
            "password": "N1ght$Jazz",
        },
    },
    "5": {
        "summary": "User_5",
        "value": {
            "email": "savoy.user5@example.com",
            "password": "T3aTime%58",
        },
    },
})):
    hash_password = pwd_context.hash(data_user.password)
    new_data_user = UserCreate(email=data_user.email, hash_password=hash_password)
    async with async_session_maker() as session:
        user = await UsersRepository(session).create(new_data_user)
        await session.commit()

    return {"status": "OK"}
