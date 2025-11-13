"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    database_url: str = "postgresql://postgres:postgres@localhost:5434/langgraph_agent"
    db_sslmode: str = "disable"

    # LLM API Keys
    openai_api_key: str = ""
    google_api_key: str = ""

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

    # CORS Configuration (can be comma-separated string or list)
    cors_origins: Union[List[str], str] = "http://localhost:3000,http://localhost:3001"

    # Environment
    environment: str = "development"
    log_level: str = "INFO"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )

    @property
    def database_url_with_ssl(self) -> str:
        """
        Get database URL for asyncpg connection.
        
        Note: asyncpg uses 'ssl' parameter, not 'sslmode'.
        For local development with 'disable', we don't add any SSL parameter.
        """
        url = self.database_url
        
        # For development with SSL disabled, return URL as-is
        if self.db_sslmode == "disable":
            return url
        
        # For production with SSL enabled, asyncpg handles it differently
        # You may need to pass ssl context separately in production
        return url


# Global settings instance
settings = Settings()

