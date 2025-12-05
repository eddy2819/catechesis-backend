import uuid
from sqlalchemy import Column, String, Date, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.database import Base
import enum

class StudentStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"

class Student(Base): 
    __tablename__ = "students"

    id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(Date, nullable=False)
    grade = Column(String(20), nullable=True)
    allergies = Column(String(200), nullable=True)
    medical_conditions = Column(String(200), nullable=True)
    status = Column(Enum(StudentStatus), default=StudentStatus.active, nullable=False)
    photo_url = Column(Text, nullable=True)

    parents = relationship("Parent", secondary="parent_student", back_populates="students")
    # Relations: back_populates names must match the attribute name on the other model
    notes = relationship("Note", back_populates="student")
    sacrament = relationship("Sacrament", uselist=False, back_populates="student", cascade="all, delete")
    attendance_records = relationship("StudentAttendance", back_populates="student", cascade="all, delete")


