from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestCreate(BaseModel):
    email: EmailStr
    password: str
    lastname: str
    firstname: str
    nickname: str


class UserCreate(BaseModel):
    email: EmailStr
    hash_password: str
    lastname: str
    firstname: str
    nickname: str


class User(BaseModel):
    id: int
    email: EmailStr
    lastname: str
    firstname: str
    nickname: str

    model_config = ConfigDict(from_attributes=True)
