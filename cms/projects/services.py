from sqlalchemy.orm import Session
from cms.projects.schemas import ProjectCreate, ProjectUpdate, AssignProjectToVolunteer, VolunteerParticipationResponse
from cms.projects.models import Project
from cms.auth.models import CustomUser
from cms.volunteers.models import VolunteerParticipation
from fastapi import HTTPException, status, Request


def create_project(project: ProjectCreate, db: Session, request: Request, current_user):
    db_project = db.query(Project).filter(Project.title == project.title).first()

    if db_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Product already exists."
        )

    db_project = Project(
        title=project.title,
        description=project.description,
        start_date=project.start_date,
        end_date=project.end_date,
        creator_id=current_user.id,
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project



def get_all_projects(db: Session):
    projects = db.query(Project).all()
    
    return projects



def get_project_by_id(project_id: int, db: Session):
    return db.query(Project).filter(Project.id == project_id).first()


def update_project(project_id: int, project_update: ProjectUpdate, db: Session):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        return None
    for key, value in project_update.dict(exclude_unset=True).items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project


def delete_project(project_id: int, db: Session):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        db.delete(project)
        db.commit()
        return True
    return False



def assign_volunteer_to_project(project_id: int, assign_project_to_volunteer: AssignProjectToVolunteer, db: Session):
    volunteer = db.query(CustomUser).filter(CustomUser.id == assign_project_to_volunteer.volunteer_id).first()
    if not volunteer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Volunteer not found."
        )

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found."
        )

    existing_participation = (
        db.query(VolunteerParticipation)
        .filter(VolunteerParticipation.volunteer_id == assign_project_to_volunteer.volunteer_id, VolunteerParticipation.project_id == project_id)
        .first()
    )
    if existing_participation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Project already assigned to the volunteer."
        )

    volunteer_participation = VolunteerParticipation(
        volunteer_id=assign_project_to_volunteer.volunteer_id,
        project_id=project_id,
        hours_contributed=assign_project_to_volunteer.hours_contributed
    )
    db.add(volunteer_participation)
    db.commit()
    db.refresh(volunteer_participation)

    return VolunteerParticipationResponse(
        volunteer_id=volunteer_participation.volunteer_id,
        project_id=volunteer_participation.project_id,
        hours_contributed=volunteer_participation.hours_contributed
    )

