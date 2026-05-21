import requests
import pandas as pd
from datetime import datetime


API_KEY = '          '  # I removed my API key 
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

def fetch_live_weather(city_name):
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather = {
            'city': city_name,
            'datetime': datetime.utcfromtimestamp(data['dt']),
            'TMAX': data['main']['temp_max'],
            'TMIN': data['main']['temp_min'],
            'TAVG': data['main']['temp'],
            'AWND': data['wind']['speed'] if 'wind' in data and 'speed' in data['wind'] else None,
            'PRCP': data['rain']['1h'] if 'rain' in data and '1h' in data['rain'] else 0.0,
            'SEASON': get_season(datetime.utcfromtimestamp(data['dt']).month)
        }
        return pd.DataFrame([weather])
    else:
        print(f"Failed to fetch weather for {city_name}: {response.status_code}")
        return None

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

if __name__ == "__main__":
    city = input("Enter city name: ")
    df = fetch_live_weather(city)
    if df is not None:
        print(df)
    else:
        print("No data fetched.")
