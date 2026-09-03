from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="➕ Kino qo'shish"),
                KeyboardButton(text="🗑 Kino o'chirish")
            ],
            [
                KeyboardButton(text="🎬 Kinolar"),
                KeyboardButton(text="📊 Statistika")
            ],
            [
                KeyboardButton(text="📢 Reklama")
            ],
            [
                KeyboardButton(text="⬅️ Bosh menyu")
            ]
        ],
        resize_keyboard=True
    )