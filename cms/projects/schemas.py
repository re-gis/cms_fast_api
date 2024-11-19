from pydantic import BaseModel
from typing import Optional
from datetime import datetime



class ProjectBase(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int

    class Config:
        orm_mode = True
