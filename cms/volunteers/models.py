from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
from cms.config import Base



class VolunteerParticipation(Base):
    __tablename__ = "volunteer_participation"

    id = Column(Integer, primary_key=True, index=True)
    volunteer_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))
    hours_contributed = Column(DECIMAL)

    volunteer = relationship("CustomUser")
    project = relationship("Project")
