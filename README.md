# Renfe Bot

This is a Telegram bot that helps users find train schedules and availability for Renfe trains.

## DEMO

[![Video demostrativo](https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg)](https://i.imgur.com/0XKsp9r.mp4)


## Features

- Search for train stations
- Select departure and arrival stations
- Choose travel dates
- Monitor specific train numbers for availability updates

## Setup

To run this bot, you'll need to:

1. Install Python and pip
2. Set up a virtual environment
3. Install required dependencies (`python -m pip install python-telegram-bot selenium`)
4. Obtain a Telegram API token
5. Download the [ChromeDriver](https://developer.chrome.com/docs/chromedriver/downloads) executable for Selenium

## Configuration

Replace the values in file named  `config.py` with your own API_TOKEN and CHROME_DRIVER_PATH.

## Usage

1. Run the bot using Python: `python bot.py`

2. Start interacting with the bot by sending `/origen` command.

## Dependencies

This project uses the following libraries:

- python-telegram-bot
- selenium
- re
- datetime

Make sure these are installed in your virtual environment.

