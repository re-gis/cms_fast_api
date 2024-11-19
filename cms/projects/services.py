from sqlalchemy.orm import Session
from cms.projects.schemas import ProjectCreate
from cms.projects.models import Project
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
