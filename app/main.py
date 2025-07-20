from fastapi import FastAPI
from core.config import get_settings
from api import balita_router, posyandu_router, pemeriksaan_router, auth_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API Stunting",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(balita_router.router)
app.include_router(posyandu_router.router)
app.include_router(pemeriksaan_router.router)
app.include_router(auth_router.router)

@app.get("/")
def root():
    return {"message": "API Stunting aktif"}
