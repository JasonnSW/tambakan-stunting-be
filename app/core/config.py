from pydantic_settings import BaseSettings, SettingsConfigDict 
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str
    app_env: str
    database_url: str
    secret_key: str
    admin_username: str
    admin_password: str

    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

@lru_cache()
def get_settings():
    return Settings()