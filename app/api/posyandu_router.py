from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.database import get_db
from services.posyandu import PosyanduService
from schemas.posyandu import PosyanduCreate, PosyanduUpdate, PosyanduResponse

router = APIRouter(
    prefix="/posyandu",
    tags=["Posyandu"]
)

@router.get("/", response_model=list[PosyanduResponse])
def get_all_posyandu(db: Session = Depends(get_db)):
    return PosyanduService(db).get_all_posyandu()

@router.get("/{posyandu_id}", response_model=PosyanduResponse)
def get_posyandu_by_id(posyandu_id: int, db: Session = Depends(get_db)):
    return PosyanduService(db).get_posyandu_by_id(posyandu_id)

@router.post("/", response_model=PosyanduResponse, status_code=status.HTTP_201_CREATED)
def create_posyandu(posyandu_data: PosyanduCreate, db: Session = Depends(get_db)):
    return PosyanduService(db).create_posyandu(posyandu_data)

@router.put("/{posyandu_id}", response_model=PosyanduResponse)
def update_posyandu(posyandu_id: int, posyandu_data: PosyanduUpdate, db: Session = Depends(get_db)):
    return PosyanduService(db).update_posyandu(posyandu_id, posyandu_data)

@router.delete("/{posyandu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posyandu(posyandu_id: int, db: Session = Depends(get_db)):
    PosyanduService(db).delete_posyandu(posyandu_id)
    return {"message": "Posyandu berhasil dihapus"}