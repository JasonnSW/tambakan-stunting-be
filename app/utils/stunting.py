from pygrowup import Calculator, helpers
from decimal import Decimal
import datetime
from models.pemeriksaan import StatusStunting

# Inisialisasi objek Calculator
calculator = Calculator(
    adjust_height_data=False,
    adjust_weight_scores=False,
    include_cdc=False,
    logger_name='pygrowup',
    log_level='INFO'
)

def tentukan_status_stunting(
    berat: Decimal,
    tinggi: Decimal,
    tanggal_lahir: datetime.date,
    jenis_kelamin: str
) -> dict:
    if tinggi <= 0 or berat <= 0:
        return {
            "status_stunting": "Tidak Dapat Ditentukan",
            "rekomendasi": "Data tidak valid",
            "zscore_tbu": None,
            "kategori_tbu": None,
            "zscore_bbtb": None,
            "kategori_bbtb": None
        }
    print("TINGGI:", berat)
    print("BERAT:", tinggi)
    print("LAHIR:", tanggal_lahir)
    print("JENIS KELAMIN:", jenis_kelamin)

    try:
        # Format tanggal lahir untuk pygrowup
        dob_str = tanggal_lahir.strftime("%d%m%y")
        valid_date = helpers.get_good_date(dob_str)[1]
        valid_age = helpers.date_to_age_in_months(valid_date)

        # Format jenis kelamin (pygrowup expects 'M' or 'F')
        valid_gender = helpers.get_good_sex(jenis_kelamin)

        # Hitung Z-score TB/U
        zscore_tbu = round(calculator.lhfa(float(tinggi), valid_age, valid_gender), 2)

        # Hitung Z-score BB/TB
        zscore_bbtb = round(calculator.wfl(float(berat), valid_age, valid_gender, float(tinggi)), 2)

        # Interpretasi kategori TB/U
        kategori_tbu = (
            "Sangat Pendek" if zscore_tbu < -3 else
            "Pendek" if zscore_tbu < -2 else
            "Normal"
        )

        # Interpretasi kategori BB/TB
        kategori_bbtb = (
            "Gizi Buruk" if zscore_bbtb < -3 else
            "Gizi Kurang" if zscore_bbtb < -2 else
            "Normal" if zscore_bbtb <= 2 else
            "Gizi Lebih"
        )

        status = StatusStunting.STUNTING if zscore_tbu < -2 else StatusStunting.NORMAL
        rekomendasi = "Segera ke posyandu atau puskesmas" if zscore_tbu < -2 else "Pertahankan kondisi ini"

        return {
            "zscore_tbu": zscore_tbu,
            "kategori_tbu": kategori_tbu,
            "zscore_bbtb": zscore_bbtb,
            "kategori_bbtb": kategori_bbtb,
            "status_stunting": status,
            "rekomendasi": rekomendasi
        }

    except Exception as e:
        return {
            "status_stunting": None,
            "rekomendasi": f"Gagal menghitung: {str(e)}",
            "zscore_tbu": None,
            "kategori_tbu": None,
            "zscore_bbtb": None,
            "kategori_bbtb": None
        }
