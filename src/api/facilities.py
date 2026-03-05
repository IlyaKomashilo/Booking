from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd, Facility

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.post(
    "",
    summary="",
    description="",
    response_description="",
)
async def create_facility(
        db: DBDep,
        facility_in: FacilityAdd,
):
    facility = await db.facilities.create(facility_in)
    await db.commit()
    return {"status": "OK", "created_facility": facility}


@router.get(
    "",
    summary="",
    description="",
    response_description="",
)
async def read_facilities(
        db: DBDep,
):
    return await db.facilities.read_all()


@router.put(
    "",
    summary="",
    description="",
    response_description="",
)
async def replace_facility(
        facility_id: int,
        db: DBDep,
        facility_in: FacilityAdd,
):
    facility_data = Facility(id=facility_id, **facility_in.model_dump(exclude_unset=True))
    await db.facilities.update(facility_data, id=facility_id)
    await db.commit()
    return {"status": "OK"}


@router.delete(
    "",
    summary="",
    description="",
    response_description="",
)
async def delete_facility(
        db: DBDep,
        facility_id: int,
):
    await db.facilities.delete(id=facility_id)
    await db.commit()
    return {"status": "OK"}