import json

def dodaj_czas_do_jsona(czas):
    with open("nadgodziny.json", "r") as f:
        json_data = json.load(f)
    
    #print(json_data)

    czas_json = json_data["godziny"]*60+json_data["minuty"]
    czas += czas_json

    json_data["godziny"] = int(czas/60)
    json_data["minuty"] = czas%60

    with open("nadgodziny.json", "w") as f:
        json.dump(json_data, f)
    
    print(json_data["godziny"], "h", json_data["minuty"], "min")

def odejmij_czas_z_jsona(czas): 
    
    godziny, minuty = czas.split(",")
    czas = (60 * int(godziny) + int(minuty))
    
    with open("nadgodziny.json", "r") as f:
        json_data = json.load(f)
    
    #print(json_data)

    czas_json = json_data["godziny"]*60+json_data["minuty"]
    czas_json -= czas

    json_data["godziny"] = int(czas_json/60)
    json_data["minuty"] = czas_json%60

    with open("nadgodziny.json", "w") as f:
        json.dump(json_data, f)
    
    print(json_data["godziny"], "h", json_data["minuty"], "min")
    


def oblicz_nadgodziny():
    czas_rozpoczecia = input("Podaj czas rozpoczecia: ")
    czas_zakonczenia = input("Podaj czas zakonczenia: ")

    godzina_ropoczecia, minuta_rozpoczecia = czas_rozpoczecia.split(",")
    godzina_zakonczenia, minuta_zakonczenia = czas_zakonczenia.split(",")

    print(godzina_ropoczecia, minuta_rozpoczecia)
    print(godzina_zakonczenia, minuta_zakonczenia)

    czas = (60 * int(godzina_zakonczenia) + int(minuta_zakonczenia)) - (60 * int(godzina_ropoczecia) + int(minuta_rozpoczecia)) - 8*60

    print(int(czas/60), "h", czas%60, "min")
    print("Czy dodać nadgodziny do pliku? T/N")

    if input() == "N" or input() == "n": 
        print("Nadal nic nie robie")
    else: dodaj_czas_do_jsona(czas)

# if __name__ == "__main__":
with open("nadgodziny.json", "r") as f:
            json_data = json.load(f)
print(json_data["godziny"], "h", json_data["minuty"], "min")
print("1. Policz nadgodziny")
print("2. Odczyt nadgodzin z pliku")
print("3. Odejmij nadgodziny")

wybor = input("Wybierz opcję: ")

match wybor:
    case "1":
        oblicz_nadgodziny()
    case "2":
        print(json_data["godziny"], "h", json_data["minuty"], "min")
    case "3":
        czas = input("Podaj czas do odjęcia: ")
        odejmij_czas_z_jsona(czas)