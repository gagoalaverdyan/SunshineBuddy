import requests
import telebot
from environs import Env
from telebot import types

from helper_functions import (
    build_precipitation_message,
    build_regional_message,
    build_weather_message,
    build_wind_message,
    emojify,
)

# Reading env
env = Env()
env.read_env()

# Bot initialization
bot = telebot.TeleBot(env.str("BOT_API_KEY"))
weather_data = dict()


# Welcome message
@bot.message_handler(commands=["start"])
def bot_start(message):
    bot.send_message(
        message.chat.id,
        "☀️",
    )
    bot.send_message(
        message.chat.id,
        "Feeling the sunshine?\nSunshine Buddy here!\nWink what city you're in and let's see your forecast!",
    )


# Handling text messages as city queries
@bot.message_handler(content_types=["text"])
def city_handler(message):
    global weather_data
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": message.text.strip(),
        "units": "metric",
        "appid": env.str("WEATHER_API_KEY"),
    }
    weather_query = requests.get(url, params=params)

    try:
        weather_query = requests.get(url, params=params)
        weather_query.raise_for_status()
        weather_data = weather_query.json()
        current_state = weather_data["weather"][0]["main"]

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("🌧️ Precipitation", callback_data="precipitation")
        btn2 = types.InlineKeyboardButton("💨 Wind", callback_data="wind")
        btn3 = types.InlineKeyboardButton("🏞️ Regional", callback_data="regional")
        btn4 = types.InlineKeyboardButton("🌤️ Forecast", callback_data="forecast")
        markup.add(btn1, btn2, btn3, btn4)

        bot.send_message(message.chat.id, emojify(current_state))
        bot.send_message(message.chat.id, build_weather_message(weather_data), reply_markup=markup)
    except:
        bot.send_message(message.chat.id, "🐧")
        bot.send_message(message.chat.id, "Unable to find that city. Try again.")


# Handling callback queries
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "precipitation":
        bot.send_message(call.message.chat.id, build_precipitation_message(weather_data))
    elif call.data == "wind":
        bot.send_message(call.message.chat.id, build_wind_message(weather_data))
    elif call.data == "regional":
        bot.send_message(call.message.chat.id, build_regional_message(weather_data))
    elif call.data == "forecast":
        bot.send_message(call.message.chat.id, "Forecast info")


# Keep the bot running
bot.polling(none_stop=True)
