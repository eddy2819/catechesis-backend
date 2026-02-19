import uuid
from sqlalchemy import Column, String, Boolean
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from src.db.database import Base
from src.models.enums import UserRole
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(sa.Enum(UserRole), nullable=False, default=UserRole.admin)
