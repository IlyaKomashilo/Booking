from pydantic import BaseModel, EmailStr, Field


class UserRequestCreate(BaseModel):
    email: EmailStr = Field(description="Email пользователя для регистрации или входа.")
    password: str = Field(
        min_length=8, description="Пароль пользователя в открытом виде."
    )


class UserCreate(BaseModel):
    email: EmailStr = Field(description="Нормализованный email пользователя.")
    hash_password: str = Field(description="Хэш пароля пользователя.")


class User(BaseModel):
    id: int = Field(description="Уникальный идентификатор пользователя.")
    email: EmailStr = Field(description="Email пользователя.")


class UserWithHashPassword(User):
    hash_password: str = Field(description="Хэш пароля пользователя.")
