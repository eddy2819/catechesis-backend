from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.db.database import get_db
from src.models.grades import Evaluation, Grade
from src.schemas.grades import (
    EvaluationCreate, EvaluationResponse,
    GradeCreate, GradeResponse
)

routerGrades = APIRouter(prefix="/grades", tags=["Grades"])

# Endpoints for Evaluations
@routerGrades.post("/evaluation", response_model=EvaluationResponse, status_code=201)
def create_evaluation(evaluation: EvaluationCreate, db: Session = Depends(get_db)):
    db_evaluation = Evaluation(**evaluation.model_dump())
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation

@routerGrades.get("/evaluation", response_model=List[EvaluationResponse])
def get_evaluations(db: Session = Depends(get_db)):
    return db.query(Evaluation).all()

@routerGrades.get("/evaluation/{evaluation_id}", response_model=EvaluationResponse)
def get_evaluation(evaluation_id: UUID, db: Session = Depends(get_db)):
    db_evaluation = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not db_evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return db_evaluation

# Endpoints for Grades
@routerGrades.post("/grade", response_model=GradeResponse, status_code=201)
def create_grade(grade: GradeCreate, db: Session = Depends(get_db)):
    # Calculate evaluation max score logic conceptually (not enforced here, could check if score > max_score)
    db_evaluation = db.query(Evaluation).filter(Evaluation.id == grade.evaluation_id).first()
    if not db_evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
        
    db_grade = Grade(**grade.model_dump())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

@routerGrades.get("/evaluation/{evaluation_id}/grades", response_model=List[GradeResponse])
def get_grades_by_evaluation(evaluation_id: UUID, db: Session = Depends(get_db)):
    return db.query(Grade).filter(Grade.evaluation_id == evaluation_id).all()

@routerGrades.get("/student/{student_id}/grades", response_model=List[GradeResponse])
def get_grades_by_student(student_id: UUID, db: Session = Depends(get_db)):
    return db.query(Grade).filter(Grade.student_id == student_id).all()
