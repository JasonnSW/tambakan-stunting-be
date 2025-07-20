from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.balita import BalitaRepository
from schemas.balita import BalitaCreate, BalitaUpdate

class BalitaService:
    def __init__(self, db: Session):
        self.repo = BalitaRepository(db)

    def get_balita_by_id(self, balita_id: int):
        db_balita = self.repo.get_by_id(balita_id)
        if not db_balita:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data balita tidak ditemukan")
        return db_balita

    def get_all_balita(self, skip: int, limit: int):
        return self.repo.get_all(skip, limit)

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