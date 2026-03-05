from pydantic import BaseModel, Field


class FacilityAdd(BaseModel):
    """" """
    title: str = Field(..., min_length=1, max_length=100, description="")


class Facility(FacilityAdd):
    """ """
    id: int = Field(description="")