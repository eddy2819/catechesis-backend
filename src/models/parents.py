import uuid
from sqlalchemy import Column, String, Text, Table, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.database import Base

parent_student = Table(
    "parent_student",
    Base.metadata,
    Column("parent_id", UUID(as_uuid=True), ForeignKey("parents.id"), primary_key=True),
    Column("student_id", UUID(as_uuid=True), ForeignKey("students.id"), primary_key=True)
)

class Parent(Base):
    __tablename__ = "parents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    relationship_type = Column(String(20), nullable=False)  # madre, padre, tutor, otro
    address = Column(Text, nullable=True)
    occupation = Column(String(100), nullable=True)

    students = relationship("Student", secondary="parent_student", back_populates="parents")