from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from typing import List
from uuid import UUID
import os, shutil
import uuid
from datetime import date

from src.db.database import SessionLocal
from src.models.parents import Parent as ParentModel
from src.schemas.parents import Parent, ParentCreate, ParentUpdate
from src.routers.depens import get_current_user
from src.models.students import Student as StudentModel
from src.schemas.students import Student, StudentCreate, StudentUpdate

routerParents = APIRouter(
    prefix="/parents",
    tags=["parents"],

)

# Dependency DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# routes
@routerParents.post("/", response_model=Parent)
def create_parent(parent:ParentCreate, db:Session = Depends(get_db)):
    db_parent = ParentModel(
        first_name=parent.first_name,
        last_name=parent.last_name,
        phone=parent.phone,
        email=parent.email,
        address=parent.address,
        relationship_type=parent.relationship_type,
        occupation=parent.occupation,
    )

    if parent.student_ids:
        students_found = db.query(StudentModel).filter(StudentModel.id.in_(parent.student_ids)).all()
        db_parent.students = students_found

    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent

@routerParents.get("/", response_model=List[Parent])
def list_parents(db: Session = Depends(get_db)):
    parents = (
        db.query(ParentModel)
        .options(joinedload(ParentModel.students))
        .all()
    )
    return parents

@routerParents.get("/{parent_id}", response_model=Parent)
def get_parent(parent_id: UUID, db: Session = Depends(get_db)):
    parent = db.query(ParentModel).filter(ParentModel.id == parent_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent

@routerParents.put("/{parent_id}", response_model=Parent)
def update_parent(parent_id: UUID, parent_update: ParentUpdate, db: Session = Depends(get_db)):
    parent = db.query(ParentModel).filter(ParentModel.id == parent_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")

    parent.first_name = parent_update.first_name
    parent.last_name = parent_update.last_name
    parent.phone = parent_update.phone
    parent.email = parent_update.email
    parent.address = parent_update.address
    parent.relationship_type = parent_update.relationship_type
    parent.occupation = parent_update.occupation

    db.commit()
    db.refresh(parent)
    return parent 

@routerParents.delete("/{parent_id}", status_code=204)
def delete_parent(parent_id: UUID, db: Session = Depends(get_db)):
    parent = db.query(ParentModel).filter(ParentModel.id == parent_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    db.delete(parent)
    db.commit()
    return

