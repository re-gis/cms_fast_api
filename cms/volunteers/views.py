from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from cms.config import get_db
from cms.volunteers import services
from cms.volunteers.schemas import VolunteerParticipationCreate, VolunteerParticipationResponse, VolunteersResponse
from cms.auth.models import CustomUser
from cms.middlewares.middlewares import admin_required, get_current_user
from cms.auth.schemas import ErrorResponse

router = APIRouter()

@router.get("/participations/all", response_model=VolunteersResponse)
def get_all_participations(current_user: CustomUser = Depends(get_current_user), _: CustomUser = Depends(admin_required), db: Session = Depends(get_db)):
    try:
        participations = services.get_all_participations(db)
        if isinstance(participations, ErrorResponse):
            raise HTTPException(status_code=400, detail=participations.error)

        participations_response = [VolunteerParticipationResponse.from_orm(participation) for participation in participations]
        return VolunteersResponse(participations=participations_response)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
