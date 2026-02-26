from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date

from src.db.database import get_db
from src.models.catechist import Catechist as CatechistModel
from src.models.catechist_attendance import CatechistAttendance as CatechistAttendanceModel
from src.schemas.catechist import Catechist, CatechistCreate, CatechistUpdate, CatechistAttendance, CatechistAttendanceCreate, CatechistAttendanceUpdate

routerCatechists = APIRouter(prefix="/catechists", tags=["Catechists"], )


@routerCatechists.post("/", response_model=Catechist , status_code=201)
def create_Catechist(catechist: CatechistCreate, db: Session = Depends(get_db)):
    db_catechist = CatechistModel(**catechist.dict())
    db.add(db_catechist)
    db.commit()
    db.refresh(db_catechist)
    return db_catechist

@routerCatechists.get("/", response_model=list[Catechist], status_code=200)
def list_catechists(db: Session = Depends(get_db)):
    return db.query(CatechistModel).all()


@routerCatechists.get("/attendance", response_model=list[CatechistAttendance], status_code=200)
def list_all_attendance(db: Session = Depends(get_db)):
    return db.query(CatechistAttendanceModel).all()

@routerCatechists.get("/attendance/by-date/{event_date}", response_model=list[CatechistAttendance], status_code=200)
def list_attendance_by_date(event_date: date, db: Session = Depends(get_db)):
    return db.query(CatechistAttendanceModel).filter(CatechistAttendanceModel.event_date == event_date).all()

@routerCatechists.get("/{catechist_id}", response_model=Catechist, status_code=200)
def get_catechist(catechist_id: UUID, db: Session = Depends(get_db)):
    catechist = db.query(CatechistModel).filter(CatechistModel.id == catechist_id).first()
    if not catechist:
        raise HTTPException(status_code=404, detail="Catechist not found")
    return catechist


@routerCatechists.put("/{catechist_id}", response_model=Catechist, status_code=200)
def update_catechist(catechist_id: UUID, catechist_update: CatechistCreate, db: Session = Depends(get_db)):
    catechist = db.query(CatechistModel).filter(CatechistModel.id == catechist_id).first()
    if not catechist:
        raise HTTPException(status_code=404, detail="Catechist not found")
    for key, value in catechist_update.dict(exclude_unset=True).items():
        setattr(catechist, key, value)
    db.commit()
    db.refresh(catechist)
    return catechist

@routerCatechists.delete("/{catechist_id}", status_code=204)
def delete_catechist(catechist_id: UUID, db: Session = Depends(get_db)):
    catechist = db.query(CatechistModel).filter(CatechistModel.id == catechist_id).first()
    if not catechist:
        raise HTTPException(status_code=404, detail="Catechist not found")
    db.delete(catechist)
    db.commit()
    return {"message": "Catechist deleted successfully"}


@routerCatechists.post("/{catechist_id}/attendance", response_model=CatechistAttendance, status_code=201)
def mark_attendance(catechist_id: UUID, attendance: CatechistAttendanceCreate, db: Session = Depends(get_db)):
    data = attendance.dict()
    data["catechist_id"] = catechist_id

    db_attendance = CatechistAttendanceModel(**data)
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@routerCatechists.get("/{catechist_id}/attendance", response_model=list[CatechistAttendance], status_code=200)
def list_attendance(catechist_id: UUID, db: Session = Depends(get_db)):
    return db.query(CatechistAttendanceModel).filter(CatechistAttendanceModel.catechist_id == catechist_id).all()



