import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from database import init_db

from handlers.start import router as start_router
from handlers.admin import router as admin_router
from handlers.movies import router as movies_router
from handlers.favorites import router as favorites_router
from handlers.search import router as search_router
from handlers.random_movie import router as random_router
from handlers.history import router as history_router
from handlers.ai_helper import router as ai_router
from handlers.help import router as help_router


async def main():
    print("🚀 DONIMEDIA ishga tushmoqda...")

    # Database
    await init_db()
    print("🗄 Database tayyor!")

    # Bot
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Routerlar
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(movies_router)
    dp.include_router(favorites_router)
    dp.include_router(search_router)
    dp.include_router(random_router)
    dp.include_router(history_router)
    dp.include_router(ai_router)
    dp.include_router(help_router)
    print("✅ DONIMEDIA ishga tushdi!")
    print("🎬 Kino tizimi: ON")
    print("🔐 Majburiy obuna: ON")
    print("👑 Admin panel: ON")
    print("❤️ Sevimlilar: ON")

    try:
        await dp.start_polling(bot)

    finally:
        await bot.session.close()
        print("🛑 DONIMEDIA to'xtadi.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot to'xtatildi.")