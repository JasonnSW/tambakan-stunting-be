from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Balita(Base):
    __tablename__ = "balita"
    
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, nullable=False)
    nik = Column(String(16), unique=True, nullable=False)
    nama_orang_tua = Column(String, nullable=False)
    posyandu_id = Column(Integer, ForeignKey("posyandu.id"))
    tanggal_lahir = Column(DateTime)
    jenis_kelamin = Column(String(1))
    rt = Column(String, nullable=True)
    rw = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    posyandu = relationship("Posyandu", back_populates="balita")
    pemeriksaan = relationship("Pemeriksaan", back_populates="balita")