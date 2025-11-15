from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
from uuid import UUID
from src.models.enums import CatechistRole, CatechistStatus, AttendanceStatus

class CatechistBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    email: EmailStr
    phone_number: Optional[str] = None
    role: CatechistRole
    specialization: Optional[str] = None
    scheduled: Optional[str] = None
    status: CatechistStatus
    joined_date: date
    address: Optional[str] = None
    notes: Optional[str] = None

class CatechistCreate(CatechistBase):
    pass

class CatechistUpdate(CatechistBase):
    pass


class Catechist(CatechistBase):
    id: UUID

    class Config:
        orm_mode = True
        from_attributes = True


class CatechistAttendanceBase(BaseModel):
    event_date: date
    status: AttendanceStatus
    notes: Optional[str] = None

class CatechistAttendanceCreate(CatechistAttendanceBase):
    pass

class CatechistAttendanceUpdate(CatechistAttendanceBase):
    pass

class CatechistAttendance(CatechistAttendanceBase):
    id: UUID

    class Config:
        orm_mode = True
        from_attributes = True      
