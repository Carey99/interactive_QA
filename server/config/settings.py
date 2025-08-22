"""
Configuration settings for the Startup Business Guide API

This module handles all configuration settings using Pydantic Settings
for environment variable validation and type safety.
"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    
    All settings have sensible defaults and can be overridden
    via environment variables or .env file
    """
    
    model_config = {"extra": "allow"}  # Allow extra fields from .env
    
    # Groq API Configuration
    GROQ_API_KEY: str = ""
    
    # LLM Configuration
    MODEL_NAME: str = "llama-3.1-8b-instant"  # Fast, high-quality model
    MAX_TOKENS: int = 1000
    TEMPERATURE: float = 0.7  # Good balance of creativity and consistency
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8001  # Local development port
    DEBUG: bool = False  # Production mode for Vercel
    
    # CORS Configuration - Updated for split deployment
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000,https://interactive-qa-ai.vercel.app,https://*.vercel.app"
    
    @property
    def allowed_origins(self) -> List[str]:
        """Convert comma-separated origins to list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 60
    
    # Application Settings
    APP_NAME: str = "Startup Business Guide API"
    APP_VERSION: str = "1.0.0"
    
    # Startup Business Guide specific settings
    SYSTEM_PROMPT: str = """You are an expert startup business advisor and guide. Your role is to provide accurate, helpful, and actionable advice for entrepreneurs and startup founders.

Key areas of expertise:
- Business plan development
- Legal requirements and documentation
- Funding and investment strategies  
- Market research and validation
- Regulatory compliance
- International business and travel requirements
- Financial planning and management
- Team building and operations

Guidelines:
- Provide specific, actionable advice
- Include relevant documentation requirements when applicable
- Mention important deadlines or time-sensitive considerations
- Suggest reliable sources for additional information
- Be comprehensive but concise
- Use clear, professional language
- Structure responses with bullet points or numbered lists when helpful

Always aim to give practical, implementable guidance that helps users take concrete next steps."""

    model_config = {
        "extra": "allow",
        "env_file": ".env",
        "case_sensitive": True
    }


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    
    Using lru_cache ensures settings are loaded only once
    and reused across the application
    
    Returns:
        Settings: Validated settings instance
    """
    return Settings()
