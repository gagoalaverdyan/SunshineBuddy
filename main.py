import requests
import telebot
from environs import Env
from telebot import types

from helper_functions import buld_weather_message, emojify

# Reading env
env = Env()
env.read_env()

# Bot initialization
bot = telebot.TeleBot(env.str("BOT_API_KEY"))


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


@bot.message_handler(content_types=["text"])
def city_handler(message):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": message.text.strip(),
        "units": "metric",
        "appid": env.str("WEATHER_API_KEY"),
    }
    weather_query = requests.get(url, params=params)

    if weather_query.status_code == 200:
        weather_data = weather_query.json()
        current_state = weather_data["weather"][0]["main"]

        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("🏞️ Additional", callback_data="additional")
        btn2 = types.InlineKeyboardButton("🌧️ Precipation", callback_data="precipation")
        btn3 = types.InlineKeyboardButton("💨 Wind", callback_data="wind")
        btn4 = types.InlineKeyboardButton("🌤️ Forecast", callback_data="wind")
        markup.add(btn1, btn2, btn3, btn4)

        bot.send_message(message.chat.id, emojify(current_state))
        bot.send_message(message.chat.id, buld_weather_message(weather_data), reply_markup=markup)


bot.polling(none_stop=True)
