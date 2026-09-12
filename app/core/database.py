import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SECRET")
def get_supabase() -> Client:
  return create_client(url, key)

supabase = get_supabase()