from supabase import create_client, Client
from app.core.config import settings

def get_supabase_client() -> Client:
    """
    Returns an initialized Supabase client using credentials from settings.
    Requires SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY to be set.
    Using the service role key enables bypassing RLS for admin-level operations.
    """
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError("Supabase credentials are not properly configured in environment variables.")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
