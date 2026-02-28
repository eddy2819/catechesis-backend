import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.database import Base


class GrupCatechistis(Base):
    __tablename__ = "grup_catechistis"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    address = Column(String(250), nullable=False)
    level = Column(String(100), nullable=False)


    students = relationship("Student", back_populates="grup")
    catechists = relationship("GrupCatechist", back_populates="grup", cascade="all, delete-orphan")

    
    
    