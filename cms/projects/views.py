from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from cms.config import get_db
from cms.projects import services
from cms.projects.schemas import ProjectCreate, ProjectResponse
from cms.auth.schemas import ErrorResponse
from cms.middlewares.middlewares import get_current_user, admin_required
from cms.auth.models import CustomUser


router = APIRouter()


@router.post(
    "/create", response_model=ProjectResponse, response_model_exclude_unset=True
)
def create_project(
    project: ProjectCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: CustomUser = Depends(get_current_user),
    _: CustomUser = Depends(admin_required),
):
    try:
        result = services.create_project(project, db, request, current_user)

        if isinstance(result, ErrorResponse):
            raise HTTPException(status_code=400, detail=result.error)

        return result

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
