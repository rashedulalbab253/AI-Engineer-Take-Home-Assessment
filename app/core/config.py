import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "LexDraft AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # DB configuration
    SQLITE_URL: str = "sqlite:///./data/db/lexdraft.db"
    
    # Groq configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "dummy_key")
    
    # Storage
    UPLOAD_DIR: str = "./data/uploads"
    VECTOR_STORE_DIR: str = "./data/vector_store"
    
    # Model
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.VECTOR_STORE_DIR, exist_ok=True)
os.makedirs("./data/db", exist_ok=True)
