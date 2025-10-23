from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import date
from uuid import UUID
from .sacraments import Sacrament, SacramentCreate

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    grade: Optional[str] = None
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    status: Literal["active", "inactive"] = "active"
    sacrament: Optional[SacramentCreate] = None


class StudentCreate(StudentBase):
    sacrament: Optional[SacramentCreate] = None

class StudentUpdate(StudentBase):
    sacrament: Optional[SacramentCreate] = None

class Student(StudentBase):
    id: UUID
    sacrament: Optional[Sacrament] = None

    class Config:
        from_attributes = True