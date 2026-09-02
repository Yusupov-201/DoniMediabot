from aiogram import Router, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database import (
    get_favorites,
    remove_favorite,
    get_movie,
    increase_views,
    add_history,
    is_favorite
)


router = Router()


def favorite_buttons(movie_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="▶️ Kinoni ko‘rish",
                    callback_data=f"fav_watch:{movie_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💔 Sevimlidan o‘chirish",
                    callback_data=f"fav_delete:{movie_id}"
                )
            ]
        ]
    )


@router.message(F.text == "❤️ Sevimlilar")
async def show_favorites(message: Message):

    movies = await get_favorites(
        message.from_user.id
    )

    if not movies:
        await message.answer(
            "❤️ <b>Sevimlilar</b>\n\n"
            "Hozircha sevimli kinolaringiz yo‘q.\n\n"
            "Kino ko‘rayotganda ❤️ tugmasini bosib "
            "saqlashingiz mumkin.",
            parse_mode="HTML"
        )
        return

    text = "❤️ <b>SEVIMLI KINOLAR</b>\n\n"
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
                callback_data=f"fav_watch:{movie['id']}"
            )
        ])

        buttons.append([
            InlineKeyboardButton(
                text="💔 O‘chirish",
                callback_data=f"fav_delete:{movie['id']}"
            )
        ])

    await message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=buttons
        ),
        parse_mode="HTML"
    )


# ▶️ Sevimli kinoni ko‘rish
@router.callback_query(F.data.startswith("fav_watch:"))
async def watch_favorite(callback: CallbackQuery):

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

    # Ko‘rishlar
    await increase_views(movie["id"])

    # Tarix
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
        f"🔢 Kod: <code>{movie['code']}</code>\n\n"
        f"🍿 <b>DONIMEDIA</b>"
    )

    await callback.message.answer_video(
        video=movie["file_id"],
        caption=caption,
        reply_markup=favorite_buttons(movie["id"]),
        parse_mode="HTML"
    )

    await callback.answer()


# 💔 Sevimlidan o‘chirish
@router.callback_query(F.data.startswith("fav_delete:"))
async def delete_favorite(callback: CallbackQuery):

    movie_id = int(
        callback.data.split(":")[1]
    )

    await remove_favorite(
        callback.from_user.id,
        movie_id
    )

    await callback.answer(
        "💔 Sevimlilardan o‘chirildi!"
    )

    # Ro‘yxatni qayta chiqaramiz
    movies = await get_favorites(
        callback.from_user.id
    )

    if not movies:

        await callback.message.edit_text(
            "❤️ <b>Sevimlilar</b>\n\n"
            "Ro‘yxat bo‘sh.",
            parse_mode="HTML"
        )

        return

    text = "❤️ <b>SEVIMLI KINOLAR</b>\n\n"
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
                callback_data=f"fav_watch:{movie['id']}"
            )
        ])

        buttons.append([
            InlineKeyboardButton(
                text="💔 O‘chirish",
                callback_data=f"fav_delete:{movie['id']}"
            )
        ])

    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=buttons
        ),
        parse_mode="HTML"
    )


async def get_movie_by_id(movie_id):

    import aiosqlite
    from database import DB_PATH

    async with aiosqlite.connect(DB_PATH) as db:

        db.row_factory = aiosqlite.Row

        cursor = await db.execute(
            "SELECT * FROM movies WHERE id = ?",
            (movie_id,)
        )

        return await cursor.fetchone()