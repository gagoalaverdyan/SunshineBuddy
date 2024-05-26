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
    pressure = weather_data["main"]["pressure"]
    humidity = weather_data["main"]["humidity"]

    message = f"{desription.title()}\n\n"
    message += f"It's {temp}°C in {location}\n"
    message += f"Feels like {weather_data["main"]["feels_like"]}°C\n"

    return message
