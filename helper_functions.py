from datetime import datetime


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
    if degree < 0 or degree > 360:
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
def utc_to_timezone(shift_seconds):
    hours = abs(shift_seconds // 3600)
    minutes = abs((shift_seconds % 3600) // 60)
    
    sign = '+' if shift_seconds >= 0 else '-'
    timezone_str = f"UTC{sign}{hours:02d}:{minutes:02d}"
    
    return timezone_str

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

    message = f"{desription.title()}\n\n"
    message += f"It's {temp}°C in {location}\n"
    message += f"Feels like {feels_like}°C\n\n"
    message += f"☁️ Cloudiness: {cloudiness} %\n"
    message += f"📊 Pressure: {pressure} hPa\n"
    message += f"💧 Humidity: {humidity} %\n"
    message += f"🛣️ Visibility: {visibility} km\n"

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

    if message:
        return message
    else:
        return f"{emojify(weather_data["weather"][0]["main"])} No precipitation currently!\nEnjoy your day 😊"

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
