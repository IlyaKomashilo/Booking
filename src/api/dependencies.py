from typing import Annotated

from fastapi import Depends, HTTPException, Query, Request
from pydantic import BaseModel

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    """Параметры пагинации для листинговых endpoint-ов."""

    page: Annotated[int | None, Query(default=1, ge=1, description="Номер страницы")]
    per_page: Annotated[
        int | None,
        Query(default=None, ge=1, le=25, description="Количество на странице"),
    ]


PaginationDep = Annotated[PaginationParams, Depends()]


def read_token(request: Request) -> str:
    """Извлекает JWT access token из cookie запроса."""

    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Не предоставлен токен доступа")
    return token


def read_current_user(token: str = Depends(read_token)) -> int:
    """Декодирует токен и возвращает идентификатор текущего пользователя."""

    data = AuthService().decode_token(token)
    return int(data["user_id"])


UserIdDep = Annotated[int, Depends(read_current_user)]
