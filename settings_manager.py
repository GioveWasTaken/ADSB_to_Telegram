# settings_manager.py

import json
import os

SETTINGS_FILE = "settings.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {
            "interval": 30,
            "provider": "radarbox",
            "language": "en"
        }
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

def save_interval(seconds):
    settings = load_settings()
    settings["interval"] = seconds
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

def get_interval():
    return load_settings().get("interval", 30)

def get_tracking_provider():
    return load_settings().get("provider", "radarbox")

def save_tracking_provider(provider):
    settings = load_settings()
    settings["provider"] = provider
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

def get_language():
    return load_settings().get("language", "en")

def save_language(language_code):
    settings = load_settings()
    settings["language"] = language_code
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)
