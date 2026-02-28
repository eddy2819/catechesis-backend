from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class GrupBase(BaseModel):
    address: str = Field(..., description="Dirección del grupo")
    level: str = Field(..., description="Nivel del grupo")

class GrupCreate(GrupBase):
    pass

class GrupUpdate(GrupBase):
    pass

class GrupResponse(GrupBase):
    id: UUID
    
    class Config:
        from_attributes = True

class assign_catechist_to_grup(BaseModel):
    catechist_id: UUID
    rol: str