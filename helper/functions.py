from datetime import datetime

import requests
from environs import Env

# Reading env
env = Env()
env.read_env()

# Global variables4
aqi_info = dict()

# Turns weather condition into an emoji
def emojify(weather_state: str) -> str:
    match weather_state:
        case "Thunderstorm":
            return "⚡"
        case "Drizzle":
            return "🌦️"
        case "Rain":
            return "🌧️"
        case "Snow":
            return "❄️"
        case "Clear":
            return "☀️"
        case "Clouds":
            return "☁️"
        case _:
            return "💨"
        
# Turns wind degrees to a wind direction as a word 
def get_wind_direction(degree: int) -> str:
    if not (0 <= degree <= 360):
        return "Invalid degree"

    directions = [
        "North", "North-Northeast", "Northeast", "East-Northeast",
        "East", "East-Southeast", "Southeast", "South-Southeast",
        "South", "South-Southwest", "Southwest", "West-Southwest",
        "West", "West-Northwest", "Northwest", "North-Northwest"
    ]

    idx = round(degree / 22.5) % 16
    return directions[idx]

# Turns UTC shift in seconds into timezone
def utc_to_timezone(shift_seconds: int) -> str:
    hours = abs(shift_seconds // 3600)
    minutes = abs((shift_seconds % 3600) // 60)
    
    sign = '+' if shift_seconds >= 0 else '-'
    return f"UTC{sign}{hours:02d}:{minutes:02d}"

# Turns AQI Code to air quality state
def aqi_state(aqi: int) -> str:
    match aqi:
        case 1:
            return "Good"
        case 2:
            return "Fair"
        case 3:
            return "Moderate"
        case 4:
            return "Poor"
        case 5:
            return "Very Poor"
        case _:
            return "No information"


# Gets Air Quality Info
def get_aqi(lat: float, lon: float) -> dict:
    global aqi_info

    url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": env.str("WEATHER_API_KEY"),
    }

    aqi_query = requests.get(url, params=params).json()
    aqi = aqi_query["list"][0]["main"]["aqi"]
    aqi_info = {
        "index": aqi,
        "state": aqi_state(aqi),
        "co": round(float(aqi_query["list"][0]["components"]["co"]), 4),
        "no": round(float(aqi_query["list"][0]["components"]["no"]), 4),
        "no2": round(float(aqi_query["list"][0]["components"]["no2"]), 4),
        "o3": round(float(aqi_query["list"][0]["components"]["o3"]), 4),
        "so2": round(float(aqi_query["list"][0]["components"]["so2"]), 4),
        "pm2_5": round(float(aqi_query["list"][0]["components"]["pm2_5"]), 4),
        "pm10": round(float(aqi_query["list"][0]["components"]["pm10"]), 4),
        "nh3": round(float(aqi_query["list"][0]["components"]["nh3"]), 4),
    }
    return aqi_info

# Builds the current weather response
def build_weather_message(weather_data: dict) -> str:
    location = f"{weather_data["name"]}, {weather_data["sys"]["country"]}"
    desription = weather_data["weather"][0]["description"]
    temp = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    cloudiness = weather_data["clouds"]["all"]
    pressure = weather_data["main"]["pressure"]
    humidity = weather_data["main"]["humidity"]
    visibility = round(float(weather_data["visibility"]) / 1000, 2)
    air_quality = get_aqi(weather_data["coord"]["lat"], weather_data["coord"]["lon"])["state"]

    message = f"{desription.title()}\n\n"
    message += f"It's {temp}°C in {location}\n"
    message += f"Feels like {feels_like}°C\n\n"
    message += f"☁️ Cloudiness: {cloudiness} %\n"
    message += f"📊 Pressure: {pressure} hPa\n"
    message += f"💧 Humidity: {humidity} %\n"
    message += f"🛣️ Visibility: {visibility} km\n"
    message += f"🍀 Air Quality: {air_quality}"

    return message

# Builds the response for precipitation handler
def build_precipitation_message(weather_data: dict) -> str:
    message = ""

    if "rain" in weather_data.keys():
        message += "🌧️ Rain:\n"
        for h, m in weather_data["rain"].items():
            message += f"Last {h}: {m}mm\n"
    if "snow" in weather_data.keys():
        message += "❄️ Snow:\n"
        for h, m in weather_data["snow"].items():
            message += f"Last {h}: {m}mm\n"

    if not message:
        message = f"{emojify(weather_data['weather'][0]['main'])} No precipitation currently!\nEnjoy your day 😊"

    return message

# Builds the response for wind handler
def build_wind_message(weather_data: dict) -> str:
    message = ""

    speed = weather_data["wind"]["speed"]
    deg = get_wind_direction(weather_data["wind"]["deg"])

    message += f"🍃 Wind speed: {speed} m/s\n"
    message += f"🧭 Wind direction: {deg}\n"

    return message

# Build the response for regional handler
def build_regional_message(weather_data: dict) -> str:
    message = ""

    sunrise = datetime.fromtimestamp(weather_data["sys"]["sunrise"]).strftime("%H:%M")
    sunset = datetime.fromtimestamp(weather_data["sys"]["sunset"]).strftime("%H:%M")
    timezone = utc_to_timezone(weather_data["timezone"])
    longitude = weather_data["coord"]["lon"]
    latitude = weather_data["coord"]["lat"]

    message += f"🌄 Sunrise: {sunrise}\n"
    message += f"🌇 Sunset: {sunset}\n"
    message += f"🌎 Timezone: {timezone}\n\n"
    message += f"🧭 Longitude: {longitude}°\n"
    message += f"🧭 Latitude: {latitude}°\n\n"

    return message

# Build the response for regional handler
def build_air_quality_message() -> str:
    global aqi_info

    message = ""

    message += f"Air Quality Index: {aqi_info["index"]} ({aqi_info["state"]})\n\n"
    message += "Polluting gases:\n"
    for k, v in aqi_info.items():
        if k in ("index", "state"):
            continue
        else:
            message += f"{k.upper()}: {v} μg/m3\n"

    return message
