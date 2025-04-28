import json
import datetime
import db_connector as connector
import streamlit as st

db_url = st.secrets["SUPABASE_URL"]
db_key = st.secrets["SUPABASE_KEY"]

def add_times(a: datetime, b: datetime) -> datetime.time:
    """
    Adds two datetime objects together.
    """
    # Convert to timedelta
    datetime_a = datetime.datetime.combine(datetime.date.today(), a)
    datetime_b = datetime.datetime.combine(datetime.date.today(), b)

    # Oblicz różnicę między nimi (timedelta)
    time_difference = datetime_b - datetime_a


    combined_time_delta = datetime.timedelta(hours=a.hour, minutes=a.minute) + datetime.timedelta(hours=b.hour, minutes=b.minute)
    return combined_time_delta  


def subtract_times(a: datetime, b: datetime) -> datetime.time:
    hours = a.hour
    hours =- b.hour
    minutes = a.minute
    minutes =- b.minute
    
    if minutes < 0:
        hours -= 1
        minutes += 60
        
    return datetime.time(hours, minutes)

def load_data_from_json(filename: str = "nadgodziny.json"):
        with open(filename, "r") as f:
            json_data = json.load(f)
        return json_data

def save_data_to_json(data: dict, filename: str = "nadgodziny.json"):
        with open(filename, "w") as f:
            json.dump(json_data, f)
            
def dodaj_czas_do_jsona(czas, json_data = None):
    
    if json_data is None:
        json_data = load_data_from_json()
    
    #print(json_data)

    czas_json = json_data["godziny"]*60+json_data["minuty"]
    czas += czas_json

    json_data["godziny"] = int(czas/60)
    json_data["minuty"] = czas%60

    with open("nadgodziny.json", "w") as f:
        json.dump(json_data, f)
    
    print(json_data["godziny"], "h", json_data["minuty"], "min")
    
def dodaj_czas_do_db(czas: datetime.time) -> None:
    oryginalny_czas = connector.read_from_db(db_url = db_url, db_key = db_key)
        
    czas = add_times(oryginalny_czas, czas)
    connector.load_to_db(ID=1,time = czas, db_url = db_url, db_key = db_key)

def odejmij_czas_z_jsona(czas): 
    
    godziny, minuty = czas.split(":")
    czas = (60 * int(godziny) + int(minuty))
    
    # with open("nadgodziny.json", "r") as f:
    #     json_data = json.load(f)
    json_data = load_data_from_json()
    
    #print(json_data)

    czas_json = json_data["godziny"]*60+json_data["minuty"]
    czas_json -= czas

    json_data["godziny"] = int(czas_json/60)
    json_data["minuty"] = czas_json%60

    with open("nadgodziny.json", "w") as f:
        json.dump(json_data, f)
    
    print(json_data["godziny"], "h", json_data["minuty"], "min")

def odejmij_czas_z_db(czas: datetime.time) -> None:
    oryginalny_czas = connector.read_from_db(db_url = db_url, db_key = db_key)
    czas = subtract_times(oryginalny_czas, czas)
    connector.load_to_db(time = czas, db_url = db_url, db_key = db_key)
    
def oblicz_nadgodziny(czas_rozpoczecia:str, czas_zakonczenia:str, debug = False):

    godzina_ropoczecia, minuta_rozpoczecia = czas_rozpoczecia.hour, czas_rozpoczecia.minute
    godzina_zakonczenia, minuta_zakonczenia = czas_zakonczenia.hour, czas_zakonczenia.minute

    if debug:
        print(f"Rozpoczęto o {godzina_ropoczecia}:{minuta_rozpoczecia}")
        print(f"Skończono o  {godzina_zakonczenia}:{minuta_zakonczenia}")

    czas = (60 * int(godzina_zakonczenia) + int(minuta_zakonczenia)) - (60 * int(godzina_ropoczecia) + int(minuta_rozpoczecia)) - (8*60)

    if debug:
        print(int(czas/60), "h", czas%60, "min")
        print("Czy dodać nadgodziny do pliku? T/N")
    
    if input() == "N" or input() == "n": 
        print("Nadal nic nie robie")
        exit()
    else: dodaj_czas_do_jsona(czas)
     
def oblicz_nadgodziny_datetime(czas_rozpoczecia: datetime.time, czas_zakonczenia: datetime.time) -> datetime.time:
    
    godzina_ropoczecia, minuta_rozpoczecia = czas_rozpoczecia.hour, czas_rozpoczecia.minute
    godzina_zakonczenia, minuta_zakonczenia = czas_zakonczenia.hour, czas_zakonczenia.minute
    
    czas = (60 * int(godzina_zakonczenia) + int(minuta_zakonczenia)) - (60 * int(godzina_ropoczecia) + int(minuta_rozpoczecia)) - (8*60)
    czas = datetime.time(czas//60, czas%60)
    return czas

if __name__ == "__main__":
    with open("nadgodziny.json", "r") as f:
                json_data = json.load(f)
    #print(json_data["godziny"], "h", json_data["minuty"], "min")
    print("1. Policz nadgodziny")
    print("2. Odczyt nadgodzin z pliku")
    print("3. Odejmij nadgodziny")
    
    wybor = input("Wybierz opcję: ")
    
    
    if wybor == "1":
        czas_rozpoczecia = input("Podaj czas rozpoczecia [gg:mm]: ")
        czas_zakonczenia = input("Podaj czas zakonczenia [gg:mm]: ")
        oblicz_nadgodziny(czas_rozpoczecia = czas_rozpoczecia, czas_zakonczenia = czas_zakonczenia)
    elif wybor == "2":
        print(json_data["godziny"], "h", json_data["minuty"], "min")
    elif wybor == "3":
        czas = input("Podaj czas do odjęcia: ")
        odejmij_czas_z_jsona(czas)