import requests
import telebot
from environs import Env

# Reading env
env = Env()
env.read_env()

bot = telebot.TeleBot(env.str("BOT_API_KEY"))


@bot.message_handler(commands=["start"])
def bot_start(message):
    bot.send_message(message.chat.id, "Hello!")


bot.polling(none_stop=True)
