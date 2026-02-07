from fastapi import Depends, Query
from pydantic import BaseModel
from typing import Annotated

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default=1, ge=1, description='Page number')]
    per_page: Annotated[int | None, Query(default=None, ge=1, le=25, description='How many hotels in page')]

PaginationDep = Annotated[PaginationParams, Depends()]