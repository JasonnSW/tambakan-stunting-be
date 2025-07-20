from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .base import Base

class Posyandu(Base):
    __tablename__ = "posyandu"
    
    id = Column(Integer, primary_key=True, index=True)
    nama_posyandu = Column(String, nullable=False)
    alamat = Column(String, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    balita = relationship("Balita", back_populates="posyandu")