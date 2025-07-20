from core.config import get_settings
from schemas.user import UserLogin
from fastapi import HTTPException, status
from core.security import create_access_token  
from datetime import timedelta


class AuthService:
    @staticmethod
    def authenticate(user: UserLogin):
        settings = get_settings()

        if user.username != settings.admin_username or user.password != settings.admin_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        expires = timedelta(minutes=60)
        
        access_token = create_access_token(
            data={"sub": user.username},
            expires_delta=expires
        )

        return {"access_token": access_token, "token_type": "bearer"}
