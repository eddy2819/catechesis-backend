from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.schemas.users import UserOut
from src.models.user import User
from src.routers.depens import get_current_user, require_roles 
from src.db.database import get_db
from src.models.enums import UserRole

routerUsers = APIRouter(
    prefix="/users", 
    tags=["users"]
)

@routerUsers.get("/", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), current_user: User = Depends(
    require_roles([
        UserRole.admin,
        UserRole.catequista,
        UserRole.secretario
        ]))):
    return db.query(User).all() 