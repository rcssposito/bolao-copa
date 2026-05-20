from supabase import create_client, Client
from app.config import get_settings


def get_supabase_client() -> Client:
    """Create and return Supabase client instance"""
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_key)


# Global client instance
supabase: Client = get_supabase_client()

# Made with Bob
