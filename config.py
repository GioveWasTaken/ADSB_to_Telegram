
# config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram credentials
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Local tar1090 JSON data URL
TAR1090_JSON_URL = "http://yourtar1090ipHERE!/data/aircraft.json"

# Default radar coordinates (overwritten by GPS sent via Telegram)
FEEDER_LAT = 41.0732
FEEDER_LON = 14.3271

# Maximum distance in km (0 = disable distance filtering)
MAX_KM = 0
