from fastapi import APIRouter
from schemas.auth import LoginRequest, Token
from services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()

@router.post("/login", response_model=Token)
def login(request: LoginRequest):
    return auth_service.login(request)
