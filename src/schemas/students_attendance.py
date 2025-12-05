from pydantic import BaseModel
from typing import Optional
from datetime import date
from uuid import UUID
from src.models.enums import AttendanceStatus


class AttendanceBase(BaseModel):
    date: date
    status: AttendanceStatus
    notes: str | None = None

class AttendanceCreate(AttendanceBase):
    pass
    
class AttendanceUpdate(BaseModel):
    status: AttendanceStatus | None = None
    notes: str | None = None

class AttendanceResponse(AttendanceBase):
    id: UUID
    student_id: UUID

    class Config:
        orm_mode = True
