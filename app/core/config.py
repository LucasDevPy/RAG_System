from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    # Safe dummy default prevents validation errors during CI imports
    openai_api_key: str = "sk-dummy-key-for-testing-purposes-only"
    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    chunk_size: int = 1000
    chunk_overlap: int = 200

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()