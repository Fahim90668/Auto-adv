from supabase import create_client, Client
from core.config import settings

# Client using anon/public key for user-facing operations (respects RLS)
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Client using service role key for administrative/background tasks (bypasses RLS)
supabase_admin: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)