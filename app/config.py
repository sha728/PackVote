from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "PackVote"
    VERSION: str = "1.0.0"
    
    # Database (MySQL Support)
    DATABASE_URL: str = "sqlite:///./packvote.db" 

    # Google APIs (Forms/Sheets/Maps)
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = None
    GOOGLE_SERVICE_ACCOUNT_FILE: Optional[str] = None
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    
    # OpenWeather / Open-Meteo
    
    # Email (SMTP)
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Google Form
    GOOGLE_FORM_LINK: str = "https://docs.google.com/forms/d/e/1FAIpQLScJEkvkVUi-xT-Tk9PaQgjA-nKe4Te0urxSeQaFMYd8UJT8FA/viewform?usp=header" # Default fallback
    
    # Gemini
    GEMINI_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

settings = Settings()
