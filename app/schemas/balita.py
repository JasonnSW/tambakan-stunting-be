from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum
from schemas.posyandu import PosyanduResponse
from schemas.pemeriksaan import StatusStunting, RiwayatPemeriksaan, StatusTerkini, PemeriksaanBase

class JenisKelamin(str, Enum):
    LAKI_LAKI = "M"
    PEREMPUAN = "F"

class BalitaBase(BaseModel):
    nama: str
    nik: str
    nama_orang_tua: str
    posyandu_id: int
    tanggal_lahir: datetime
    jenis_kelamin: JenisKelamin
    rt: Optional[str]
    rw: Optional[str]

class StuntingResult(BaseModel):
    zscore_tbu: Optional[float] = None
    kategori_tbu: Optional[str] = None
    zscore_bbtb: Optional[float] = None
    kategori_bbtb: Optional[str] = None
    status_stunting: Optional[str] = None
    rekomendasi: Optional[str] = None

class BalitaCreateWithPemeriksaan(BalitaBase):
    tinggi_badan: float
    berat_badan: float

class BalitaCreate(BalitaCreateWithPemeriksaan):
    @validator('nik')
    def validate_nik(cls, v):
        if len(v) != 16:
            raise ValueError('NIK harus 16 digit')
        if not v.isdigit():
            raise ValueError('NIK hanya boleh berisi angka')
        return v

class BalitaUpdate(BaseModel):
    nama: Optional[str] = None
    nik: Optional[str] = None
    nama_orang_tua: Optional[str] = None
    posyandu_id: Optional[int] = None
    tanggal_lahir: Optional[datetime] = None
    jenis_kelamin: Optional[JenisKelamin] = None

    @validator('nik')
    def validate_nik(cls, v):
        if v is not None:
            if len(v) != 16:
                raise ValueError('NIK harus 16 digit')
            if not v.isdigit():
                raise ValueError('NIK hanya boleh berisi angka')
        return v

class BalitaResponse(BalitaBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    posyandu: Optional[PosyanduResponse] = None
    
    class Config:
        from_attributes = True

class BalitaResponseWithStatus(BalitaResponse):
    status: StuntingResult

class BalitaSearchResponse(BaseModel):
    id: int
    nama: str
    nik: str
    nama_orang_tua: str
    tanggal_lahir: datetime
    jenis_kelamin: str
    status_terkini: Optional[StatusTerkini]
    riwayat_pemeriksaan: List[RiwayatPemeriksaan]

class BalitaWithPosyandu(BaseModel):
    id: int
    nama: str
    nik: str
    nama_orang_tua: str
    tanggal_lahir: datetime
    jenis_kelamin: JenisKelamin
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    posyandu: Optional[PosyanduResponse] = None

    class Config:
        from_attributes = True

class BalitaWithPemeriksaan(BalitaResponse):
    pemeriksaan: List["PemeriksaanResponse"] = []

class BalitaWithAll(BalitaResponse):
    posyandu: Optional["PosyanduResponse"] = None
    pemeriksaan: List["PemeriksaanResponse"] = []