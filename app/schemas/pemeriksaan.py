from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum
from decimal import Decimal

class StatusStunting(str, Enum):
    NORMAL = "NORMAL"
    STUNTING = "STUNTING"

class PemeriksaanBase(BaseModel):
    balita_id: int
    tanggal_pemeriksaan: Optional[datetime] = None
    usia_bulan: Optional[int] = None 
    tinggi_badan: Decimal
    berat_badan: Decimal

class PemeriksaanSimpleCreate(PemeriksaanBase):
    status_stunting: Optional[str] = None

class PosyanduMini(BaseModel):
    nama_posyandu: str
    alamat: str

    class Config:
        from_attributes = True

class BalitaMini(BaseModel):
    nama: str
    nik: str
    nama_orang_tua: str
    posyandu: Optional[PosyanduMini] = None

    class Config:
        from_attributes = True

class AnalisisResult(BaseModel):
    status_stunting: str
    z_score: float

class StatusTerkini(BaseModel):
    status_stunting: Optional[StatusStunting] = None
    tinggi_badan: float
    berat_badan: float

class PemeriksaanInput(BaseModel):
    nik: str
    tanggal_lahir: datetime
    posyandu_id: int
    tanggal_pemeriksaan: datetime
    jenis_kelamin: str 
    tinggi_badan: float
    berat_badan: float
    
class RiwayatPemeriksaan(BaseModel):
    tanggal: datetime
    tinggi_badan: float
    berat_badan: float
    posyandu: str
    z_score_tb_u: Optional[float]
    z_score_bb_tb: Optional[float]

class PemeriksaanCreate(PemeriksaanBase):
    @validator('usia_bulan')
    def validate_usia_bulan(cls, v):
        if v < 0 or v > 60:  # 0-5 tahun
            raise ValueError('Usia bulan harus antara 0-60 bulan')
        return v
    
    @validator('tinggi_badan')
    def validate_tinggi_badan(cls, v):
        if v < 30 or v > 150:  # cm
            raise ValueError('Tinggi badan harus antara 30-150 cm')
        return v
    
    @validator('berat_badan')
    def validate_berat_badan(cls, v):
        if v < 1 or v > 50:  # kg
            raise ValueError('Berat badan harus antara 1-50 kg')
        return v

class PemeriksaanUpdate(BaseModel):
    tanggal_pemeriksaan: Optional[datetime] = None
    usia_bulan: Optional[int] = None
    tinggi_badan: Optional[Decimal] = None
    berat_badan: Optional[Decimal] = None
    status_stunting: Optional[StatusStunting] = None

    @validator('usia_bulan')
    def validate_usia_bulan(cls, v):
        if v is not None and (v < 0 or v > 60):
            raise ValueError('Usia bulan harus antara 0-60 bulan')
        return v
    
    @validator('tinggi_badan')
    def validate_tinggi_badan(cls, v):
        if v is not None and (v < 30 or v > 150):
            raise ValueError('Tinggi badan harus antara 30-150 cm')
        return v
    
    @validator('berat_badan')
    def validate_berat_badan(cls, v):
        if v is not None and (v < 1 or v > 50):
            raise ValueError('Berat badan harus antara 1-50 kg')
        return v

class PemeriksaanResponse(PemeriksaanBase):
    id: int
    balita_id: Optional[int] = None
    status_stunting: Optional[StatusStunting] = None 
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    balita: Optional[BalitaMini] = None
    tinggi_badan: Optional[Decimal] = None
    berat_badan: Optional[Decimal] = None

    class Config:
        from_attributes = True

class PemeriksaanStatus(BaseModel):
    zscore_tbu: float
    kategori_tbu: str
    zscore_bbtb: float
    kategori_bbtb: str
    status_stunting: StatusStunting
    rekomendasi: str

class PemeriksaanBalitaResponse(BaseModel):
    id: int
    nama: str
    nik: str
    nama_orang_tua: str
    tanggal_lahir: datetime
    jenis_kelamin: str
    posyandu_id: int
    rt: str
    rw: str
    status: PemeriksaanStatus

    class Config:
        from_attributes = True

class StatusStuntingInfo(BaseModel):
    status: StatusStunting
    zscore_tbu: float
    kategori_tbu: str
    zscore_bbtb: float
    kategori_bbtb: str
    rekomendasi: str

class PemeriksaanOutput(BaseModel):
    tanggal_pemeriksaan: datetime
    tinggi_badan: float
    berat_badan: float
    status_stunting: Optional[StatusStuntingInfo] = None 

class PemeriksaanWithBalita(PemeriksaanResponse):
    balita: Optional["BalitaResponse"] = None