from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database import search_movies, get_movie_by_id


router = Router()


class SearchMovie(StatesGroup):
    query = State()


# =========================================================
# 🔎 KINO QIDIRISHNI BOSHLASH
# =========================================================

@router.message(F.text == "🔎 Kino qidirish")
async def search_start(message: Message, state: FSMContext):

    await state.set_state(SearchMovie.query)

    await message.answer(
        "🔎 <b>KINO QIDIRISH</b>\n\n"
        "🎬 Kino nomini yoki kodini yozing.\n\n"
        "Masalan:\n"
        "<code>Avatar</code>\n"
        "<code>125</code>\n\n"
        "❌ Bekor qilish uchun /cancel yozing.",
        parse_mode="HTML"
    )


# =========================================================
# 🔎 QIDIRUV NATIJASI
# =========================================================

@router.message(SearchMovie.query)
async def search_result(
    message: Message,
    state: FSMContext
):

    query = message.text.strip()

    if query.lower() == "/cancel":

        await state.clear()

        await message.answer(
            "❌ Qidiruv bekor qilindi."
        )

        return

    if not query:

        await message.answer(
            "❌ Qidiruv so‘rovi bo‘sh bo‘lmasin."
        )

        return

    movies = await search_movies(query)

    await state.clear()

    if not movies:

        await message.answer(
            "😔 <b>Kino topilmadi.</b>\n\n"
            "Boshqa nom yoki kod bilan qidirib ko‘ring.",
            parse_mode="HTML"
        )

        return

    text = (
        "🔎 <b>QIDIRUV NATIJALARI</b>\n\n"
        f"🎬 Topildi: <b>{len(movies)}</b> ta kino\n\n"
    )

    buttons = []

    for movie in movies:

        text += (
            f"🎬 <b>{movie['title']}</b>\n"
            f"🔢 Kod: <code>{movie['code']}</code>\n"
            f"⭐ Reyting: {movie['rating']}\n"
            f"👀 Ko‘rishlar: {movie['views']}\n\n"
        )

        buttons.append([
            InlineKeyboardButton(
                text=f"▶️ {movie['title']}",
                callback_data=f"search_movie:{movie['id']}"
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
# 🎬 KINONI OCHISH
# =========================================================

@router.callback_query(
    F.data.startswith("search_movie:")
)
async def search_movie_open(
    callback: CallbackQuery
):

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
        f"🔢 Kino kodi: <code>{movie['code']}</code>\n\n"
        f"🍿 <b>DONIMEDIA</b>"
    )

    await callback.message.answer_video(
        video=movie["file_id"],
        caption=caption,
        parse_mode="HTML"
    )

    await callback.answer()