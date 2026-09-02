from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database import (
    get_latest_movies,
    get_top_movies,
    get_movie_by_id,
    increase_views,
    add_history
)


router = Router()


def movie_button(movie):
    return [
        InlineKeyboardButton(
            text=f"🎬 {movie['title']}",
            callback_data=f"catalog_movie:{movie['id']}"
        )
    ]


@router.message(F.text == "🔥 Premyeralar")
async def premieres(message: Message):

    movies = await get_latest_movies(10)

    if not movies:
        await message.answer(
            "🔥 <b>PREMYERALAR</b>\n\n"
            "Hozircha yangi kinolar mavjud emas.",
            parse_mode="HTML"
        )
        return

    text = "🔥 <b>YANGI PREMYERALAR</b>\n\n"

    buttons = []

    for movie in movies:
        text += (
            f"🎬 <b>{movie['title']}</b>\n"
            f"🔢 Kod: <code>{movie['code']}</code>\n"
            f"📅 {movie['year'] or 'Nomaʼlum'}\n"
            f"⭐ {movie['rating']}\n\n"
        )

        buttons.append(movie_button(movie))

    await message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=buttons
        ),
        parse_mode="HTML"
    )


@router.message(F.text == "⭐ Eng mashhurlar")
async def top_movies(message: Message):

    movies = await get_top_movies(10)

    if not movies:
        await message.answer(
            "⭐ <b>Eng mashhurlar</b>\n\n"
            "Hozircha kinolar mavjud emas.",
            parse_mode="HTML"
        )
        return

    text = "⭐ <b>Eng mashhurlar</b>\n\n"

    buttons = []

    for index, movie in enumerate(movies, start=1):

        text += (
            f"{index}. 🎬 <b>{movie['title']}</b>\n"
            f"🔢 Kod: <code>{movie['code']}</code>\n"
            f"⭐ {movie['rating']}\n"
            f"👀 {movie['views']} ta ko‘rish\n\n"
        )

        buttons.append(movie_button(movie))

    await message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=buttons
        ),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("catalog_movie:"))
async def catalog_movie(callback: CallbackQuery):

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

    await increase_views(movie["id"])

    await add_history(
        callback.from_user.id,
        movie["id"]
    )

    caption = (
        f"🎬 <b>{movie['title']}</b>\n\n"
        f"📝 {movie['description'] or 'Tavsif mavjud emas'}\n\n"
        f"🎭 Janr: {movie['genre'] or 'Nomaʼlum'}\n"
        f"📅 Yil: {movie['year'] or 'Nomaʼlum'}\n"
        f"⭐ Reyting: {movie['rating']}\n"
        f"👀 Ko‘rishlar: {movie['views'] + 1}\n\n"
        f"🔢 Kino kodi: <code>{movie['code']}</code>\n\n"
        f"🍿 <b>DONIMEDIA</b>"
    )

    await callback.message.answer_video(
        video=movie["file_id"],
        caption=caption,
        parse_mode="HTML"
    )

    await callback.answer()