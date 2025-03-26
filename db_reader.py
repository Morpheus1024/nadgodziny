import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

db_url = os.getenv("SUPABASE_URL")
db_key = os.getenv("SUPABASE_KEY")


def load_to_db(hours: int, minutes: int, ID: int = 1):
    supabase: Client = create_client(db_url, db_key)

    supabase.table("nadgodziny").update({"godziny": hours}).eq("ID", ID).execute()
    supabase.table("nadgodziny").update({"minuty": minutes}).eq("ID", ID).execute()
    
def read_from_db(ID: int = 1):
    supabase: Client = create_client(db_url, db_key)

    godziny = supabase.table("nadgodziny").select("godziny").eq("ID", ID).execute() # where ID = 1
    minuty = supabase.table("nadgodziny").select("minuty").eq("ID", ID).execute() # where ID = 1

    return godziny.data[0]['godziny'], minuty.data[0]['minuty']

if not db_url or not db_key:
    raise ValueError("Supabase URL and key must be set as environment variables.")
