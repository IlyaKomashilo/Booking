from pydantic import BaseModel, EmailStr


class UserRequestCreate(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    hash_password: str


class User(BaseModel):
    id: int
    email: EmailStr


class UserWithHashPassword(User):
    hash_password: str
