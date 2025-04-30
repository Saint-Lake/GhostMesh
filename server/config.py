import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file (look up from current file's directory)
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class Settings:
    # JWT/Auth
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changeme")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    # Database
    DB_URL: str = os.getenv("DB_URL", "sqlite+aiosqlite:///./ghostmesh.db")

    # TLS / Certificate Paths
    CERT_FILE: str = os.getenv("CERT_FILE", "server/certs/cert.pem")
    KEY_FILE: str = os.getenv("KEY_FILE", "server/certs/key.pem")

    # Other optional C2-specific configs
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    API_RATE_LIMIT: int = int(os.getenv("API_RATE_LIMIT", 30))  # requests per minute

settings = Settings()
