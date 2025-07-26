from sqlalchemy.orm import Session
from datetime import datetime
from models import Balita, Pemeriksaan
from sqlalchemy import extract, func, case, desc
from sqlalchemy.orm import joinedload, aliased

class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_total_balita(self) -> int:
        return self.db.query(Balita).count()

    def get_kasus_stunting(self) -> int:
        latest = (
            self.db.query(Pemeriksaan)
            .distinct(Pemeriksaan.balita_id)
            .order_by(Pemeriksaan.balita_id, desc(Pemeriksaan.tanggal_pemeriksaan))
            .subquery()
        )

        alias = aliased(Pemeriksaan, latest)

        return (
            self.db.query(func.count())
            .select_from(alias)
            .filter(alias.status_stunting == "STUNTING")
            .scalar()
        )

    def get_status_normal(self) -> int:
        latest = (
            self.db.query(Pemeriksaan)
            .distinct(Pemeriksaan.balita_id)
            .order_by(Pemeriksaan.balita_id, desc(Pemeriksaan.tanggal_pemeriksaan))
            .subquery()
        )

        alias = aliased(Pemeriksaan, latest)

        return (
            self.db.query(func.count())
            .select_from(alias)
            .filter(alias.status_stunting == "NORMAL")
            .scalar()
        )

    def get_pemeriksaan_bulan_ini(self) -> int:
        now = datetime.now()
        return (
            self.db.query(Pemeriksaan)
            .filter(extract("month", Pemeriksaan.tanggal_pemeriksaan) == now.month)
            .filter(extract("year", Pemeriksaan.tanggal_pemeriksaan) == now.year)
            .count()
        )

    def get_trend_data(self):
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
            .all()
        )

    def get_aktivitas_terbaru(self):
        return (
            self.db.query(Pemeriksaan)
            .join(Pemeriksaan.balita)  
            .options(
                joinedload(Pemeriksaan.balita).joinedload(Balita.posyandu)
            )
            .order_by(Pemeriksaan.tanggal_pemeriksaan.desc())
            .all()
        )

