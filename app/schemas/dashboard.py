from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
from schemas.pemeriksaan import PemeriksaanResponse

class DashboardStats(BaseModel):
    total_balita: int
    kasus_stunting: int
    status_normal: int
    bulan_ini: int
    persentase_stunting: float
    persentase_normal: float

class TrendData(BaseModel):
    bulan: str
    total_pemeriksaan: int
    kasus_stunting: int
    status_normal: int

class DashboardResponse(BaseModel):
    stats: DashboardStats
    trend_data: List[TrendData]
    aktivitas_terbaru: List[PemeriksaanResponse]