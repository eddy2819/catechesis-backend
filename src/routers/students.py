from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from typing import List
from uuid import UUID
import os, shutil
import uuid
from datetime import date

from src.db.database import SessionLocal
from src.models.students import Student as StudentModel
from src.schemas.students import Student, StudentCreate, StudentUpdate
from src.routers.depens import get_current_user
from src.models.sacraments import Sacrament as SacramentModel
from src.models.students_attendance import StudentAttendance
from src.schemas.students_attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse


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

UPLOAD_DIR = "uploads/students/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

BASE_URL = "http://localhost:8000"

def build_full_url(student_model: StudentModel):
    """Construye la URL completa para photo_url si no la tiene."""
    if student_model.photo_url and not student_model.photo_url.startswith("http"):
        student_model.photo_url = f"{BASE_URL}{student_model.photo_url}"
    return student_model

# routes
@routerStudents.post("/", response_model=Student)
def create_student(student:StudentCreate, db:Session = Depends(get_db)):
    pthoto_url = None
    if student.photo_url:
        filename = f"{uuid.uuid4()}_{student.photo_url.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(student.photo_url.file.read())
        photo_url = f"{BASE_URL}/uploads/students/{filename}"

    db_student = StudentModel(
        first_name=student.first_name,
        last_name=student.last_name,
        birth_date=student.birth_date,
        grade=student.grade,
        allergies=student.allergies,
        medical_conditions=student.medical_conditions,
        photo_url=photo_url
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

@routerStudents.post("/upload-photo", status_code=200)
def upload_photo(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos de imagen.")
    
    # Crear un nombre de archivo único
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        # Guarda el archivo en el disco
        with open(file_path, "wb") as f:
             # Usamos shutil.copyfileobj que es más eficiente que file.read()
             shutil.copyfileobj(file.file, f)
    except Exception:
        raise HTTPException(status_code=500, detail="Error al guardar la imagen.")

    # Devuelve la URL pública
    # Asegúrate que tu FastAPI esté sirviendo la carpeta /uploads/
    photo_url = f"/uploads/students/{filename}" 
    return {"photo_url": photo_url}

@routerStudents.get("/",response_model=List[Student])
def list_students(db: Session = Depends(get_db)):
    students = (
        db.query(StudentModel)
        .options(
            joinedload(StudentModel.sacrament),
            joinedload(StudentModel.parents)
        )
        .all()
    )
    processed_students = [build_full_url(student) for student in students]
    return processed_students

@routerStudents.get("/{student_id}", response_model=Student)
def get_student(student_id: UUID, db: Session = Depends(get_db)):
    Student = (
        db.query(StudentModel)
        .options(joinedload(StudentModel.sacrament))
        .options(joinedload(StudentModel.parents))
        .filter(StudentModel.id == student_id)
        .first()
    )
    if not Student:
        raise HTTPException(status_code=404, detail="Student not found")
    Student = build_full_url(Student)
    return Student

@routerStudents.put("/{student_id}", response_model=Student)
def update_student(student_id: UUID, student_update: StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(StudentModel).options(
        joinedload(StudentModel.sacrament)
    ).filter(StudentModel.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    update_data = student_update.dict(exclude_unset=True)
    sacrament_data = update_data.pop("sacrament", None)

    # Actualiza campos simples (incluyendo 'photo_url' si vino como string)
    for key, value in update_data.items():
        setattr(student, key, value)
    
    # --- LÓGICA DE SACRAMENTO CORREGIDA ---
    if sacrament_data is not None:
        if student.sacrament:
            # Si el estudiante YA TIENE sacramentos, actualízalos
            for s_key, s_value in sacrament_data.items():
                setattr(student.sacrament, s_key, s_value)
        else:
            # Si el estudiante NO TIENE sacramentos, créalos
            new_sacrament = SacramentModel(**sacrament_data, student_id=student.id)
            db.add(new_sacrament)
    # --- FIN DE LA CORRECCIÓN --- (Tu 'else' anterior estaba mal y causaría un crash)

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



@routerStudents.post("/attendance", response_model=AttendanceResponse, status_code=201)
def mark_attendance(student_id: UUID, attendance: AttendanceCreate, db: Session = Depends(get_db)):
    record = StudentAttendance(
        student_id=student_id,
        date=attendance.date,
        status=attendance.status,
        notes=attendance.notes
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@routerStudents.get("/attendance/by-date/{selected_date}", response_model=List[AttendanceResponse], status_code=200)
def list_attendance_by_date(selected_date: date, db: Session = Depends(get_db)):
    records = db.query(StudentAttendance).filter(StudentAttendance.date == selected_date).all()
    return records


@routerStudents.put("/attendance/{attendance_id}", response_model=AttendanceResponse, status_code=200)
def update_attendance(attendance_id: UUID, updates: AttendanceUpdate, db: Session = Depends(get_db)):
    record = db.query(StudentAttendance).filter(StudentAttendance.id == attendance_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    if updates.status is not None:
        record.status = updates.status
    if updates.notes is not None:
        record.notes = updates.notes

    db.commit()
    db.refresh(record)
    return record