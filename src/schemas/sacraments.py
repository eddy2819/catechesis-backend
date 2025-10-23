from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID

class SacramentBase(BaseModel):
    baptism_date: Optional[date] = None
    first_communion_date: Optional[date] = None
    confirmation_date: Optional[date] = None

class SacramentCreate(SacramentBase):
    pass

class SacramentUpdate(SacramentBase):
    pass

class Sacrament(SacramentBase):
    id: UUID
    student_id: UUID

    class Config:
        from_attributes = True