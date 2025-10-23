import uuid
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.database import Base
import enum

# Opcional: categorías de notas
class NoteCategory(str, enum.Enum):
    OBSERVATION = "observation"
    BEHAVIOR = "behavior"
    TASK = "task"
    OTHER = "other"

class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    student = relationship("Student", back_populates="notes")
    
    # Opcional: quién creó la nota (profesor)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    author = relationship("User")
    
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    
    category = Column(Enum(NoteCategory), nullable=True, default=NoteCategory.OTHER)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
