from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, DECIMAL
from sqlalchemy.orm import relationship
from .base import Base
import enum

class StatusStunting(enum.Enum):
    NORMAL = "NORMAL"
    STUNTING = "STUNTING"

class Pemeriksaan(Base):
    __tablename__ = "pemeriksaan"
    
    id = Column(Integer, primary_key=True, index=True)
    balita_id = Column(Integer, ForeignKey("balita.id", ondelete="CASCADE"))
    tanggal_pemeriksaan = Column(DateTime)
    usia_bulan = Column(Integer)
    tinggi_badan = Column(DECIMAL(5, 2))  
    berat_badan = Column(DECIMAL(5, 2))
    status_stunting = Column(Enum(StatusStunting))
    total_pemeriksaan = Column(Integer, default=0)

    zscore_tbu = Column(DECIMAL(5, 2))
    kategori_tbu = Column(String)
    zscore_bbtb = Column(DECIMAL(5, 2))
    kategori_bbtb = Column(String)
    rekomendasi = Column(String)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    balita = relationship("Balita", back_populates="pemeriksaan")
