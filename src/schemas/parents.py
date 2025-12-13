from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID

class ParentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    relationship_type: str
    address: Optional[str]
    occupation: Optional[str]


class ParentCreate(ParentBase):
    student_ids: List[UUID] = []

class ParentUpdate(ParentBase):
    student_ids: List[UUID] = []

class Parent(ParentBase):
    id: UUID
    student_ids: List[UUID] = []

    class Config:
        orm_mode = True
        