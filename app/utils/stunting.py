from decimal import Decimal
from schemas.pemeriksaan import StatusStunting

def tentukan_status_stunting(tinggi_badan: Decimal, usia_bulan: int) -> StatusStunting:
    if usia_bulan < 24:
        return StatusStunting.STUNTING if tinggi_badan < 80 else StatusStunting.NORMAL
    elif usia_bulan < 60:
        return StatusStunting.STUNTING if tinggi_badan < 100 else StatusStunting.NORMAL
    else:
        return StatusStunting.NORMAL
