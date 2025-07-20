from fastapi import APIRouter
from schemas.user import UserLogin
from services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(user: UserLogin):
    return AuthService.authenticate(user)
