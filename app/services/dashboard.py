from sqlalchemy.orm import Session
from repositories.dashboard import DashboardRepository
from schemas.dashboard import DashboardResponse, DashboardStats, TrendData
from schemas.pemeriksaan import PemeriksaanResponse

def get_dashboard_data(db: Session) -> DashboardResponse:
    repo = DashboardRepository(db)

    total_balita = repo.get_total_balita()
    kasus_stunting = repo.get_kasus_stunting()
    status_normal = repo.get_status_normal()
    bulan_ini = repo.get_pemeriksaan_bulan_ini()

    persentase_stunting = (kasus_stunting / total_balita * 100) if total_balita else 0
    persentase_normal = (status_normal / total_balita * 100) if total_balita else 0

    trend_data_raw = repo.get_trend_data()
    trend_data = [
        TrendData(
            bulan = td.bulan.strip() if td.bulan else "",
            total_pemeriksaan=td.total_pemeriksaan,
            kasus_stunting=td.kasus_stunting,
            status_normal=td.status_normal,
        )
        for td in trend_data_raw
    ]

    aktivitas = repo.get_aktivitas_terbaru()
    aktivitas_response = [PemeriksaanResponse.from_orm(p) for p in aktivitas]

    return DashboardResponse(
        stats=DashboardStats(
            total_balita=total_balita,
            kasus_stunting=kasus_stunting,
            status_normal=status_normal,
            bulan_ini=bulan_ini,
            persentase_stunting=round(persentase_stunting, 1),
            persentase_normal=round(persentase_normal, 1),
        ),
        trend_data=trend_data,
        aktivitas_terbaru=aktivitas_response,
    )
