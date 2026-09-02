from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database import get_history, get_movie_by_id


router = Router()


# =========================================================
# 🕐 TARIX
# =========================================================

@router.message(F.text == "🕐 Tarix")
async def show_history(message: Message):

    movies = await get_history(
        message.from_user.id,
        10
    )

    if not movies:
        await message.answer(
            "🕐 <b>KO‘RISH TARIXI</b>\n\n"
            "Hozircha hech qanday kino ko‘rmagansiz. 🎬",
            parse_mode="HTML"
        )
        return

    text = "🕐 <b>OXIRGI KO‘RILGAN KINOLAR</b>\n\n"

    buttons = []

    for movie in movies:

        text += (
            f"🎬 <b>{movie['title']}</b>\n"
            f"🔢 Kod: <code>{movie['code']}</code>\n"
            f"⭐ Reyting: {movie['rating']}\n\n"
        )

        buttons.append([
            InlineKeyboardButton(
                text=f"▶️ {movie['title']}",
                callback_data=f"history_movie:{movie['id']}"
            )
        ])

    await message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=buttons
        ),
        parse_mode="HTML"
    )


# =========================================================
# 🎬 TARIXDAGI KINONI OCHISH
# =========================================================

@router.callback_query(
    F.data.startswith("history_movie:")
)
async def history_movie(callback: CallbackQuery):

    movie_id = int(
        callback.data.split(":")[1]
    )

    movie = await get_movie_by_id(movie_id)

    if not movie:
        await callback.answer(
            "❌ Kino topilmadi!",
            show_alert=True
        )
        return

    caption = (
        f"🎬 <b>{movie['title']}</b>\n\n"
        f"📝 {movie['description'] or 'Tavsif mavjud emas'}\n\n"
        f"🎭 Janr: {movie['genre'] or 'Nomaʼlum'}\n"
        f"📅 Yil: {movie['year'] or 'Nomaʼlum'}\n"
        f"⭐ Reyting: {movie['rating']}\n"
        f"👀 Ko‘rishlar: {movie['views']}\n\n"
        f"🔢 Kod: <code>{movie['code']}</code>\n\n"
        f"🍿 <b>DONIMEDIA</b>"
    )

    await callback.message.answer_video(
        video=movie["file_id"],
        caption=caption,
        parse_mode="HTML"
    )

    await callback.answer()