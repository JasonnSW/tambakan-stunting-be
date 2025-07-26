from sqlalchemy.orm import Session
from sqlalchemy import extract
from models.pemeriksaan import Pemeriksaan as PemeriksaanModel
from models.balita import Balita as BalitaModel
from typing import List, Optional
from schemas.pemeriksaan import PemeriksaanCreate, PemeriksaanUpdate, PemeriksaanSimpleCreate

class PemeriksaanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(PemeriksaanModel).offset(skip).limit(limit).all()

    def get_by_id(self, id: int):
        return self.db.query(PemeriksaanModel).filter(PemeriksaanModel.id == id).first()

    def get_balita_by_nik(self, nik: str) -> Optional[BalitaModel]:
        return self.db.query(BalitaModel).filter(BalitaModel.nik == nik).first()

    def get_riwayat_by_balita_id(self, balita_id: int) -> List[PemeriksaanModel]:
        return (
            self.db.query(PemeriksaanModel)
            .filter(PemeriksaanModel.balita_id == balita_id)
            .order_by(PemeriksaanModel.tanggal_pemeriksaan.desc())
            .all()
        )

    def create(self, data: PemeriksaanCreate):
        db_data = PemeriksaanModel(**data.dict())
        self.db.add(db_data)

        balita = self.db.query(BalitaModel).filter(BalitaModel.id == db_data.balita_id).first()
        if balita:
            if balita.total_pemeriksaan is None:
                balita.total_pemeriksaan = 1
            else:
                balita.total_pemeriksaan += 1

        self.db.commit()
        self.db.refresh(db_data)
        return db_data
    
    def create_simple_pemeriksaan(self, data: PemeriksaanSimpleCreate):
        balita = self.db.query(Balita).filter(Balita.nik == data.nik).first()
        if not balita:
            raise HTTPException(status_code=404, detail="Balita tidak ditemukan")

        new_pemeriksaan = Pemeriksaan(
            balita_id=balita.id,
            tanggal_pemeriksaan=datetime.now(),
            tinggi_badan=data.tinggi_badan,
            berat_badan=data.berat_badan,
        )

        self.db.add(new_pemeriksaan)
        self.db.commit()
        self.db.refresh(new_pemeriksaan)
        return new_pemeriksaan

    def update(self, id: int, data: PemeriksaanUpdate):
        db_data = self.get_by_id(id)
        if not db_data:
            return None
        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_data, key, value)
        db_data.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(db_data)
        return db_data

    def delete(self, pemeriksaan: PemeriksaanModel):
        self.db.delete(pemeriksaan)
        self.db.commit()
    
    def delete_by_nik_and_month_year(self, nik: str, bulan: int, tahun: int):
        pemeriksaans = (
            self.db.query(PemeriksaanModel)
            .join(BalitaModel, PemeriksaanModel.balita_id == BalitaModel.id)
            .filter(
                BalitaModel.nik == nik,
                extract("month", PemeriksaanModel.tanggal_pemeriksaan) == bulan,
                extract("year", PemeriksaanModel.tanggal_pemeriksaan) == tahun
            )
            .all()
        )

        if not pemeriksaans:
            return None

        for pemeriksaan in pemeriksaans:
            self.db.delete(pemeriksaan)

        self.db.commit()
        return pemeriksaans

    def save_pemeriksaan(self, balita: BalitaModel, pemeriksaan: PemeriksaanModel):
        balita.pemeriksaan.append(pemeriksaan)
        self.db.add(balita)
        self.db.commit()
        self.db.refresh(balita)
