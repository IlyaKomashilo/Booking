from fastapi import Depends, Query, Request, HTTPException
from pydantic import BaseModel
from typing import Annotated

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1, description="Номер страницы")]
    per_page: Annotated[
        int | None,
        Query(default=None, ge=1, le=25, description="Количество на странице"),
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def read_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Не предоставлен токен доступа")
    return token


def read_current_user(token: str = Depends(read_token)) -> int:
    data = AuthService().decode_token(token)
    return int(data["user_id"])


UseridDep = Annotated[int, Depends(read_current_user)]