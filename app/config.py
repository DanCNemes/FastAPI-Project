from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str = ""
    DATABASE_PORT: str
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    DATABASE: str
    DATABASE_DRIVER: str

    class Config:
        env_file = ".env"

settings = Settings()