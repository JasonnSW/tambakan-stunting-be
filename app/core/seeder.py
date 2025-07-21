from models.posyandu import Posyandu
from core.database import SessionLocal
from core.config import get_settings
from datetime import datetime

seed_data = [
    {"nama_posyandu": "Tekik", "alamat": "Jl. Tekik"},
    {"nama_posyandu": "Tambakan", "alamat": "Jl. Tambakan"},
    {"nama_posyandu": "Kantor Desa", "alamat": "Jl. Kantor Desa"},
    {"nama_posyandu": "Sukorejo", "alamat": "Jl. Sukorejo"},
]

db = SessionLocal()

for data in seed_data:
    posyandu = Posyandu(
        nama_posyandu=data["nama_posyandu"],
        alamat=data["alamat"],
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(posyandu)

db.commit()
db.close()

print("Seeder Posyandu berhasil dijalankan.")

#tekik
#tambakan
#kantor desa
#sukorejo
