from pydantic import BaseModel
from sqlalchemy import delete, insert, select, update


class BaseRepository:
    """Базовый репозиторий с типовыми CRUD-операциями."""

    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def create(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model).values(**data.model_dump()).returning(self.model)
        )
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model, from_attributes=True)

    async def read_filtered(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [
            self.schema.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]

    async def read_all(self, *args, **kwargs):
        return await self.read_filtered()

    async def read_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model, from_attributes=True)

    async def update(
        self, data: BaseModel, is_patch: bool = False, **filter_by
    ) -> None:
        edit_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=is_patch))
        )
        await self.session.execute(edit_data_stmt)

    async def delete(self, **filter_by) -> None:
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_data_stmt)
