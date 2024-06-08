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


# Builds the current weather response
def buld_weather_message(weather_data: dict) -> str:
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
