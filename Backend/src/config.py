from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    MONGODB_URL: str
    ENVIRONMENT: str
    OPENAI_API_KEY: str
    LANGCHAIN_TRACING_V2: bool
    LANGCHAIN_ENDPOINT: str
    LANGCHAIN_API_KEY: str
    LANGCHAIN_PROJECT: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

# Create a global instance
settings = get_settings() 