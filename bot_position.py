# bot_position.py

import json
import os

POSITION_FILE = "position.json"

def save_position(lat, lon):
    """Save the radar position to a local JSON file."""
    with open(POSITION_FILE, "w") as f:
        json.dump({"lat": lat, "lon": lon}, f)

def load_position():
    """Load the radar position from a local JSON file."""
    if not os.path.exists(POSITION_FILE):
        return None
    with open(POSITION_FILE, "r") as f:
        return json.load(f)
