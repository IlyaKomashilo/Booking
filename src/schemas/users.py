from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestCreate(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    hash_password: str


class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
