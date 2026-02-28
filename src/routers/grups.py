from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from typing import List
from uuid import UUID
import os, shutil
import uuid
from datetime import date

from src.db.database import get_db
from src.schemas.grup import GrupCreate, GrupResponse, assign_catechist_to_grup
from src.models.grup_catechistis import GrupCatechistis
from src.models.grup_catechist import GrupCatechist
from src.models.catechist import Catechist
from src.models.students import Student

routerGrup = APIRouter(prefix="/grups", tags=["Grups"])

@routerGrup.post("/grup", response_model=GrupResponse)
def create_grup(grup: GrupCreate, db: Session = Depends(get_db)):
    db_grup = GrupCatechistis(**grup.dict())
    db.add(db_grup)
    db.commit()
    db.refresh(db_grup)
    return db_grup


@routerGrup.post("/grup/{grup_id}/catechist", response_model=GrupResponse)
def assign_catechist_to_grup(grup_id: UUID, catechist_id: UUID, rol: str = "catechist", db: Session = Depends(get_db)):
    db_grup = db.query(GrupCatechistis).filter(GrupCatechistis.id == grup_id).first()
    if not db_grup:
        raise HTTPException(status_code=404, detail="Grup not found")
    db_catechist = db.query(Catechist).filter(Catechist.id == catechist_id).first()
    if not db_catechist:
        raise HTTPException(status_code=404, detail="Catechist not found")
    db_grup_catechist = GrupCatechist(grup_id=grup_id, catechist_id=catechist_id, rol=rol)
    db.add(db_grup_catechist)
    db.commit()
    db.refresh(db_grup)
    return db_grup

@routerGrup.get("/grup", response_model=List[GrupResponse])
def get_grups(db: Session = Depends(get_db)):
    return db.query(GrupCatechistis).all()

@routerGrup.get("/grup/{grup_id}", response_model=GrupResponse)
def get_grup(grup_id: UUID, db: Session = Depends(get_db)):
    db_grup = db.query(GrupCatechistis).filter(GrupCatechistis.id == grup_id).first()
    if not db_grup:
        raise HTTPException(status_code=404, detail="Grup not found")
    return db_grup


@routerGrup.post("/{grupo_id}/auto-assign-students")
def auto_assign_students_to_grup(grupo_id: UUID, db: Session = Depends(get_db)):
    db_grup = db.query(GrupCatechistis).filter(GrupCatechistis.id == grupo_id).first()
    if not db_grup:
        raise HTTPException(status_code=404, detail="Grup not found")
        
    db_students = db.query(Student).filter(
        Student.grup_id == None,
        Student.address == db_grup.address
    ).all()
    
    for student in db_students:
        student.grup_id = grupo_id
    db.commit()
    db.refresh(db_grup)
    return {"message": "Students assigned successfully" , "students_assigned": len(db_students)} 