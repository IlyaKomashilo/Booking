from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UseridDep
from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestCreate, UserCreate
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    description="Создаёт нового пользователя, хэширует пароль и сохраняет запись в БД. Возвращает статус выполнения.",
)
async def create_user(
    user_in: UserRequestCreate = Body(
        openapi_examples={
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
        }
    )
):
    normalized_email = user_in.email.lower()
    hash_password = AuthService().hash_password(user_in.password)
    user_to_create = UserCreate(email=normalized_email, hash_password=hash_password)
    async with async_session_maker() as session:
        await UsersRepository(session).create(user_to_create)
        await session.commit()

    return {"status": "OK"}


@router.post(
    "/login",
    summary="Вход пользователя",
    description="Проверяет email и пароль. При успехе возвращает JWT access token и устанавливает cookie access_token."
                " Ошибки: 401 при неверных учётных данных.",
)
async def login_user(
    response: Response,
    user_in: UserRequestCreate = Body(
        openapi_examples={
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
        }
    ),
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).read_user_with_hash_password(
            email=user_in.email.lower()
        )
        if not user:
            raise HTTPException(
                status_code=401, detail="Пользователь с таким email не зарегистрирован"
            )
        if not AuthService().verify_password(user_in.password, user.hash_password):
            raise HTTPException(status_code=401, detail="Пароль не верный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token}


@router.post(
    "/logout",
    summary="Выход пользователя",
    description="Удаляет cookie access_token"
)
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "OK"}


@router.get("/me")
async def read_me(
        user_id: UseridDep
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).read_one_or_none(id=user_id)
    return user