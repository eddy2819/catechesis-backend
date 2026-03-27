import uuid
from sqlalchemy import Column, String, Date, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.database import Base

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String(150), nullable=False)
    description = Column(String(250), nullable=True)
    date = Column(Date, nullable=False)
    max_score = Column(Float, nullable=False)
    type = Column(String(50), nullable=False)

    grup_id = Column(UUID(as_uuid=True), ForeignKey("grup_catechistis.id"), nullable=False)
    catechist_id = Column(UUID(as_uuid=True), ForeignKey("catechists.id"), nullable=False)

    grades = relationship("Grade", back_populates="evaluation", cascade="all, delete")