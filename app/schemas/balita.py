from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class JenisKelamin(str, Enum):
    LAKI_LAKI = "L"
    PEREMPUAN = "P"

class BalitaBase(BaseModel):
    nama: str
    nik: str
    nama_orang_tua: str
    posyandu_id: int
    tanggal_lahir: datetime
    jenis_kelamin: JenisKelamin

class BalitaCreate(BalitaBase):
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
    
    class Config:
        from_attributes = True

class BalitaWithPosyandu(BalitaResponse):
    posyandu: Optional["PosyanduResponse"] = None

class BalitaWithPemeriksaan(BalitaResponse):
    pemeriksaan: List["PemeriksaanResponse"] = []

class BalitaWithAll(BalitaResponse):
    posyandu: Optional["PosyanduResponse"] = None
    pemeriksaan: List["PemeriksaanResponse"] = []