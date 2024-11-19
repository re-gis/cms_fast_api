from pydantic import BaseModel

class VolunteerParticipationCreate(BaseModel):
    project_id: int
    hours_contributed: float

class VolunteerParticipationResponse(VolunteerParticipationCreate):
    id: int

    class Config:
        orm_mode = True
