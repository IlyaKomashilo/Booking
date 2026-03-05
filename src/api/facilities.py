from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

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
    return {"status": "OK", "created_facility": facility}