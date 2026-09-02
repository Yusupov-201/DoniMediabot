from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🎬 Kino kodlari"),
                KeyboardButton(text="🔥 Premyeralar")
            ],
            [
                KeyboardButton(text="🔎 Kino qidirish"),
                KeyboardButton(text="🎯 Tasodifiy kino")
            ],
            [
                KeyboardButton(text="⭐ Eng mashhurlar"),
                KeyboardButton(text="❤️ Sevimlilar")
            ],
            [
                KeyboardButton(text="🕐 Tarix"),
                KeyboardButton(text="🤖 AI yordamchi")
            ],
            [
                KeyboardButton(text="🆘 Yordam")
            ]
        ],
        resize_keyboard=True
    )