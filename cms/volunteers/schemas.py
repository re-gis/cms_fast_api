from pydantic import BaseModel
from typing import List
from cms.volunteers.models import VolunteerParticipation

class VolunteerParticipationCreate(BaseModel):
    project_id: int
    hours_contributed: float
    
    class Config:
        from_attributes = True

class VolunteerParticipationResponse(VolunteerParticipationCreate):
    id: int
    volunteer_id: int

    class Config:
        orm_mode = True
        
        
class VolunteersResponse(BaseModel):
    participations: List[VolunteerParticipationResponse]
