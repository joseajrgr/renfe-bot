# Renfe Bot

This is a Telegram bot that helps users find train schedules and availability for Renfe trains.

## DEMO



https://github.com/user-attachments/assets/5a2754da-01c1-45df-b400-663a5773c37a




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

