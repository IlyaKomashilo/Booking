from fastapi import APIRouter, Body, HTTPException, Response

from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestCreate, UserCreate
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register",
             summary="Регистрирование пользователя",
             description="<h1>Регестрирует пользователя и хэширует пароль</h1>")
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
    hash_password = AuthService().hash_password(data_user.password)
    new_data_user = UserCreate(email=data_user.email, hash_password=hash_password)
    async with async_session_maker() as session:
        await UsersRepository(session).create(new_data_user)
        await session.commit()

    return {"status": "OK"}


@router.post("/login",
             summary="log in пользователя",
             description="""
                          <h3>Аутентификация пользователя</h3>
                          <p>Проверяет <b>email</b> и <b>password</b>. При успешной проверке возвращает <b>JWT access token</b>.</p>
                          <ul>
                            <li><b>200</b> — токен выдан</li>
                            <li><b>401</b> — неверные учётные данные или пользователь не найден</li>
                          </ul>
                          """,)
async def login_user(
        response: Response,
        data_user: UserRequestCreate = Body(openapi_examples={

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
})
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).read_user_with_hash_password(email=data_user.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService.verify_password(data_user.password, user.hash_password):
            raise HTTPException(status_code=401, detail="Пароль не верный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token}