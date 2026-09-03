from aiogram import Router, F
from aiogram.types import Message

from keyboards.main import main_menu


router = Router()


@router.message(F.text == "🆘 Yordam")
async def help_handler(message: Message):

    text = (
        "🆘 <b>DONIMEDIA YORDAM MARKAZI</b>\n\n"

        "🎬 <b>Kino kodlari</b>\n"
        "Kino kodini yuboring va kerakli filmni tezda toping.\n\n"

        "🔥 <b>Premyeralar</b>\n"
        "Botga eng yangi qo‘shilgan kinolarni ko‘ring.\n\n"

        "🔎 <b>Kino qidirish</b>\n"
        "Kino nomi yoki janri orqali qidirish mumkin.\n\n"

        "🎯 <b>Tasodifiy kino</b>\n"
        "Tasodifiy kino tanlab beradi.\n\n"

        "⭐ <b>Eng mashhurlar</b>\n"
        "Eng ko‘p ko‘rilgan kinolar ro‘yxati.\n\n"

        "❤️ <b>Sevimlilar</b>\n"
        "Yoqtirgan kinolaringizni saqlab qo‘ying.\n\n"

        "🕐 <b>Tarix</b>\n"
        "Oldin ko‘rgan kinolaringizni ko‘ring.\n\n"

        "🤖 <b>AI yordamchi</b>\n"
        "Gemini AI orqali kino tanlash va savollaringizga javob olish.\n\n"

        "📌 <b>Kino qanday olinadi?</b>\n"
        "1️⃣ Majburiy kanalga obuna bo‘ling.\n"
        "2️⃣ Kino kodini yuboring.\n"
        "3️⃣ Bot kinoni yuboradi.\n\n"

        "💬 Muammo yoki taklif bo‘lsa, administrator bilan bog‘laning.\n\n"

        "🎥 <b>DONIMEDIA</b> — kino olamiga qulay kirish!"
    )

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=main_menu()
    )