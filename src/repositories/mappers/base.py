"""Базовый интерфейс мапперов между ORM и Pydantic-схемами."""

from typing import TypeVar

from pydantic import BaseModel

from src.database import Base

DBModelType = TypeVar("DBModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    """Базовый mapper для конвертации данных между слоями."""

    db_model: type[DBModelType] | None = None
    schema: type[SchemaType] | None = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence(cls, data):
        return cls.db_model(**data.model_dump())
