import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.db.database import Base


class GrupCatechist(Base):
    __tablename__ = "grup_catechist"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    grup_id  = Column(UUID(as_uuid=True), ForeignKey("grup_catechistis.id"), nullable=False)
    catechist_id = Column(UUID(as_uuid=True), ForeignKey("catechists.id"), nullable=False)

    rol = Column(String(20), nullable=False)

    grup = relationship("GrupCatechistis", back_populates="catechists")
    catechist = relationship("Catechist", back_populates="grups")
    