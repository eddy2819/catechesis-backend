from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from src.core.config import settings
from sqlalchemy.orm import Session
from src.db.database import get_db
from typing import List
from src.models.user import User
import uuid
from src.core.security import SECRET_KEY, ALGORITHM
from src.models.enums import UserRole



security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}, 
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str: str | None = payload.get("sub")
        if not user_id_str:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Convertir string a UUID (tu columna es UUID(as_uuid=True))
    try:
        user_uuid = uuid.UUID(user_id_str)
    except (ValueError, TypeError):
        raise credentials_exception

    user = db.query(User).filter(User.id == user_uuid).first()
    if not user:
        raise credentials_exception

    return user  # devuelve instancia ORM User 

def require_roles(allowed_roles: List[UserRole]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"}, 
            )
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
                headers={"WWW-Authenticate": "Bearer"}, 
            )
        return current_user 
    return role_checker        

