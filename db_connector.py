import os
import datetime
# from dotenv import load_dotenv
from supabase import create_client, Client

#load_dotenv()

#db_url = os.getenv("SUPABASE_URL")
#db_key = os.getenv("SUPABASE_KEY")


def load_to_db(time: datetime.time, ID: int = 1, db_url: str = None, db_key: str = None):
    
    if isinstance(time, datetime.timedelta):
        print(time)
        time = datetime.time(time.seconds // 3600, (time.seconds // 60) % 60)
    
    hours = time.hour
    minutes = time.minute
    
    supabase: Client = create_client(db_url, db_key)

    supabase.table("nadgodziny").update({"godziny": hours}).eq("ID", ID).execute()
    supabase.table("nadgodziny").update({"minuty": minutes}).eq("ID", ID).execute()
    
def read_from_db(supabase: Client, ID: int = 1, db_url: str = None, db_key: str = None) -> datetime:
    #supabase: Client = create_client(db_url, db_key)

    godziny = supabase.table("nadgodziny").select("godziny").eq("ID", ID).execute() # where ID = 1
    minuty = supabase.table("nadgodziny").select("minuty").eq("ID", ID).execute() # where ID = 1
    #print(godziny, minuty)
    
    godziny = int(godziny.data[0]["godziny"])
    minuty = int(minuty.data[0]["minuty"])

    return datetime.time(int(godziny), int(minuty))

def connect_to_db(db_url: str = None, db_key: str = None) -> Client:
    if db_url is None or db_key is None:
        raise ValueError("Database URL and key must be provided.")

    client = create_client(db_url, db_key)
    
    return client

