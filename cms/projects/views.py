from fastapi import APIRouter, Depends, HTTPException, Request, Body
from sqlalchemy.orm import Session
from cms.config import get_db
from cms.projects import services
from cms.projects.schemas import (
    ProjectCreate,
    ProjectResponse,
    ProjectsResponse,
    ProjectUpdate,
    AssignResponse,
    AssignProjectToVolunteer,
    VolunteerParticipationResponse
)
from cms.auth.schemas import ErrorResponse
from cms.middlewares.middlewares import get_current_user, admin_required
from cms.auth.models import CustomUser
from typing import Optional


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


@router.get("/all", response_model=ProjectsResponse, response_model_exclude_unset=True)
def get_all_projects(db: Session = Depends(get_db)):
    try:
        projects = services.get_all_projects(db)
        if isinstance(projects, ErrorResponse):
            raise HTTPException(status_code=400, detail=projects.error)

        projects_response = [ProjectResponse.from_orm(project) for project in projects]
        return ProjectsResponse(projects=projects_response)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{project_id}", response_model=ProjectResponse, response_model_exclude_unset=True
)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = services.get_project_by_id(project_id, db)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse.model_validate(project)


@router.put(
    "/{project_id}", response_model=ProjectResponse, response_model_exclude_unset=True
)
def update_project(
    project_id: int,
    project_update: Optional[ProjectUpdate] = Body(default={}),
    db: Session = Depends(get_db),
    current_user: CustomUser = Depends(get_current_user),
    _: CustomUser = Depends(admin_required),
):
    project = services.update_project(project_id, project_update, db)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectResponse.model_validate(project)


@router.delete("/{project_id}", response_model=dict)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: CustomUser = Depends(get_current_user),
    _: CustomUser = Depends(admin_required),
):
    success = services.delete_project(project_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"detail": "Project deleted successfully"}


@router.post("/{project_id}/assign/volunteer", response_model=VolunteerParticipationResponse)
def assign_project_to_volunteer(
    project_id: int,
    dto: AssignProjectToVolunteer,
    db: Session = Depends(get_db),
    current_user: CustomUser = Depends(get_current_user),
    _: CustomUser = Depends(admin_required),
):
    result = services.assign_volunteer_to_project(project_id, dto, db)
    
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
