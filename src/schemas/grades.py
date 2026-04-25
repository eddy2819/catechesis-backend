from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import date
from typing import Optional, List

class GradeBase(BaseModel):
    evaluation_id: UUID
    student_id: UUID
    score: float
    comments: Optional[str] = None

class GradeCreate(GradeBase):
    pass

class GradeResponse(GradeBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class EvaluationBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: date
    max_score: float
    type: str
    grup_id: UUID
    catechist_id: UUID

class EvaluationCreate(EvaluationBase):
    pass

class EvaluationResponse(EvaluationBase):
    id: UUID
    grades: List[GradeResponse] = []
    model_config = ConfigDict(from_attributes=True)
