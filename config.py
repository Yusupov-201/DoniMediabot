import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ADMIN_ID = os.getenv("ADMIN_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

if not CHANNEL_ID:
    raise ValueError("CHANNEL_ID topilmadi!")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID topilmadi!")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY topilmadi!")

# Telegram ID raqamga aylantiriladi
ADMIN_ID = int(ADMIN_ID)