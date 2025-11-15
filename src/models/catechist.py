import uuid
from sqlalchemy import Column, String, Date, Enum
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.database import Base
from src.models.enums import CatechistRole, CatechistStatus


class Catechist(Base):
    __tablename__ = "catechists"

    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4,unique=True,nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(Date, nullable=True)
    email = Column(String(150), unique=True, nullable=False)
    phone_number = Column(String(20), nullable=True)
    role = Column(sa.Enum(CatechistRole), nullable=False, default=CatechistRole.catequista)
    specialization = Column(String(200), nullable=True)
    scheduled = Column(String(200), nullable=True)
    status = Column(sa.Enum(CatechistStatus), nullable=False, default=CatechistStatus.activo)
    joined_date = Column(Date, nullable=False)
    address = Column(String(250), nullable=True)
    notes = Column(String(500), nullable=True)

    attendances = relationship(
        "CatechistAttendance",
        back_populates="catechist",
        cascade="all, delete-orphan")
    