from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Supabase config (usando as variáveis que você já tem)
    next_public_supabase_url: str
    next_public_supabase_publishable_key: str
    
    # Football API (já configurada)
    football_api_key: str
    
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def supabase_url(self) -> str:
        """Alias para compatibilidade"""
        return self.next_public_supabase_url
    
    @property
    def supabase_key(self) -> str:
        """Alias para compatibilidade"""
        return self.next_public_supabase_publishable_key


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Made with Bob
