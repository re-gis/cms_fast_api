from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List


class ProjectBase(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int

    class Config:
        from_attributes = True


class ProjectsResponse(BaseModel):
    projects: List[ProjectResponse]


class ProjectUpdate(ProjectBase):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class AssignProjectToVolunteer(BaseModel):
    volunteer_id: int
    hours_contributed: float

    class Config:
        from_attributes = True


class AssignResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True


class VolunteerParticipationResponse(BaseModel):
    volunteer_id: int
    project_id: int
    hours_contributed: float

    class Config:
        orm_mode = True 