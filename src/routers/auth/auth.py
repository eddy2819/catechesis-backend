from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.users import UserCreate, UserLogin, Token
from src.db.database import get_db
from src.core.security import get_password_hash, verify_password, create_access_token
import uuid

routerAuth = APIRouter(prefix="/auth", tags=["auth"])

@routerAuth.post("/register", status_code=status.HTTP_201_CREATED, response_model=Token)
def register(user:UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_pw = get_password_hash(user.password)
    new_user = User(
        id =uuid.uuid4(),
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@routerAuth.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(data:UserLogin, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}