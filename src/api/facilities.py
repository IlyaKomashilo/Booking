from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import Facility, FacilityCreate

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.post(
    "",
    summary="Создание удобства",
    description="Создаёт новое удобство и возвращает созданную запись.",
    response_description="Статус операции и данные созданного удобства.",
)
async def create_facility(
    db: DBDep,
    facility_in: FacilityCreate,
):
    facility = await db.facilities.create(facility_in)
    await db.commit()
    return {"status": "OK", "created_facility": facility}


@router.get(
    "",
    summary="Список удобств",
    description="Возвращает список всех доступных удобств.",
    response_description="Список удобств.",
)
async def read_facilities(
    db: DBDep,
):
    return await db.facilities.read_all()


@router.put(
    "",
    summary="Полная замена удобства",
    description="Полностью обновляет удобство по facility_id.",
    response_description="Подтверждение успешного обновления.",
)
async def replace_facility(
    facility_id: int,
    db: DBDep,
    facility_in: FacilityCreate,
):
    facility_data = Facility(
        id=facility_id, **facility_in.model_dump(exclude_unset=True)
    )
    await db.facilities.update(facility_data, id=facility_id)
    await db.commit()
    return {"status": "OK"}


@router.delete(
    "",
    summary="Удаление удобства",
    description="Удаляет удобство по facility_id.",
    response_description="Подтверждение успешного удаления.",
)
async def delete_facility(
    db: DBDep,
    facility_id: int,
):
    await db.facilities.delete(id=facility_id)
    await db.commit()
    return {"status": "OK"}
