import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID_1 = os.getenv("CHANNEL_ID_1")
CHANNEL_ID_2 = os.getenv("CHANNEL_ID_2")

ADMIN_ID = os.getenv("ADMIN_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi!")

if not CHANNEL_ID_1:
    raise ValueError("CHANNEL_ID_1 topilmadi!")

if not CHANNEL_ID_2:
    raise ValueError("CHANNEL_ID_2 topilmadi!")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID topilmadi!")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY topilmadi!")


ADMIN_ID = int(ADMIN_ID)

CHANNEL_ID_1 = CHANNEL_ID_1.strip()
CHANNEL_ID_2 = CHANNEL_ID_2.strip()