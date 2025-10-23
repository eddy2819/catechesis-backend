import uuid
from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.database import Base

class Sacrament(Base):
    __tablename__ = "sacraments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)

    baptism_date = Column(Date, nullable=True)
    first_communion_date = Column(Date, nullable=True)
    confirmation_date = Column(Date, nullable=True)
  

    student = relationship("Student", back_populates="sacrament")
