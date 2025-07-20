from sqlalchemy.orm import Session
from models.pemeriksaan import Pemeriksaan as PemeriksaanModel
from schemas.pemeriksaan import PemeriksaanCreate, PemeriksaanUpdate

class PemeriksaanRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(PemeriksaanModel).offset(skip).limit(limit).all()

    def get_by_id(self, id: int):
        return self.db.query(PemeriksaanModel).filter(PemeriksaanModel.id == id).first()

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

    def delete(self, id: int):
        db_data = self.get_by_id(id)
        if not db_data:
            return None

        balita = self.db.query(BalitaModel).filter(BalitaModel.id == db_data.balita_id).first()
        if balita and balita.total_pemeriksaan:
            balita.total_pemeriksaan = max(0, balita.total_pemeriksaan - 1)

        self.db.delete(db_data)
        self.db.commit()
        return db_data