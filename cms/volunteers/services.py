from cms.volunteers.models import VolunteerParticipation
from sqlalchemy.orm import Session


def get_all_participations(db: Session):
    db_participation = db.query(VolunteerParticipation).all()

    return db_participation
