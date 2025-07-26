from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.balita import BalitaRepository
from schemas.balita import BalitaCreate, BalitaUpdate, BalitaSearchResponse
from schemas.pemeriksaan import RiwayatPemeriksaan, StatusTerkini
from models.pemeriksaan import Pemeriksaan
from models.posyandu import Posyandu
from datetime import date
from typing import List, Optional

def hitung_usia_dalam_bulan(tanggal_lahir: date, tanggal_skrg: date) -> int:
    return (tanggal_skrg.year - tanggal_lahir.year) * 12 + (tanggal_skrg.month - tanggal_lahir.month)

class BalitaService:
    def __init__(self, db: Session):
        self.repo = BalitaRepository(db)

    def get_balita_by_id(self, balita_id: int):
        db_balita = self.repo.get_by_id(balita_id)
        if not db_balita:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data balita tidak ditemukan")
        return db_balita

    def get_all_balita(self, skip: int):
        return self.repo.get_all(skip)

    def create_balita(self, balita: BalitaCreate):
        existing_balita = self.repo.get_by_nik(balita.nik)
        if existing_balita:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="NIK sudah terdaftar")
        return self.repo.create(balita)

    def update_balita(self, balita_id: int, balita_data: BalitaUpdate):
        self.get_balita_by_id(balita_id) 
        return self.repo.update(balita_id, balita_data)

    def delete_balita(self, balita_id: int):
        self.get_balita_by_id(balita_id)
        return self.repo.delete(balita_id)

    def search_balita(self, nik: Optional[str] = None, nama: Optional[str] = None) -> list[BalitaSearchResponse]:
        result = []

        all_balita = self.repo.search()

        for b in all_balita:
            if len(b.pemeriksaan) == 0:
                self.repo.delete(b.id)

        balita_list = [
            b for b in all_balita
            if len(b.pemeriksaan) > 0
        ]
        
        if nik:
            balita_list = [b for b in balita_list if b.nik == nik]
        elif nama:
            balita_list = [b for b in balita_list if nama.lower() in b.nama.lower()]

        today = date.today()

        for balita in balita_list:
            pemeriksaan_sorted = sorted(
                [p for p in balita.pemeriksaan if p.tanggal_pemeriksaan is not None],
                key=lambda x: x.id,
                reverse=True
            )

            latest_valid = next(
                (p for p in pemeriksaan_sorted if p.status_stunting is not None), 
                None
            )

            status_terkini = None
            if latest_valid:
                status_terkini = StatusTerkini(
                    status_stunting=latest_valid.status_stunting,
                    tinggi_badan=float(latest_valid.tinggi_badan),
                    berat_badan=float(latest_valid.berat_badan)
                )

            riwayat = [
                RiwayatPemeriksaan(
                    tanggal=p.tanggal_pemeriksaan,
                    tinggi_badan=float(p.tinggi_badan),
                    berat_badan=float(p.berat_badan),
                    posyandu=balita.posyandu.nama_posyandu if balita.posyandu else "-",
                    z_score_tb_u=p.zscore_tbu,
                    z_score_bb_tb=p.zscore_bbtb
                )
                for p in pemeriksaan_sorted  
            ]

            usia_bulan = hitung_usia_dalam_bulan(balita.tanggal_lahir, today)
            total_pemeriksaan = len(pemeriksaan_sorted)

            result.append(
                BalitaSearchResponse(
                    id=balita.id,
                    nama=balita.nama,
                    nik=balita.nik,
                    nama_orang_tua=balita.nama_orang_tua,
                    tanggal_lahir=balita.tanggal_lahir,
                    jenis_kelamin=balita.jenis_kelamin,
                    usia_bulan=usia_bulan,
                    total_pemeriksaan=total_pemeriksaan,
                    status_terkini=status_terkini,
                    riwayat_pemeriksaan=riwayat
                )
            )
        return result
