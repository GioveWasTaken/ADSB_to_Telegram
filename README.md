# ✈️ ADS-B to Telegram Bot

> Don't know what this is about or want to build your own radar station?
> 👉 Check this amazing guide: [https://sdr-enthusiasts.gitbook.io/ads-b](https://sdr-enthusiasts.gitbook.io/ads-b)

This bot connects to your local tar1090-based ADS-B setup, monitors real-time aircraft above your home, and sends alerts directly to your Telegram chat.

---

## ⚡ QUICK SETUP (for lazy people, like me)

1. 🚀 Clone the repository:

   ```bash
   git clone https://github.com/yourusername/adsb-to-telegram.git
   cd adsb-to-telegram
   ```

2. 🛡️ Create your `.env` file:

   ```bash
   cp .env.example .env
   ```

   Then edit `.env` and add your bot token and chat ID.

   > 💡 You can use `chatidfinder.py` to get your chat ID automatically.

3. 📦 Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. ▶️ Start the bot:

   ```bash
   python main.py
   ```

5. 🐳 (Optional) Use Docker:

   ```bash
   docker-compose up --build -d
   ```

---

## 📄 Telegram Commands

| Command              | Description                                  |
| -------------------- | -------------------------------------------- |
| `/getid`             | Returns your chat ID                         |
| `/menu`              | Displays configuration summary               |
| `10-300`             | Set scan interval in seconds                 |
| 📌 Send location     | Set radar position via Telegram location pin |
| `fr24`, `adsb`, etc. | Set tracking provider link type              |

---

## 🛠️ How to Install with Docker

1. Copy `.env.example` to `.env` and fill in your credentials
2. Run the bot:

   ```bash
   docker-compose up --build -d
   ```
3. To stop:

   ```bash
   docker-compose down
   ```

---

## 🛠️ Detailed Setup

### ✅ Requirements

* tar1090 running locally ([http://localhost:8080/data/aircraft.json](http://localhost:8080/data/aircraft.json))
* Python 3.9+ or Docker
* Telegram bot token from @BotFather
* Your Telegram chat ID

### 📁 Files Explained

* `main.py`: Core bot logic and aircraft scanner
* `config.py`: Default location, tar1090 URL, distance filter
* `settings_manager.py`: Runtime config: interval, provider, language
* `bot_position.py`: Saves radar position (via Telegram or config)
* `messages.py`: Language dictionary for multi-language support
* `.env.example`: Template for user config
* `Dockerfile` + `docker-compose.yml`: Optional Docker support

### ⚙️ config.py Options

* `TAR1090_JSON_URL`: default is `http://192.168.1.2:8080/data/aircraft.json`
* `FEEDER_LAT / FEEDER_LON`: fallback radar location
* `MAX_KM`: max distance from radar (0 = unlimited)

---

## 📂 Project Structure

```
adsb-to-telegram/
├── main.py
├── config.py
├── settings_manager.py
├── bot_position.py
├── messages.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 🧪 Compatible With

* Raspberry Pi 4/5 (64-bit OS)
* Python 3.11+
* tar1090
* Docker & Docker Compose
* Telegram Bot API v20+

---

## 🙌 Credits

Made with Love and Coffee by Giove.
MIT Licensed.
Free to use, modify, share, and track planes for fun.
