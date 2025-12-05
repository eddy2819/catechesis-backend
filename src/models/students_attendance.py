from sqlalchemy import Column, Date, Enum, ForeignKey, String
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import sqlalchemy as sa
from src.db.database import Base
from src.models.enums import AttendanceStatus


class StudentAttendance(Base):
    __tablename__ = "student_attendance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(sa.Enum(AttendanceStatus, name="attendance_status"), nullable=False)
    notes = Column(String, nullable=True)

    student = relationship("Student", back_populates="attendance_records")
