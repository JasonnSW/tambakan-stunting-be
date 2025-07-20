from sqlalchemy.orm import Session
from models.posyandu import Posyandu as PosyanduModel
from schemas.posyandu import PosyanduCreate, PosyanduUpdate

class PosyanduRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(PosyanduModel).all()

    def get_by_id(self, id: int):
        return self.db.query(PosyanduModel).filter(PosyanduModel.id == id).first()

    def create(self, posyandu_data: PosyanduCreate):
        new_posyandu = PosyanduModel(
            nama_posyandu=posyandu_data.nama_posyandu,
            alamat=posyandu_data.alamat
        )
        self.db.add(new_posyandu)
        self.db.commit()
        self.db.refresh(new_posyandu)
        return new_posyandu

    def update(self, id: int, posyandu_data: PosyanduUpdate):
        posyandu = self.get_by_id(id)
        if not posyandu:
            return None
        
        if posyandu_data.nama_posyandu is not None:
            posyandu.nama_posyandu = posyandu_data.nama_posyandu
        if posyandu_data.alamat is not None:
            posyandu.alamat = posyandu_data.alamat

        self.db.commit()
        self.db.refresh(posyandu)
        return posyandu

    def delete(self, id: int):
        posyandu = self.get_by_id(id)
        if not posyandu:
            return None

        self.db.delete(posyandu)
        self.db.commit()
        return posyandu
