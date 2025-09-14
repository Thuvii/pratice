import os
from supabase import create_client, Client
from dotenv import load_dotenv



def get_client() -> Client:
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_KEY in .env")
    return create_client(url, key)

def main():
    supabase = get_client()

    try:
        res = supabase.table("movies").select("*").execute()
        print(res.data)
    except Exception as e:
        print(f'error: {e}')

if __name__ ==  "__main__":
    main()     
    
