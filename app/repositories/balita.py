from sqlalchemy.orm import Session, selectinload
from models.balita import Balita as BalitaModel
from models.pemeriksaan import Pemeriksaan as PemeriksaanModel
from models.posyandu import Posyandu as PosyanduModel
from schemas.balita import BalitaCreate, BalitaUpdate

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

    def get_all(self, skip: int = 0, limit: int = 100) -> list[BalitaModel]:
        return (
            self.db.query(BalitaModel)
            .options(selectinload(BalitaModel.posyandu))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, balita: BalitaCreate) -> BalitaModel:
        db_balita = BalitaModel(
            nama=balita.nama,
            nik=balita.nik,
            nama_orang_tua=balita.nama_orang_tua,
            posyandu_id=balita.posyandu_id,
            tanggal_lahir=balita.tanggal_lahir,
            jenis_kelamin=balita.jenis_kelamin.value,
            rt=balita.rt,
            rw=balita.rw
        )
        self.db.add(db_balita)
        self.db.commit()
        self.db.refresh(db_balita)
        return db_balita

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