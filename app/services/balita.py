from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.balita import BalitaRepository
from schemas.balita import BalitaCreate, BalitaUpdate, BalitaSearchResponse
from schemas.pemeriksaan import RiwayatPemeriksaan, StatusTerkini
from models.pemeriksaan import Pemeriksaan
from models.posyandu import Posyandu

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
    
    def search_balita(self) -> list[BalitaSearchResponse]:
        result = []
        balita_list = self.repo.search()
        
        for balita in balita_list:
            pemeriksaan_sorted = sorted(balita.pemeriksaan, key=lambda x: x.tanggal_pemeriksaan, reverse=True)
            status_terkini = None

            if pemeriksaan_sorted:
                latest = pemeriksaan_sorted[0]
                status_terkini = StatusTerkini(
                    status_stunting=latest.status_stunting,
                    tinggi_badan=float(latest.tinggi_badan),
                    berat_badan=float(latest.berat_badan)
                )

            riwayat = [
                RiwayatPemeriksaan(
                    tanggal=p.tanggal_pemeriksaan,
                    tinggi_badan=float(p.tinggi_badan),
                    berat_badan=float(p.berat_badan),
                    posyandu=balita.posyandu.nama_posyandu if balita.posyandu else "-"
                )
                for p in pemeriksaan_sorted
            ]

            result.append(
                BalitaSearchResponse(
                    id=balita.id,
                    nama=balita.nama,
                    nik=balita.nik,
                    nama_orang_tua=balita.nama_orang_tua,
                    tanggal_lahir=balita.tanggal_lahir,
                    jenis_kelamin=balita.jenis_kelamin,
                    status_terkini=status_terkini,
                    riwayat_pemeriksaan=riwayat
                )
            )
        return result