from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class PosyanduBase(BaseModel):
    nama_posyandu: str
    alamat: str

class PosyanduCreate(PosyanduBase):
    pass

class PosyanduUpdate(BaseModel):
    nama_posyandu: Optional[str] = None
    alamat: Optional[str] = None

class PosyanduResponse(PosyanduBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True  

class PosyanduWithBalita(PosyanduResponse):
    balita: List["BalitaResponse"] = []
