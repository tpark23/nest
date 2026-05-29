import re

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    UPLOAD_DIR: str = "uploads/"
    MAX_FILES_PER_UPLOAD: int = 10
    TRANSACTION_PATTERNS = [
        re.compile(r'^(?P<transaction_date>\d{2}/\d{2})\s+(?P<posting_date>\d{2}/\d{2})\s+(?P<description>.+?)\s+(?P<amount>\d+\.\d{2}),?$'),
        re.compile(r'^(?P<transaction_date>\d{2}/\d{2})\s+(?P<posting_date>\d{2}/\d{2})\s+(?P<description>.+?)\s+(?P<amount>-?\d+\.\d{2}),?$'), # negative
        re.compile(r'^(?P<transaction_date>\d{2}/\d{2})\s+(?P<description>.+?)\s+(?P<amount>\d+\.\d{2})$'),
        re.compile(r'^(?P<transaction_date>\d{2}/\d{2})\s+(?P<description>.+?)\s+(?P<amount>-?\d+\.\d{2})$'), # negative
        re.compile(r'^(?P<transaction_date>\d{2}/\d{2})\s+(?P<posting_date>\d{2}/\d{2})\s+\S+\s+\S+\s+(?P<description>.+?)\s+\$(?P<amount>\d+\.\d{2})$'),
        re.compile(r'^(?P<transaction_date>\d{2}/\d{2})\s+(?P<posting_date>\d{2}/\d{2})\s+\S+\s+\S+\s+(?P<description>.+?)\s+\$(?P<amount>\d+\.\d{2}-?)$')
    ]
    
    class Config:
        env_file = ".env"

settings = Settings()