from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    UPLOAD_DIR: str = "uploads/"
    MAX_FILES_PER_UPLOAD: int = 10
    
    class Config:
        env_file = ".env"

settings = Settings()