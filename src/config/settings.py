"""
Configuration management with environment-specific settings
"""
from pydantic import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Bot Configuration
    telegram_token: str
    bot_username: str = "ClaudeNewsBot"
    
    # AI Configuration
    gemini_api_key: str
    
    # Database (SQLite for local development)
    database_url: str = "sqlite:///data/bot.db"
    
    # Features
    enable_web_search: bool = True
    enable_analytics: bool = True
    max_file_size_mb: int = 10
    
    # File Paths
    uploads_dir: str = "data/uploads"
    exports_dir: str = "data/exports"
    templates_dir: str = "data/templates"
    
    # Rate Limiting
    rate_limit_per_minute: int = 20
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "data/bot.log"
    
    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()