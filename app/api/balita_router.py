from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.balita import BalitaCreate, BalitaUpdate, BalitaResponse, BalitaWithPosyandu, BalitaSearchResponse,BalitaResponseWithStatus
from services.balita import BalitaService
from core.database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/balita",
    tags=["Balita"]
)

@router.post("/", response_model=BalitaResponseWithStatus, status_code=status.HTTP_201_CREATED)
def create_balita_endpoint(
    balita_data: BalitaCreate, 
    db: Session = Depends(get_db)
):
    service = BalitaService(db)
    return service.create_balita(balita_data)

@router.get("/search", response_model=List[BalitaSearchResponse])
def search_balita(nik: Optional[str] = None, nama: Optional[str] = None, db: Session = Depends(get_db)):
    return BalitaService(db).search_balita(nik=nik, nama=nama)


@router.get("/", response_model=List[BalitaWithPosyandu])
def get_all_balita_endpoint(
    skip: int = 0, 
    db: Session = Depends(get_db)
):
    service = BalitaService(db)
    return service.get_all_balita(skip)

@router.get("/{balita_id}", response_model=BalitaWithPosyandu)
def get_balita_by_id_endpoint(
    balita_id: int, 
    db: Session = Depends(get_db)
):
    service = BalitaService(db)
    return service.get_balita_by_id(balita_id)

@router.put("/{balita_id}", response_model=BalitaResponse)
def update_balita_endpoint(
    balita_id: int, 
    balita_data: BalitaUpdate, 
    db: Session = Depends(get_db)
):
    service = BalitaService(db)
    return service.update_balita(balita_id, balita_data)

@router.delete("/{balita_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_balita_endpoint(
    balita_id: int, 
    db: Session = Depends(get_db)
):
    service = BalitaService(db)
    service.delete_balita(balita_id)
    return {"detail": "Data balita berhasil dihapus"}