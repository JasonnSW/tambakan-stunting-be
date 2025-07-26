from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.pemeriksaan import PemeriksaanRepository
from schemas.pemeriksaan import PemeriksaanCreate, PemeriksaanUpdate, PemeriksaanResponse, PemeriksaanSimpleCreate, PemeriksaanInput
from utils.stunting import tentukan_status_stunting
from dateutil.relativedelta import relativedelta
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

    def delete(self, id: int):
        pemeriksaan = self.repo.get_by_id(id)
        if not pemeriksaan:
            raise HTTPException(status_code=404, detail="Pemeriksaan tidak ditemukan")
        self.repo.delete(pemeriksaan)
        return {"message": "Pemeriksaan berhasil dihapus"}

    def delete_by_nik_and_month_year(self, nik: str, bulan: int, tahun: int):
        deleted = self.repo.delete_by_nik_and_month_year(nik, bulan, tahun)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pemeriksaan tidak ditemukan")
        return deleted

    def tambah_pemeriksaan(self, data: PemeriksaanInput):
        balita = self.repo.get_balita_by_nik(data.nik)
        if not balita:
            raise HTTPException(status_code=404, detail="Balita tidak ditemukan")

        # Hitung status stunting
        status_stunting = tentukan_status_stunting(
            berat=data.berat_badan,
            tinggi=data.tinggi_badan,
            tanggal_lahir=balita.tanggal_lahir,
            jenis_kelamin=balita.jenis_kelamin
        )

        # Hitung usia bulan
        rd = relativedelta(datetime.utcnow().date(), balita.tanggal_lahir.date())
        usia_bulan = rd.years * 12 + rd.months

        # Buat objek PemeriksaanModel
        db_pemeriksaan = Pemeriksaan(
            balita_id=balita.id,
            tanggal_pemeriksaan=data.tanggal_pemeriksaan,
            tinggi_badan=data.tinggi_badan,
            berat_badan=data.berat_badan,
            usia_bulan=usia_bulan,
            status_stunting=status_stunting["status_stunting"],
            zscore_tbu=status_stunting["zscore_tbu"],
            kategori_tbu=status_stunting["kategori_tbu"],
            zscore_bbtb=status_stunting["zscore_bbtb"],
            kategori_bbtb=status_stunting["kategori_bbtb"],
            rekomendasi=status_stunting["rekomendasi"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.repo.save_pemeriksaan(balita, db_pemeriksaan)

        return {
            "id": balita.id,
            "nama": balita.nama,
            "nik": balita.nik,
            "tanggal_pemeriksaan": data.tanggal_pemeriksaan,
            "nama_orang_tua": balita.nama_orang_tua,
            "posyandu_id": balita.posyandu_id,
            "tanggal_lahir": balita.tanggal_lahir,
            "jenis_kelamin": balita.jenis_kelamin,
            "rt": balita.rt,
            "rw": balita.rw,
            "posyandu": balita.posyandu,
            "created_at": balita.created_at,
            "updated_at": balita.updated_at,
            "status": status_stunting
        }