
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


class Config:
    # Application security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-this-secret")

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Encryption
    # Supports both variable names, prioritizing ENCRYPTION_KEY.
    ENCRYPTION_KEY = (
        os.getenv("ENCRYPTION_KEY")
        or os.getenv("FERNET_KEY")
    )

    # CSRF protection
    WTF_CSRF_ENABLED = True

    # Session security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = (
        os.getenv("SESSION_COOKIE_SECURE", "False").lower() == "true"
    )
    PERMANENT_SESSION_LIFETIME = 3600

    # Application settings
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    # AI model path
    AI_MODEL_PATH = str(BASE_DIR / "ai_engine" / "model.pkl")
