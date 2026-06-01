from supabase import Client
from app.db.supabase import get_supabase_client

class BaseRepository:
    """
    Base repository class that initializes the Supabase client.
    Other repositories inherit from this to share the same client connection.
    """
    def __init__(self, client: Client = None):
        self.client = client or get_supabase_client()
