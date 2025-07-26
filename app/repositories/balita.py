from sqlalchemy.orm import Session, selectinload
from models.balita import Balita as BalitaModel
from models.pemeriksaan import Pemeriksaan as PemeriksaanModel
from models.posyandu import Posyandu as PosyanduModel
from schemas.balita import BalitaCreate, BalitaUpdate
from utils.stunting import tentukan_status_stunting
from datetime import datetime
from dateutil.relativedelta import relativedelta

class BalitaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, balita_id: int) -> BalitaModel | None:
        return (
            self.db.query(BalitaModel)
            .options(selectinload(BalitaModel.posyandu))
            .filter(BalitaModel.id == balita_id)
            .first()
        )

    def get_by_nik(self, nik: str) -> BalitaModel | None:
        return self.db.query(BalitaModel).filter(BalitaModel.nik == nik).first()

    def get_all(self, skip: int = 0) -> list[BalitaModel]:
        return (
            self.db.query(BalitaModel)
            .options(selectinload(BalitaModel.posyandu))
            .offset(skip)
            .all()
        )

    def create(self, balita: BalitaCreate) -> dict:
        db_balita = BalitaModel(
            nama=balita.nama,
            nik=balita.nik,
            nama_orang_tua=balita.nama_orang_tua,
            posyandu_id=balita.posyandu_id,
            tanggal_lahir=balita.tanggal_lahir,
            jenis_kelamin=balita.jenis_kelamin.value,
            rt=balita.rt,
            rw=balita.rw,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        print(db_balita)
        self.db.add(db_balita)
        self.db.commit()
        self.db.refresh(db_balita)

        status = tentukan_status_stunting(
            berat=balita.berat_badan,
            tinggi=balita.tinggi_badan,
            tanggal_lahir=balita.tanggal_lahir,  
            jenis_kelamin=balita.jenis_kelamin 
        )

        rd = relativedelta(datetime.utcnow().date(), balita.tanggal_lahir.date())
        usia_bulan = rd.years * 12 + rd.months

        db_pemeriksaan = PemeriksaanModel(
            balita_id=db_balita.id,
            tanggal_pemeriksaan=datetime.utcnow(), 
            tinggi_badan=balita.tinggi_badan,
            berat_badan=balita.berat_badan,
            usia_bulan=usia_bulan, 
            status_stunting=status["status_stunting"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        self.db.add(db_pemeriksaan)
        self.db.commit()

        return {
            "id": db_balita.id,
            "nama": db_balita.nama,
            "nik": db_balita.nik,
            "nama_orang_tua": db_balita.nama_orang_tua,
            "posyandu_id": db_balita.posyandu_id,
            "tanggal_lahir": db_balita.tanggal_lahir,
            "jenis_kelamin": db_balita.jenis_kelamin,
            "rt": db_balita.rt,
            "rw": db_balita.rw,
            "posyandu" : db_balita.posyandu,
            "created_at": db_balita.created_at,
            "updated_at": db_balita.updated_at,
            "status": status 
        }

    def update(self, balita_id: int, balita_data: BalitaUpdate) -> BalitaModel | None:
        db_balita = self.get_by_id(balita_id)
        if db_balita:
            update_data = balita_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_balita, key, value)
            self.db.commit()
            self.db.refresh(db_balita)
        return db_balita

    def delete(self, balita_id: int) -> BalitaModel | None:
        db_balita = self.get_by_id(balita_id)
        if db_balita:
            self.db.delete(db_balita)
            self.db.commit()
        return db_balita
    
    def search(self) -> list[BalitaModel]:
        return (
            self.db.query(BalitaModel)
            .options(
                selectinload(BalitaModel.posyandu),
                selectinload(BalitaModel.pemeriksaan)
            )
            .all()
        )