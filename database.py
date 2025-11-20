import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("ERRO: Variáveis SUPABASE_URL e SUPABASE_KEY não estão no .env")


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
