from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.posyandu import PosyanduRepository
from schemas.posyandu import PosyanduCreate, PosyanduUpdate

class PosyanduService:
    def __init__(self, db: Session):
        self.repo = PosyanduRepository(db)

    def get_posyandu_by_id(self, posyandu_id: int):
        db_posyandu = self.repo.get_by_id(posyandu_id)
        if not db_posyandu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Data posyandu tidak ditemukan"
            )
        return db_posyandu

    def get_all_posyandu(self):
        return self.repo.get_all()

    def create_posyandu(self, posyandu_data: PosyanduCreate):
        return self.repo.create(posyandu_data)

    def update_posyandu(self, posyandu_id: int, posyandu_data: PosyanduUpdate):
        self.get_posyandu_by_id(posyandu_id)  
        return self.repo.update(posyandu_id, posyandu_data)

    def delete_posyandu(self, posyandu_id: int):
        self.get_posyandu_by_id(posyandu_id)  
        return self.repo.delete(posyandu_id)
