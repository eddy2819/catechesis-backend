from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.schemas.users import UserOut
from src.models.user import User
from src.routers.depens import get_current_user
from src.db.database import get_db

routerUsers = APIRouter(
    prefix="/users", 
    tags=["users"]
)

@routerUsers.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(User).all()