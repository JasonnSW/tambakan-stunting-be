from sqlalchemy.orm import Session
from datetime import datetime
from models import Balita, Pemeriksaan
from sqlalchemy import extract, func, case
from sqlalchemy.orm import joinedload

class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_total_balita(self) -> int:
        return self.db.query(Balita).count()

    def get_kasus_stunting(self) -> int:
        return self.db.query(Pemeriksaan).filter(Pemeriksaan.status_stunting == "STUNTING").count()

    def get_status_normal(self) -> int:
        return self.db.query(Pemeriksaan).filter(Pemeriksaan.status_stunting == "NORMAL").count()

    def get_pemeriksaan_bulan_ini(self) -> int:
        now = datetime.now()
        return (
            self.db.query(Pemeriksaan)
            .filter(extract("month", Pemeriksaan.tanggal_pemeriksaan) == now.month)
            .filter(extract("year", Pemeriksaan.tanggal_pemeriksaan) == now.year)
            .count()
        )

    def get_trend_data(self, limit: int = 6):
        return (
            self.db.query(
                func.to_char(Pemeriksaan.tanggal_pemeriksaan, "Month").label("bulan"),
                func.count().label("total_pemeriksaan"),
                func.sum(case((Pemeriksaan.status_stunting == "STUNTING", 1), else_=0)).label("kasus_stunting"),
                func.sum(case((Pemeriksaan.status_stunting == "NORMAL", 1), else_=0)).label("status_normal"),
            )
            .group_by(
                func.date_trunc("month", Pemeriksaan.tanggal_pemeriksaan),
                func.to_char(Pemeriksaan.tanggal_pemeriksaan, "Month")
            )
            .order_by(func.date_trunc("month", Pemeriksaan.tanggal_pemeriksaan).desc())
            .limit(limit)
            .all()
        )

    def get_aktivitas_terbaru(self, limit: int = 5):
        return (
            self.db.query(Pemeriksaan)
            .options(
                joinedload(Pemeriksaan.balita).joinedload(Balita.posyandu)
            )
            .order_by(Pemeriksaan.tanggal_pemeriksaan.desc())
            .limit(limit)
            .all()
        )
