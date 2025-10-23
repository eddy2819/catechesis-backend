from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from uuid import UUID

from src.db.database import SessionLocal
from src.models.students import Student as StudentModel
from src.schemas.students import Student, StudentCreate, StudentUpdate
from src.routers.depens import get_current_user
from src.models.sacraments import Sacrament as SacramentModel


routerStudents = APIRouter(
    prefix="/students",
    tags=["students"],
)

# Dependency DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# routes
@routerStudents.post("/", response_model=Student)
def create_student(student:StudentCreate, db:Session = Depends(get_db)):
    db_student = StudentModel(
        first_name=student.first_name,
        last_name=student.last_name,
        birth_date=student.birth_date,
        grade=student.grade,
        allergies=student.allergies,
        medical_conditions=student.medical_conditions
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    if student.sacrament:
        db_sacrament = SacramentModel(
            student_id=db_student.id,
            baptism_date=student.sacrament.baptism_date,
            first_communion_date=student.sacrament.first_communion_date,
            confirmation_date=student.sacrament.confirmation_date
        )
        db.add(db_sacrament)
        db.commit()
        db.refresh(db_sacrament)

        # refresh student to load the newly created sacrament relationship
        db.refresh(db_student)

    return db_student

@routerStudents.get("/",response_model=List[Student])
def list_students(db: Session = Depends(get_db)):
    students =(
        db.query(StudentModel)
        .options(joinedload(StudentModel.sacrament))
    )
    return students.all()

@routerStudents.get("/{student_id}", response_model=Student)
def get_student(student_id: UUID, db: Session = Depends(get_db)):
    Student = (
        db.query(StudentModel)
        .options(joinedload(StudentModel.sacrament))
        .filter(StudentModel.id == student_id)
        .first()
    )
    if not Student:
        raise HTTPException(status_code=404, detail="Student not found")
    return Student

@routerStudents.put("/{student_id}", response_model=Student)
def update_student(stdent_id: UUID, student_update: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == stdent_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in student_update.dict().items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

@routerStudents.delete("/{student_id}", status_code=204)
def delete_student(student_id: UUID, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return