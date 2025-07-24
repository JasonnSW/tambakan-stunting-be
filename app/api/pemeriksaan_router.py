from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.database import get_db
from services.pemeriksaan import PemeriksaanService
from schemas.pemeriksaan import PemeriksaanCreate, PemeriksaanUpdate, PemeriksaanResponse, PemeriksaanSimpleCreate
from typing import List

router = APIRouter(
    prefix="/pemeriksaan",
    tags=["Pemeriksaan"]
)

@router.get("/", response_model=list[PemeriksaanResponse])
def get_all(db: Session = Depends(get_db)):
    return PemeriksaanService(db).get_all_pemeriksaan()

@router.get("/{id}", response_model=PemeriksaanResponse)
def get_by_id(id: int, db: Session = Depends(get_db)):
    return PemeriksaanService(db).get_pemeriksaan_by_id(id)

@router.post("/", response_model=PemeriksaanResponse, status_code=status.HTTP_201_CREATED)
def create(data: PemeriksaanCreate, db: Session = Depends(get_db)):
    return PemeriksaanService(db).create_pemeriksaan(data)

@router.post("/simple", response_model=PemeriksaanResponse)
def create_simple(data: PemeriksaanSimpleCreate, db: Session = Depends(get_db)):
    service = PemeriksaanService(db)
    return service.create_simple_pemeriksaan(data)

@router.get("/balita/{nik}/riwayat", response_model=List[PemeriksaanResponse])
def get_riwayat(nik: str, db: Session = Depends(get_db)):
    service = PemeriksaanService(db)
    return service.get_riwayat_by_nik(nik)

@router.put("/{id}", response_model=PemeriksaanResponse)
def update(id: int, data: PemeriksaanUpdate, db: Session = Depends(get_db)):
    return PemeriksaanService(db).update_pemeriksaan(id, data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    PemeriksaanService(db).delete_pemeriksaan(id)
    return {"message": "Pemeriksaan berhasil dihapus"}
