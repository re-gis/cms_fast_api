from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from cms.config import Base

from cms.projects.models import Project



class CustomUser(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="volunteer")
    is_active = Column(Boolean, default=True)
    date_joined = Column(DateTime)

    projects = relationship("Project", back_populates="creator")
