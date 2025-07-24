from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.pemeriksaan import PemeriksaanRepository
from schemas.pemeriksaan import PemeriksaanCreate, PemeriksaanUpdate, PemeriksaanResponse, PemeriksaanSimpleCreate
from utils.stunting import tentukan_status_stunting
from models.pemeriksaan import Pemeriksaan
from datetime import datetime
from typing import List

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

    def get_riwayat_by_nik(self, nik: str) -> List[Pemeriksaan]:
        balita = self.repo.get_balita_by_nik(nik)
        if not balita:
            raise HTTPException(status_code=404, detail="Balita tidak ditemukan")
        return self.repo.get_riwayat_by_balita_id(balita.id)

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
    
    def create_simple_pemeriksaan(self, data: PemeriksaanSimpleCreate) -> Pemeriksaan:
        return self.repo.create_simple_pemeriksaan(data)

    def add_pemeriksaan(self, balita_id: int, data: PemeriksaanCreate):
        balita = self.repo.get_balita_by_id(balita_id)
        if not balita:
            raise HTTPException(status_code=404, detail="Balita tidak ditemukan")
        return self.repo.create_pemeriksaan(balita_id, data)

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
