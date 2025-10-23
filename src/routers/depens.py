from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from src.core.config import settings
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.models.user import User
import uuid
from src.core.security import SECRET_KEY, ALGORITHM



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

