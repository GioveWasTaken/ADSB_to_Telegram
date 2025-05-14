# main.py

import asyncio
import requests
import json
from math import radians, cos, sin, sqrt, atan2
from datetime import datetime
from telegram import Bot, Update
from telegram.ext import Application, MessageHandler, CommandHandler, CallbackQueryHandler, filters
from config import TELEGRAM_BOT_TOKEN, TAR1090_JSON_URL, FEEDER_LAT, FEEDER_LON, MAX_KM, CHAT_ID
from bot_position import load_position, save_position
from settings_manager import get_interval, get_tracking_provider, save_interval, save_tracking_provider

SEEN_FILE = "aircraft_seen.json"
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# ----------------------- Aircraft Monitoring -----------------------

def load_seen_aircraft():
    try:
        with open(SEEN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_seen_aircraft(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(seen, f, indent=2)

def fetch_aircraft():
    try:
        response = requests.get(TAR1090_JSON_URL)
        response.raise_for_status()
        return response.json().get("aircraft", [])
    except Exception as e:
        print("[ERROR] Failed to fetch aircraft data:", e)
        return []

def guess_airline(callsign):
    if not callsign or len(callsign) < 3 or callsign.upper() in ["N/A", "N_D"]:
        return "Private"
    prefix = callsign[:3].upper()
    airlines = {
        "RYR": "Ryanair", "AZA": "ITA Airways", "THY": "Turkish Airlines",
        "DLH": "Lufthansa", "AFR": "Air France", "BAW": "British Airways",
        "EZY": "easyJet", "WZZ": "Wizz Air"
    }
    return airlines.get(prefix, "Private")

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def format_aircraft_info(aircraft, count, distance_km):
    now = datetime.utcnow().strftime("%d/%m/%Y %H:%M UTC")
    callsign = aircraft.get("flight") or "N/D"
    altitude_ft = aircraft.get("alt_baro", 0)
    altitude_km = round(altitude_ft * 0.0003048, 2) if altitude_ft else "N/A"
    direction = aircraft.get("track", "N/A")
    icao = aircraft.get("hex", "N/A")
    airline = guess_airline(callsign)
    distance_str = f"{round(distance_km, 1)} km" if distance_km else "N/D"

    provider = get_tracking_provider()
    if provider == "fr24":
        link = f"https://www.flightradar24.com/data/flights/{callsign}"
    elif provider == "adsb":
        link = f"https://globe.adsbexchange.com/?icao={icao}"
    elif provider == "flightaware":
        link = f"https://flightaware.com/live/mode-s/{icao}"
    else:
        link = f"https://www.radarbox.com/callsign/{callsign}"

    return (
        f"✈️ Aircraft detected:\n"
        f"🕒 {now}\n"
        f"📞 Call Sign: {callsign}\n"
        f"🏢 Airline: {airline}\n"
        f"📍 Heading: {direction}°\n"
        f"📈 Altitude: {altitude_ft} ft ({altitude_km} km)\n"
        f"📡 Distance: {distance_str}\n"
        f"🔁 Seen: {count} time(s)\n"
        f"🆔 ICAO: {icao}\n"
        f"🌍 {link}"
    )

async def monitor_aircraft():
    print("[INFO] Aircraft monitoring started...")
    seen_aircraft = load_seen_aircraft()

    while True:
        interval = get_interval()
        radar_pos = load_position()
        lat_radar = radar_pos["lat"] if radar_pos else FEEDER_LAT
        lon_radar = radar_pos["lon"] if radar_pos else FEEDER_LON

        aircraft_list = fetch_aircraft()

        for aircraft in aircraft_list:
            icao = aircraft.get("hex")
            if not icao:
                continue

            callsign = aircraft.get("flight")
            lat = aircraft.get("lat")
            lon = aircraft.get("lon")
            distance_km = None

            if lat and lon:
                distance_km = calculate_distance(lat_radar, lon_radar, lat, lon)
                if MAX_KM > 0 and distance_km > MAX_KM:
                    continue

            count = seen_aircraft.get(icao, 0) + 1
            seen_aircraft[icao] = count

            if (not callsign or callsign.upper() == "N/A") and count < 2:
                continue

            if count == 1 or (count == 2 and (not callsign or callsign.upper() == "N/A")):
                msg = format_aircraft_info(aircraft, count, distance_km)
                print(f"[INFO] New aircraft detected: {icao}")
                try:
                    await bot.send_message(chat_id=CHAT_ID, text=msg)
                except Exception as e:
                    print("[ERROR] Failed to send Telegram message:", e)

        save_seen_aircraft(seen_aircraft)
        await asyncio.sleep(interval)

# ----------------------- Telegram Bot Handlers -----------------------

async def get_chat_id(update: Update, context):
    chat_id = update.effective_chat.id
    print(f"✅ Your chat_id is: {chat_id}")
    await update.message.reply_text(f"Your chat_id is: {chat_id}")

async def receive_location(update: Update, context):
    location = update.message.location
    if location:
        save_position(location.latitude, location.longitude)
        await update.message.reply_text(
            f"✅ Radar position saved:\nLat: {location.latitude}\nLon: {location.longitude}"
        )

async def receive_text(update: Update, context):
    text = update.message.text.strip()
    if text.isdigit():
        value = int(text)
        if 10 <= value <= 300:
            save_interval(value)
            await update.message.reply_text(f"⏱️ Interval updated to {value} seconds.")
        else:
            await update.message.reply_text("❗ Please enter a number between 10 and 300.")
    elif text.lower() in ["fr24", "adsb", "radarbox", "flightaware"]:
        save_tracking_provider(text.lower())
        await update.message.reply_text(f"✅ Tracking provider set to: {text.lower()}")
    else:
        await update.message.reply_text("❗ Invalid input. Use the /menu command or send a number.")

async def show_menu(update: Update, context):
    menu_text = (
        "🛠️ Settings Menu:\n\n"
        "📍 Send your GPS location using the 📎 in Telegram.\n"
        "⏱️ Send a number (10–300) to change the interval.\n"
        "🌐 Send one of: fr24 / adsb / radarbox / flightaware to change tracking provider."
    )
    await update.message.reply_text(menu_text)

async def handle_callback(update: Update, context):
    pass  # For future use

# ----------------------- App Entry Point -----------------------

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.LOCATION, receive_location))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_text))
    app.add_handler(CommandHandler("menu", show_menu))
    app.add_handler(CommandHandler("getid", get_chat_id))
    app.add_handler(CallbackQueryHandler(handle_callback))

    loop = asyncio.get_event_loop()
    loop.create_task(monitor_aircraft())
    app.run_polling()

if __name__ == "__main__":
    main()
