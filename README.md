# Sunshine Buddy
Sunshine Buddy is aTelegram bot that provides weather information using the `OpenWeatherMap API`. The bot is built using Python and the `pyTelegramBotAPI` library. (NOT IN PRODUCTION YET)

## Features
* Get current weather for any city
* Provides temperature and weather condition
* Wind, regional and precipitation information on-demand

## Requirements
* Python 3.6+
* Own Telegram Bot API Key
* Own OpenWeatherMap API key

## Todo
* 5-day forecast
* Daily push weather
* Favorite cities
* Units customization
* Location handling

## Installation

1. Clone the repository
```bash
git clone https://github.com/gagoalaverdyan/SunshineBuddy.git
cd SunshineBuddy
```
2. Set up a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Install the dependencies
```bash
pip install -r requirements.txt
```
4. Create a `.env` file and add the necessary environment variables
```plaintext
WEATHER_API_KEY=your_openweathermap_key
BOT_API_KEY=your_bot_key
```
5. Run the bot
```bash
python main.py
```

## Contributing
Pull requests are very welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License
The program is licensed under [GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) and is free to download, use or distribute.