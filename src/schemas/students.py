from pydantic import BaseModel, EmailStr
from typing import Optional, Literal, List
from datetime import date
from uuid import UUID
from .sacraments import Sacrament, SacramentCreate

class Parent(BaseModel):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class StudentBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: date
    grade: Optional[str] = None
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None
    status: Literal["active", "inactive"] = "active"
    photo_url: Optional[str] = None
    address: Optional[str] = None
    sacrament: Optional[SacramentCreate] = None
    parents : List[Parent] = []


class StudentCreate(StudentBase):
    sacrament: Optional[SacramentCreate] = None

class StudentUpdate(StudentBase):
    sacrament: Optional[SacramentCreate] = None
    parent_ids: Optional[List[UUID]] = None

class Student(StudentBase):
    id: UUID
    sacrament: Optional[Sacrament] = None

    class Config:
        from_attributes = True