from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from services.dashboard import get_dashboard_data
from schemas.dashboard import DashboardResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/", response_model=DashboardResponse)
def read_dashboard(db: Session = Depends(get_db)):
    return get_dashboard_data(db)
