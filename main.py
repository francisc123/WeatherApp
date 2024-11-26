import matplotlib
import requests
import json
import sys
import csv


def toCSV(city):
    filename = "weather.csv"

    result = openWeather(city)

    if result is None:
        print("Nu s-au putut scrie datele în CSV deoarece orașul nu a fost găsit.")
        return

    row = {
        'city': city,
        'date': 'Astăzi',
        'temperature': result[0],
        'humidity': result[2],
        'pressure': result[1],
        'windspeed': result[3]
    }

    try:
        with open(filename, "r") as csvfile:
            has_header = csvfile.readline().strip() != ""
    except FileNotFoundError:
        has_header = False

    with open(filename, "a") as csvfile:
        fieldnames = ["city", "date", "temperature", "humidity", "pressure", "windspeed"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not has_header:
            writer.writeheader()

        writer.writerow(row)

    print("Informatiile au fost scrise in fisierul weather.csv!")


def openWeather(city):
    api_key = '47999480158747f21f92d001b4dff492'
    base_url = 'https://api.openweathermap.org/data/2.5'
    complete_url = base_url + '/weather?q=' + city + '&appid=' + api_key
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != 404:
        temp = float(data["main"]["temp"]) - 273.15
        temp = round(temp, 0)
        pressure = float(data["main"]["pressure"])
        humidity = float(data["main"]["humidity"])
        wind = float(data["wind"]["speed"])
        z = data["weather"][0]["description"]

        return temp, pressure, humidity, wind

    else:
        print("Orasul nu a fost gasit")

def makeChoice():
    print("Pentru ce oras sunteti interesat de datele meteo?")
    city = input("Introduceti numele orasului: ")

    return city


if __name__ == "__main__":
    while True:
        city = makeChoice()
        result = openWeather(city)

        if isinstance(result, str):  # Verificăm dacă este un mesaj de eroare
            print(result)
        else:
            print(f"Temperatura în orașul {city} este {result[0]} grade C")
            print(f"Presiunea atmosferică în orașul {city} este {result[1]} hPA")
            print(f"Umiditatea în orașul {city} este {result[2]} %")
            print(f"Viteza vântului în orașul {city} este {result[3]} km/h")
            toCSV(city)

        print("\nAveti nevoie de informatii pentru alt oras?")
        print("1. Da")
        print("2. Nu")
        choice2 = int(input("Alegeți o opțiune: "))

        if choice2 != 1:
            print("La revedere!")
            sys.exit(0)
