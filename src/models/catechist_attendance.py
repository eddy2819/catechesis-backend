import uuid
from sqlalchemy import Column, String, Date, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from src.db.database import Base
from src.models.enums import AttendanceStatus




class CatechistAttendance(Base):
    __tablename__ = "catechist_attendance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    catechist_id = Column(UUID(as_uuid=True), ForeignKey("catechists.id"), nullable=False)
    event_date = Column(Date, nullable=False)
    status = Column(sa.Enum(AttendanceStatus), nullable=False, default=AttendanceStatus.presente)
    notes = Column(String(500), nullable=True)

    catechist = relationship("Catechist", back_populates="attendances")