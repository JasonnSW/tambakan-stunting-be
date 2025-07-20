from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.pemeriksaan import PemeriksaanRepository
from schemas.pemeriksaan import PemeriksaanCreate, PemeriksaanUpdate, PemeriksaanResponse
from utils.stunting import tentukan_status_stunting
from models.pemeriksaan import Pemeriksaan
from datetime import datetime

class PemeriksaanService:
    def __init__(self, db: Session):
        self.db = db 
        self.repo = PemeriksaanRepository(db)

    def get_all_pemeriksaan(self):
        return self.repo.get_all()

    def get_pemeriksaan_by_id(self, id: int):
        pemeriksaan = self.repo.get_by_id(id)
        if not pemeriksaan:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pemeriksaan tidak ditemukan")
        return pemeriksaan

    def create_pemeriksaan(self, pemeriksaan_data: PemeriksaanCreate) -> PemeriksaanResponse:
        status = tentukan_status_stunting(
            tinggi_badan=pemeriksaan_data.tinggi_badan,
            usia_bulan=pemeriksaan_data.usia_bulan
        )

        data_dict = pemeriksaan_data.model_dump()
        data_dict["status_stunting"] = status
        data_dict["created_at"] = datetime.utcnow()
        data_dict["updated_at"] = datetime.utcnow()

        return self.repo.create(PemeriksaanCreate(**data_dict))


    def update_pemeriksaan(self, id: int, data: PemeriksaanUpdate):
        existing = self.repo.get_by_id(id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pemeriksaan tidak ditemukan")
        return self.repo.update(id, data)

    def delete_pemeriksaan(self, id: int):
        existing = self.repo.get_by_id(id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pemeriksaan tidak ditemukan")
        return self.repo.delete(id)
