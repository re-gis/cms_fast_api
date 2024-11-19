from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cms.config import get_db
from cms.volunteers import services
from cms.volunteers.schemas import VolunteerParticipationCreate, VolunteerParticipationResponse

router = APIRouter()

@router.post("/volunteers/participation", response_model=VolunteerParticipationResponse)
def add_volunteer_participation(participation: VolunteerParticipationCreate, db: Session = Depends(get_db)):
    return services.add_volunteer_participation(db, participation)
